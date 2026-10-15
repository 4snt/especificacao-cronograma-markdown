#!/usr/bin/env python3
"""Build an accessible Gantt site from a GitHub Projects v2 board."""
from __future__ import annotations

import html
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUERY = """
query($owner: String!, $number: Int!, $after: String) {
  repositoryOwner(login: $owner) {
    ... on User { projectV2(number: $number) { ...ProjectSchedule } }
    ... on Organization { projectV2(number: $number) { ...ProjectSchedule } }
  }
}
fragment ProjectSchedule on ProjectV2 {
  title
  items(first: 100, after: $after) {
    nodes {
      fieldValues(first: 50) { nodes {
        ... on ProjectV2ItemFieldDateValue { date field { ... on ProjectV2FieldCommon { name } } }
        ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
        ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2FieldCommon { name } } }
        ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { name } } }
        ... on ProjectV2ItemFieldUserValue { users(first: 10) { nodes { login } } field { ... on ProjectV2FieldCommon { name } } }
      } }
      content {
        ... on Issue { title url state assignees(first: 10) { nodes { login } } }
        ... on PullRequest { title url state assignees(first: 10) { nodes { login } } }
        ... on DraftIssue { title body }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}
"""


def fetch_page(token: str, owner: str, number: int, after: str | None) -> dict:
    payload = json.dumps({"query": QUERY, "variables": {"owner": owner, "number": number, "after": after}}).encode()
    request = Request("https://api.github.com/graphql", data=payload, headers={
        "Authorization": f"Bearer {token}", "Content-Type": "application/json",
        "Accept": "application/vnd.github+json", "User-Agent": "cronograma-markdown-gantt",
    })
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except HTTPError as exc:
        raise RuntimeError(f"GitHub GraphQL retornou HTTP {exc.code}.") from exc
    except URLError as exc:
        raise RuntimeError(f"Não foi possível acessar a API do GitHub: {exc.reason}") from exc
    if result.get("errors"):
        messages = "; ".join(error.get("message", "erro GraphQL") for error in result["errors"])
        raise RuntimeError(f"Erro consultando o GitHub Project: {messages}")
    data = result.get("data", {})
    owner_node = data.get("repositoryOwner") or {}
    project = owner_node.get("projectV2")
    if not project:
        raise RuntimeError(f"Project #{number} não encontrado para o owner {owner!r}, ou token sem acesso de leitura.")
    return project


