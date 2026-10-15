# Formato dos dados do cronograma

## 1. Estrutura recomendada

Cada atividade fica em um arquivo Markdown dentro de
`cronograma/atividades/`. Isso torna as alterações pequenas e fáceis de
revisar. Um arquivo agregador pode ordenar as atividades e gerar a
visualização.

## 2. Campos propostos

  Campo               Obrigatório                    Regra
  ------------------- ------------------------------ -------------------------------------------------
  `id`                Sim                            Identificador único e estável, como `T-001`
  `title`             Sim                            Nome curto e compreensível
  `start`             Sim para atividade planejada   Data ISO `AAAA-MM-DD`
  `finish`            Sim para atividade planejada   Data ISO `AAAA-MM-DD`
  `type`              Sim                            `task` ou `milestone`
  `owner`             Recomendado                    Nome ou papel responsável
  `status`            Sim                            `not_started`, `in_progress`, `blocked`, `done`
  `progress`          Sim                            Inteiro de 0 a 100
  `depends_on`        Não                            Lista de IDs predecessores
  `baseline_start`    Na linha de base               Data aprovada inicial
  `baseline_finish`   Na linha de base               Data aprovada inicial
  `actual_start`      Não                            Data real de início
  `actual_finish`     Não                            Data real de término
  `notes`             Não                            Premissas, riscos ou contexto

## 3. Exemplo de atividade

``` markdown
---
id: T-001
title: Levantar requisitos do cronograma
type: task
start: 2026-10-19
finish: 2026-10-20
owner: Murilo Escobedo
status: not_started
progress: 0
depends_on: []
---

## Resultado esperado

Lista validada das atividades, estimativas, marcos e dependências do projeto.

## Premissas

- Datas ilustrativas; substituir pelas datas acordadas pelo grupo.
- Confirmar a disponibilidade dos responsáveis antes de aprovar a linha de base.
```

## 4. Exemplo de marco

``` markdown
---
id: M-001
title: Aprovação da linha de base
type: milestone
start: 2026-10-23
finish: 2026-10-23
owner: Equipe
status: not_started
progress: 0
depends_on:
  - T-001
---

## Critério de conclusão

A equipe revisou e aprovou o cronograma inicial.
```

## 5. Convenções

-   Usar datas ISO para evitar ambiguidades entre formatos regionais.
-   Não reutilizar IDs removidos.
-   Usar o mesmo vocabulário de estados em todos os arquivos.
-   Para marco, `start` e `finish` devem ser a mesma data.
-   Datas do exemplo são demonstrativas e não constituem compromisso
    real da equipe.
-   O MVP deve declarar se duração é contada em dias corridos ou úteis.
    A escolha precisa ser uniforme.
-   Não calcular datas finais automaticamente a partir de dependências
    sem que essa regra esteja documentada e testada.
