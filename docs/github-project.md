# Integração com GitHub Projects

## Fonte dos dados

O board do GitHub Project v2 é a fonte única das tasks e datas. Este repositório não contém uma cópia das tasks. O gerador consulta a conexão `items` do Project via GraphQL e não altera o board.

## Campos lidos

- Título do item (Issue, draft issue ou pull request).
- Campos de data `Start date` e `Target date`.
- Campo single-select `Status`.
- Assignees da issue ou campo user `Owner`.
- Campo numérico `Progress`, de 0 a 100.

Se os campos tiverem outros nomes, configure as variáveis de repositório indicadas no README. Itens sem ambas as datas aparecem no log como omitidos. Issues são links clicáveis na tabela e no Gantt.

## Associar o repositório ao Project

Com GitHub CLI e permissão para alterar o Project:

```sh
gh auth refresh -s project
gh project link PROJECT_NUMBER --owner PROJECT_OWNER --repo especificacao-cronograma-markdown
```

No URL do board, o número aparece no final, por exemplo `/users/conta/projects/3` ou `/orgs/equipe/projects/3`.

## Token para leitura pelo workflow

O `GITHUB_TOKEN` do Actions tem escopo limitado ao repositório e não pode consultar Projects. Crie um PAT clássico com escopo `read:project` e salve-o como secret `PROJECTS_TOKEN`. Se as issues vinculadas forem privadas, conceda também acesso de leitura ao repositório. Nunca faça commit do token.
