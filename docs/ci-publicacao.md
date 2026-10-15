# Geração e publicação

O workflow consulta o GitHub Project v2, gera um artefato HTML estático e publica no GitHub Pages. Ele roda em pushes para `main`, por agendamento horário ou sob demanda na aba Actions.

## Configuração necessária

Defina `PROJECT_OWNER` e `PROJECT_NUMBER` nas variáveis do repositório e `PROJECTS_TOKEN` nos secrets. Como alternativa, o workflow também aceita `PROJECT_OWNER` e `PROJECT_NUMBER` em secrets. Se `PROJECT_OWNER` não for informado, o workflow usa automaticamente o owner do repositório. O token precisa ler o Project; o `GITHUB_TOKEN` da execução não tem acesso a Projects. Para um Project de usuário, use um PAT clássico com `read:project`. Não grave tokens no código ou nos arquivos do projeto.

No GitHub Pages, habilite a publicação via GitHub Actions. Se a tela de configuração não estiver acessível, uma pessoa com permissão de administração pode habilitar o Pages pela API, usando GitHub CLI autenticado com escopo `repo`:

```sh
gh auth refresh -s repo
gh api --method POST repos/4snt/especificacao-cronograma-markdown/pages -f build_type=workflow
```

O workflow pede apenas `contents: read`, `pages: write` e `id-token: write` para o job de deploy.

## Atualização das tasks

O GitHub não inicia este workflow quando campos de data do Project são alterados. Por isso há uma execução horária, além de execução sob demanda. Para atualizar imediatamente, abra **Actions → Build and publish Gantt from GitHub Project → Run workflow**.

Tasks sem datas de início e fim são omitidas com aviso. Se nenhuma task válida tiver ambas as datas, a geração falha para evitar publicar um Gantt vazio.
