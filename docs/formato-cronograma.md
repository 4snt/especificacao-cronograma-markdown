# Dados do cronograma no GitHub Project

O GitHub Project é a fonte de dados; não há arquivos Markdown de tasks. Cada item planejado deve ser uma issue ou draft issue no Project.

## Campos esperados

| Dado | Origem | Obrigatório para o Gantt |
| --- | --- | --- |
| Título | Título da issue ou draft issue | Sim |
| Início | Campo de data `Start date` | Sim |
| Fim | Campo de data `Target date` | Sim |
| Status | Campo single-select `Status` | Não; padrão `Open` |
| Responsável | Assignee da issue ou campo user `Owner` | Não |
| Progresso | Campo numérico `Progress`, de 0 a 100 | Não; padrão 100 para status concluído e 0 nos outros casos |

Os nomes de campos podem ser configurados pelas variáveis de Actions descritas no README. Itens sem as duas datas são omitidos e listados como aviso no log da geração. Datas finais anteriores às iniciais falham a geração.

Datas de linha de base e datas reais podem existir no Project, mas não são confundidas com as datas planejadas mostradas no Gantt. O calendário é contado em dias corridos.
