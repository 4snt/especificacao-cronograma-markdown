# Cronograma Markdown

Este repositório consulta as tasks de um **GitHub Project**, gera um gráfico de Gantt acessível e publica o site no GitHub Pages. As tasks e datas são mantidas no Project; este repositório contém o gerador e a documentação, sem uma cópia do cronograma em Markdown.

## Como funciona

1. Crie as tasks como issues e adicione-as ao GitHub Project.
2. Preencha os campos de data **Start date** e **Target date** no Project.
3. O GitHub Actions consulta o Project, gera `dist/index.html` e publica no Pages. A atualização ocorre em pushes para `main`, manualmente ou de hora em hora.

O gráfico inclui itens com as duas datas preenchidas. Mostra título, período, responsável, status e progresso. Responsáveis vêm dos assignees da issue ou do campo de pessoas `Owner`. O progresso vem do campo numérico `Progress` (0–100); se ausente, tasks concluídas aparecem com 100% e as demais com 0%.

## Configuração do repositório

Em **Settings → Secrets and variables → Actions**, crie:

- Secret `PROJECTS_TOKEN`: token com leitura do GitHub Project. O `GITHUB_TOKEN` padrão não tem acesso a Projects. Para um Project de usuário, a documentação do GitHub indica PAT clássico com escopo `read:project`; se as issues forem privadas, o token também precisa de acesso ao repositório.
- Variable `PROJECT_OWNER`: usuário ou organização que possui o Project.
- Variable `PROJECT_NUMBER`: número exibido na URL do Project.

Opcionalmente, defina as variáveis `PROJECT_START_FIELD`, `PROJECT_FINISH_FIELD`, `PROJECT_STATUS_FIELD` e `PROJECT_PROGRESS_FIELD` se os nomes dos campos forem diferentes dos padrões (`Start date`, `Target date`, `Status` e `Progress`).

Associe o repositório ao Project uma vez. Com GitHub CLI autenticado e atualizado, use:

```sh
gh project link PROJECT_NUMBER --owner PROJECT_OWNER --repo especificacao-cronograma-markdown
```

Em seguida, em **Settings → Pages**, escolha **GitHub Actions** como fonte. Execute o workflow **Build and publish Gantt from GitHub Project** pela aba **Actions** para a primeira publicação.

## Execução local

Requer Python 3.10 ou superior. Exporte `PROJECTS_TOKEN`, `PROJECT_OWNER` e `PROJECT_NUMBER` no ambiente e rode:

```sh
python3 scripts/build.py
```

O site será gerado em `dist/index.html`. O script não cria nem altera tasks, issues, Projects ou seus campos.

## Escopo

O Project é a fonte de verdade. Este repositório transforma os itens planejados em uma visualização estática; não é um gestor de tarefas, não edita o board e não guarda uma lista paralela de atividades.

Consulte [a configuração da integração](docs/github-project.md), [a especificação](docs/spec.md) e [o fluxo de publicação](docs/ci-publicacao.md).