def load_project() -> tuple[str, list[dict]]:
    token = os.environ.get("PROJECTS_TOKEN") or os.environ.get("GH_PROJECT_TOKEN")
    owner = os.environ.get("PROJECT_OWNER", "").strip()
    number_raw = os.environ.get("PROJECT_NUMBER", "").strip()
    if not token:
        raise RuntimeError("Configure o secret PROJECTS_TOKEN com acesso de leitura ao GitHub Project.")
    if not owner or not number_raw.isdigit():
        raise RuntimeError("Configure PROJECT_OWNER e PROJECT_NUMBER nas variáveis do repositório.")
    number = int(number_raw)
    cursor, items, project_title = None, [], "GitHub Project"
    while True:
        project = fetch_page(token, owner, number, cursor)
        project_title = project["title"]
        connection = project["items"]
        items.extend(connection["nodes"])
        page = connection["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]
    return project_title, items


def mapped_value(fields: dict, preferred: str, fallback: str | None = None):
    return fields.get(preferred) if preferred in fields else fields.get(fallback) if fallback else None


def schedule_items(raw_items: list[dict]) -> tuple[list[dict], list[str]]:
    start_field = os.environ.get("PROJECT_START_FIELD", "Start date")
    finish_field = os.environ.get("PROJECT_FINISH_FIELD", "Target date")
    status_field = os.environ.get("PROJECT_STATUS_FIELD", "Status")
    progress_field = os.environ.get("PROJECT_PROGRESS_FIELD", "Progress")
    tasks, missing = [], []
    for item in raw_items:
        content = item.get("content")
        if not content:
            continue
        fields = {}
        for value in (item.get("fieldValues") or {}).get("nodes", []):
            field = value.get("field") or {}
            name = field.get("name")
            if name:
                fields[name] = value
        start = mapped_value(fields, start_field, "Start")
        finish = mapped_value(fields, finish_field, "Due date")
        start = start.get("date") if start else None
        finish = finish.get("date") if finish else None
        title = content.get("title", "(sem título)")
        if not start or not finish:
            missing.append(title)
            continue
        try:
            start_date, finish_date = date.fromisoformat(start), date.fromisoformat(finish)
        except ValueError as exc:
            raise RuntimeError(f"Datas inválidas no item {title!r}; use campos de data no Project.") from exc
        if finish_date < start_date:
            raise RuntimeError(f"A data final antecede a inicial no item {title!r}.")
        status_value = mapped_value(fields, status_field)
        status = (status_value or {}).get("name", "Open")
        progress_value = mapped_value(fields, progress_field, "Percent complete") or {}
        progress = progress_value.get("number", 100 if status.casefold() in {"done", "complete", "completed"} else 0)
        if isinstance(progress, (float, int)) and 0 <= progress <= 1:
            progress = round(progress * 100)
        try:
            progress = max(0, min(100, int(progress)))
        except (TypeError, ValueError):
            progress = 100 if status.casefold() in {"done", "complete", "completed"} else 0
        assignees = (content.get("assignees") or {}).get("nodes", [])
        owner_field = fields.get("Owner") or fields.get("Assignees") or {}
        owners = (owner_field.get("users") or {}).get("nodes", [])
        owner = ", ".join(user["login"] for user in (owners or assignees)) or "—"
        tasks.append({"title": title, "url": content.get("url", ""), "start": start,
                      "finish": finish, "status": status, "progress": progress, "owner": owner})
    if missing:
        print(f"Aviso: {len(missing)} item(ns) sem datas ({start_field} / {finish_field}) foram omitidos.", file=sys.stderr)
    if not tasks:
        print(f"Aviso: nenhum item tem {start_field!r} e {finish_field!r} preenchidos; o Gantt será publicado vazio.", file=sys.stderr)
    tasks.sort(key=lambda task: (task["start"], task["finish"], task["title"].casefold()))
    return tasks, missing


def render(project_title: str, tasks: list[dict], missing: list[str], output: Path) -> None:
    first = min((date.fromisoformat(task["start"]) for task in tasks), default=date.today())
    last = max((date.fromisoformat(task["finish"]) for task in tasks), default=first)
    span = max((last - first).days + 1, 1)
    rows, bars = [], []
    for task in tasks:
        start, finish = date.fromisoformat(task["start"]), date.fromisoformat(task["finish"])
        left = (start - first).days / span * 100
        width = max((finish - start).days + 1, 1) / span * 100
        status = task["status"]
        status_class = "".join(ch.lower() if ch.isalnum() else "-" for ch in status).strip("-")
        title = html.escape(task["title"])
        url = task["url"]
        link_title = f"<a href='{html.escape(url, quote=True)}'>{title}</a>" if url else title
        rows.append(f"<tr><td>{link_title}</td><td>{task['start']}</td><td>{task['finish']}</td><td>{html.escape(task['owner'])}</td><td>{html.escape(status)}</td><td>{task['progress']}%</td></tr>")
        bars.append(f"<div class='gantt-row'><div class='gantt-label'>{link_title}</div><div class='track' aria-label='{title}, {task['start']} a {task['finish']}'><span class='bar {status_class}' style='left:{left:.3f}%;width:{width:.3f}%' title='{task['start']} — {task['finish']}, {task['progress']}% concluído'><i style='width:{task['progress']}%'></i></span></div><span class='date'>{task['start']}</span></div>")
    if not bars:
        bars.append("<p class='muted'>Nenhuma task com datas preenchidas no Project.</p>")
    undated = ""
    if missing:
        items = "".join(f"<li>{html.escape(title)}</li>" for title in missing)
        undated = f"<h2>Tasks sem datas</h2><p class='muted'>Preencha os campos de início e fim no Project para incluí-las no Gantt.</p><div class='panel'><ul>{items}</ul></div>"
    period = (first.isoformat(), last.isoformat()) if tasks else ("—", "—")
    done = sum(task["progress"] == 100 for task in tasks)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit = os.environ.get("GITHUB_SHA", "local")[:12]
    content = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(project_title)} · Cronograma</title><style>
