#!/usr/bin/env python3
"""Validate Markdown schedule entries and render a self-contained static site."""
from __future__ import annotations

import argparse
import html
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VALID_STATUS = {"not_started", "in_progress", "blocked", "done"}
VALID_TYPES = {"task", "milestone"}
DATE_FIELDS = ("start", "finish", "baseline_start", "baseline_finish", "actual_start", "actual_finish")


def fail(path: Path, field: str, message: str) -> None:
    raise ValueError(f"{path.relative_to(ROOT)}: {field}: {message}")


def parse_file(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|$)(.*)\Z", raw, re.S)
    if not match:
        fail(path, "front matter", "expected YAML between opening and closing --- lines")
    try:
        item = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        fail(path, "front matter", str(exc).splitlines()[0])
    if not isinstance(item, dict):
        fail(path, "front matter", "expected a YAML mapping")
    item["_path"] = path
    item["_body"] = match.group(2).strip()
    return item


def as_date(item: dict, key: str, required: bool = False) -> date | None:
    value = item.get(key)
    if value is None:
        if required:
            fail(item["_path"], key, "required field is missing")
        return None
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    fail(item["_path"], key, "expected a valid ISO date (YYYY-MM-DD)")


def validate(items: list[dict]) -> None:
    by_id: dict[str, dict] = {}
    for item in items:
        path = item["_path"]
        for key in ("id", "title", "type", "status", "progress"):
            if key not in item:
                fail(path, key, "required field is missing")
        if not isinstance(item["id"], str) or not item["id"].strip():
            fail(path, "id", "must be a non-empty string")
        if item["id"] in by_id:
            fail(path, "id", f"duplicate identifier {item['id']!r}")
        by_id[item["id"]] = item
        if not isinstance(item["title"], str) or not item["title"].strip():
            fail(path, "title", "must be a non-empty string")
        if item["type"] not in VALID_TYPES:
            fail(path, "type", f"must be one of {', '.join(sorted(VALID_TYPES))}")
        if item["status"] not in VALID_STATUS:
            fail(path, "status", f"must be one of {', '.join(sorted(VALID_STATUS))}")
        if isinstance(item["progress"], bool) or not isinstance(item["progress"], int) or not 0 <= item["progress"] <= 100:
            fail(path, "progress", "must be an integer from 0 to 100")
        for key in DATE_FIELDS:
            as_date(item, key, key in ("start", "finish"))
        start, finish = as_date(item, "start", True), as_date(item, "finish", True)
        if finish < start:
            fail(path, "finish", "must be on or after start")
        if item["type"] == "milestone" and finish != start:
            fail(path, "finish", "milestones must have the same start and finish date")
        for a, b in (("baseline_start", "baseline_finish"), ("actual_start", "actual_finish")):
            da, db = as_date(item, a), as_date(item, b)
            if da and db and db < da:
                fail(path, b, f"must be on or after {a}")
        deps = item.get("depends_on", [])
        if not isinstance(deps, list) or any(not isinstance(dep, str) for dep in deps):
            fail(path, "depends_on", "must be a list of IDs")
        if len(deps) != len(set(deps)):
            fail(path, "depends_on", "contains duplicate IDs")

    graph: dict[str, list[str]] = {}
    for item in items:
        deps = item.get("depends_on", [])
        for dep in deps:
            if dep not in by_id:
                fail(item["_path"], "depends_on", f"unknown ID {dep!r}")
        graph[item["id"]] = deps
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, chain: list[str]) -> None:
        if node in visiting:
            cycle = " -> ".join(chain + [node])
            fail(by_id[node]["_path"], "depends_on", f"dependency cycle detected: {cycle}")
        if node in visited:
            return
        visiting.add(node)
        for dep in graph[node]:
            visit(dep, chain + [node])
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node, [])


def render(items: list[dict], output: Path) -> None:
    items.sort(key=lambda x: (as_date(x, "start", True), x["id"]))
    today = date.today()
    starts = [as_date(x, "start", True) for x in items]
    finishes = [as_date(x, "finish", True) for x in items]
    first = min(starts) if starts else today
    last = max(finishes) if finishes else first
    span = max((last - first).days + 1, 1)
    tasks = sum(x["type"] == "task" for x in items)
    milestones = len(items) - tasks
    rows, bars = [], []
    for item in items:
        start, finish = as_date(item, "start", True), as_date(item, "finish", True)
        left = (start - first).days / span * 100
        width = max((finish - start).days + 1, 1) / span * 100
        deps = ", ".join(item.get("depends_on", [])) or "—"
        status = item["status"].replace("_", " ")
        title = html.escape(item["title"])
        ident = html.escape(item["id"])
        owner = html.escape(str(item.get("owner", "—")))
        start_s, finish_s = start.isoformat(), finish.isoformat()
        rows.append(f"<tr><th scope='row'>{ident}</th><td>{title}</td><td>{start_s}</td><td>{finish_s}</td><td>{owner}</td><td>{html.escape(deps)}</td><td>{status}</td><td>{item['progress']}%</td></tr>")
        mark = item["type"] == "milestone"
        bars.append(f"<div class='gantt-row'><div class='gantt-label'><strong>{ident}</strong> {title}</div><div class='track' aria-label='{ident}, {start_s} até {finish_s}'><span class='bar {'milestone' if mark else status}' style='left:{left:.3f}%;width:{0 if mark else width:.3f}%;' title='{start_s} — {finish_s}, {item['progress']}% concluído'>{'◆' if mark else f'<i style="width:{item["progress"]}%"></i>'}</span></div><span class='date'>{start_s}</span></div>")
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    commit = __import__("os").environ.get("GITHUB_SHA", "local")[:12]
    content = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Cronograma do projeto</title><style>
