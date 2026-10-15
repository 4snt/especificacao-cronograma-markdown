# Especificação do gerador de Gantt

## Objetivo

Publicar uma visualização estática do cronograma cujos dados vêm do GitHub Project v2. Tasks, responsáveis, status e datas são mantidos no board; este repositório não guarda uma segunda lista de tarefas.

## Requisitos

- Consultar itens do GitHub Project via GraphQL, incluindo Issues e draft issues.
- Usar campos de data do Project para determinar início e fim planejados.
- Gerar Gantt e tabela acessível com título, período, responsável, status e progresso.
- Omitir itens sem as duas datas, registrando aviso no log; falhar quando não houver item datado.
- Publicar HTML estático no GitHub Pages por GitHub Actions.
- Atualizar em pushes para `main`, manualmente e em uma cadência horária para refletir alterações feitas diretamente no Project.
- Não criar ou editar tasks e issues automaticamente.

## Limites

O MVP não calcula caminho crítico nem interpreta dependências. Usa dias corridos e exibe as datas preenchidas pela equipe. A API do GitHub exige token separado com leitura de Projects; o token padrão de Actions não cobre essa permissão.
