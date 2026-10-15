# Cronograma Markdown

Planeje e acompanhe um cronograma em arquivos Markdown versionados. O
script valida os dados e gera um site estático acessível com Gantt e
tabela, pronto para publicar no GitHub Pages. Não requer banco de dados,
backend ou edição manual do site gerado.

## Objetivo

Manter o cronograma como texto versionado no Git e gerar uma página
estática com: - gráfico de Gantt; - atividades, marcos, responsáveis,
duração e dependências; - progresso e estado das atividades; - histórico
de mudanças pelo Git.

## Princípios

1.  **Markdown é a fonte da verdade**: a visualização é gerada e nunca
    editada manualmente.
2.  **Sem banco ou backend**: arquivos do repositório são os dados.
3.  **CI reproduzível**: validar e gerar a publicação a cada alteração
    aprovada na branch principal.
4.  **Transparência**: distinguir datas planejadas, realizadas e
    estimadas.
5.  **Ferramenta independente**: não depender do Microsoft Project nem
    de formatos proprietários.

## Documentos

-   [`docs/spec.md`](docs/spec.md): requisitos funcionais e não
    funcionais.
-   [`docs/plano-gestao-cronograma.md`](docs/plano-gestao-cronograma.md):
    plano de gestão do cronograma, alinhado ao Domínio 3.
-   [`docs/formato-cronograma.md`](docs/formato-cronograma.md): formato
    dos dados em Markdown.
-   [`docs/ci-publicacao.md`](docs/ci-publicacao.md): pipeline e
    publicação.
-   [`cronograma/exemplo.md`](cronograma/exemplo.md): exemplo inicial de
    cronograma.

## Uso local

Requer Python 3.10 ou superior.

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/build.py --check
python scripts/build.py
```

O site será criado em `dist/index.html`. Adicione cada tarefa ou marco
como um arquivo `.md` em `cronograma/atividades/`, usando o front matter
YAML descrito em [`docs/formato-cronograma.md`](docs/formato-cronograma.md).
O calendário do MVP conta dias corridos. `start` e `finish` são as datas
planejadas; campos `baseline_*` e `actual_*` registram linha de base e
datas reais separadamente.

## Publicação no GitHub Pages

Envie o repositório para o GitHub usando a branch `main`. Em **Settings
→ Pages**, escolha **GitHub Actions** como fonte de publicação. O workflow
valida pull requests e, em pushes para `main`, gera e publica o site.

O exemplo em `cronograma/exemplo.md` é apenas demonstrativo. Copie e
adapte os registros para `cronograma/atividades/` depois de confirmar
datas e responsáveis com a equipe.

## Escopo do MVP

O MVP deve validar arquivos, calcular/representar dependências, gerar
Gantt estático e publicar os artefatos. Edição colaborativa avançada,
login, notificações e integração com ferramentas externas ficam fora do
escopo inicial.

## Nota acadêmica

A solução apoia práticas de planejamento, sequenciamento, estimativa,
acompanhamento e comunicação do cronograma. Ela não substitui a análise
da equipe nem determina automaticamente se uma previsão é realista. A
adequação ao projeto real depende de validar escopo, calendário,
estimativas e dependências com os integrantes.