:root{{color-scheme:light;--ink:#182230;--muted:#64748b;--line:#e2e8f0;--blue:#2563eb;--green:#15803d}}*{{box-sizing:border-box}}body{{margin:0;background:#f8fafc;color:var(--ink);font:16px/1.5 system-ui,sans-serif}}main{{max-width:1200px;margin:auto;padding:40px 24px}}h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.1;margin:.3em 0}}h2{{margin-top:2.2rem}}.muted,.meta{{color:var(--muted)}}.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}}.card{{background:white;border:1px solid var(--line);border-radius:12px;padding:16px 20px;min-width:135px}}.card b{{display:block;font-size:1.5rem}}.panel{{background:white;border:1px solid var(--line);border-radius:14px;padding:20px;overflow:hidden}}.gantt-row{{display:grid;grid-template-columns:minmax(180px,280px) 1fr 100px;gap:12px;align-items:center;padding:9px 0;border-bottom:1px solid var(--line)}}.gantt-label{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.gantt-label a,td a{{color:inherit}}.track{{height:22px;background:repeating-linear-gradient(90deg,#f1f5f9 0,#f1f5f9 calc(10% - 1px),white calc(10% - 1px),white 10%);position:relative;border-radius:6px}}.bar{{position:absolute;top:2px;height:18px;min-width:8px;background:var(--blue);border-radius:5px;overflow:hidden}}.bar i{{display:block;height:100%;background:#16a34a}}.bar.done,.bar.completed{{background:var(--green)}}.date{{font-size:.82rem;color:var(--muted)}}.table-wrap{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:720px}}th,td{{padding:11px 12px;text-align:left;border-bottom:1px solid var(--line)}}thead{{background:#f1f5f9}}footer{{margin-top:32px;color:var(--muted);font-size:.9rem}}@media(max-width:700px){{main{{padding:24px 14px}}.gantt-row{{grid-template-columns:minmax(110px,34%) 1fr;gap:8px}}.date{{grid-column:2}}}}
</style></head><body><main><p class="muted">CRONOGRAMA · FONTE: GITHUB PROJECT</p><h1>{html.escape(project_title)}</h1><p class="muted">Gráfico gerado automaticamente a partir das tasks e campos de data do Project.</p><div class="cards"><div class="card"><b>{len(tasks)}</b>Tasks com datas</div><div class="card"><b>{done}</b>Concluídas</div><div class="card"><b>{period[0]}</b>Início</div><div class="card"><b>{period[1]}</b>Fim</div></div><h2>Gráfico de Gantt</h2><p class="muted">As barras representam o período das tasks; o preenchimento verde indica progresso.</p><section class="panel" aria-label="Gráfico de Gantt">{''.join(bars)}</section><h2>Tasks</h2><div class="panel table-wrap"><table><thead><tr><th>Task</th><th>Início</th><th>Fim</th><th>Responsável</th><th>Status</th><th>Progresso</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>{undated}<footer>Atualizado em {generated} · Commit <code>{html.escape(commit)}</code> · Dados consultados diretamente do GitHub Project.</footer></main></body></html>"""
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(content, encoding="utf-8")


def main() -> int:
    try:
        project_title, raw_items = load_project()
        tasks, missing = schedule_items(raw_items)
        output = Path(os.environ.get("OUTPUT_DIR", ROOT / "dist")).resolve()
        render(project_title, tasks, missing, output)
        print(f"{project_title}: {len(tasks)} task(s) no Gantt; site gerado em {output}.")
        return 0
    except RuntimeError as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