:root{{color-scheme:light;--ink:#182230;--muted:#64748b;--line:#e2e8f0;--blue:#2563eb;--green:#15803d;--red:#b91c1c;--amber:#b45309}}*{{box-sizing:border-box}}body{{margin:0;background:#f8fafc;color:var(--ink);font:16px/1.5 system-ui,sans-serif}}main{{max-width:1200px;margin:auto;padding:40px 24px}}h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.1;margin:.3em 0}}h2{{margin-top:2.2rem}}.muted,.meta{{color:var(--muted)}}.cards{{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}}.card{{background:white;border:1px solid var(--line);border-radius:12px;padding:16px 20px;min-width:135px}}.card b{{display:block;font-size:1.5rem}}.panel{{background:white;border:1px solid var(--line);border-radius:14px;padding:20px;overflow:hidden}}.gantt-row{{display:grid;grid-template-columns:minmax(180px,260px) 1fr 100px;gap:12px;align-items:center;padding:9px 0;border-bottom:1px solid var(--line)}}.gantt-label{{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.track{{height:22px;background:repeating-linear-gradient(90deg,#f1f5f9 0,#f1f5f9 calc(10% - 1px),white calc(10% - 1px),white 10%);position:relative;border-radius:6px}}.bar{{position:absolute;top:2px;height:18px;min-width:8px;background:var(--blue);border-radius:5px;overflow:hidden}}.bar i{{display:block;height:100%;background:#16a34a}}.bar.blocked{{background:var(--red)}}.bar.done{{background:var(--green)}}.bar.not.started{{background:#64748b}}.bar.milestone{{background:transparent;color:#7c3aed;overflow:visible;top:-3px;font-size:22px;line-height:24px}}.date{{font-size:.82rem;color:var(--muted)}}.table-wrap{{overflow:auto}}table{{width:100%;border-collapse:collapse;min-width:850px}}th,td{{padding:11px 12px;text-align:left;border-bottom:1px solid var(--line)}}thead{{background:#f1f5f9}}footer{{margin-top:32px;color:var(--muted);font-size:.9rem}}@media(max-width:700px){{main{{padding:24px 14px}}.gantt-row{{grid-template-columns:minmax(110px,34%) 1fr;gap:8px}}.date{{grid-column:2}}}}
</style></head><body><main><p class="muted">CRONOGRAMA · DIAS CORRIDOS</p><h1>Plano do projeto</h1><p class="muted">Visualização gerada automaticamente a partir dos arquivos Markdown versionados.</p><div class="cards"><div class="card"><b>{tasks}</b>Tarefas</div><div class="card"><b>{milestones}</b>Marcos</div><div class="card"><b>{first.isoformat()}</b>Início planejado</div><div class="card"><b>{last.isoformat()}</b>Fim planejado</div></div><h2>Gráfico de Gantt</h2><p class="muted">Barras indicam o período planejado; o preenchimento verde indica progresso. ◆ indica marco.</p><section class="panel" aria-label="Gráfico de Gantt">{''.join(bars) if bars else '<p>Nenhuma atividade cadastrada.</p>'}</section><h2>Atividades</h2><div class="panel table-wrap"><table><thead><tr><th>ID</th><th>Atividade</th><th>Início</th><th>Fim</th><th>Responsável</th><th>Dependências</th><th>Estado</th><th>Progresso</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div><h2>Estados</h2><p>Não iniciada · Em andamento · Bloqueada · Concluída · ◆ Marco</p><footer>Gerado em {generated} · Commit <code>{html.escape(commit)}</code> · Fonte: <code>cronograma/atividades/*.md</code></footer></main></body></html>"""
    output.mkdir(parents=True, exist_ok=True)
    (output / "index.html").write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate without generating files")
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    paths = sorted((ROOT / "cronograma" / "atividades").glob("*.md"))
    try:
        items = [parse_file(path) for path in paths]
        validate(items)
        if not args.check:
            render(items, args.output.resolve())
        print(f"Cronograma válido: {len(items)} atividade(s)." + ("" if args.check else f" Site gerado em {args.output}."))
        return 0
    except (ValueError, TypeError) as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
