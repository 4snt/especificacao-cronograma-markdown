# Especificação de Requisitos --- Cronograma Markdown

**Status:** proposta inicial\
**Versão:** 0.1\
**Foco acadêmico:** Domínio 3 --- Cronograma\
**Responsável pelo recorte:** Plano de Gestão de Cronograma --- Murilo
Escobedo

## 1. Problema

Ferramentas tradicionais de cronograma podem exigir software específico,
edição manual e compartilhamento de arquivos difíceis de revisar. O
projeto propõe manter os dados em Markdown no Git e gerar
automaticamente uma visualização acessível pelo navegador.

## 2. Objetivo do produto

Permitir que uma equipe planeje, documente, visualize e acompanhe as
atividades de um projeto usando arquivos de texto versionados, com
gráfico de Gantt gerado em CI e publicação estática.

## 3. Usuários e necessidades

-   **Integrantes da equipe:** consultar tarefas, responsáveis,
    dependências, datas e andamento.
-   **Responsável pelo cronograma:** manter estimativas, sequência,
    linha de base e previsões atualizadas.
-   **Professor e partes interessadas:** entender rapidamente a
    sequência de trabalho e os marcos.
-   **Revisores do repositório:** verificar alterações por pull request
    e histórico do Git.

## 4. Requisitos funcionais

-   **RF-01 --- Cadastro textual:** cada atividade deve ser descrita em
    arquivo Markdown seguindo um esquema documentado.
-   **RF-02 --- Identificação:** cada atividade deve ter identificador
    único e título.
-   **RF-03 --- Planejamento temporal:** permitir data de início e fim
    planejadas ou duração e calendário claramente definidos.
-   **RF-04 --- Dependências:** registrar predecessoras por
    identificador e validar referências.
-   **RF-05 --- Responsabilidade:** permitir um ou mais responsáveis por
    atividade.
-   **RF-06 --- Marcos:** representar eventos importantes sem duração.
-   **RF-07 --- Progresso:** registrar percentual concluído e estado
    atual.
-   **RF-08 --- Linha de base:** preservar a versão aprovada do
    planejamento inicial, sem confundi-la com datas atualizadas.
-   **RF-09 --- Gantt:** gerar gráfico que mostre atividades, marcos,
    duração, dependências quando suportadas, progresso e datas.
-   **RF-10 --- Validação automática:** CI deve falhar com mensagem
    clara para identificadores duplicados, campos obrigatórios ausentes,
    datas inválidas, progresso fora de 0--100 e dependências
    inexistentes.
-   **RF-11 --- Publicação:** gerar um site estático publicável por
    GitHub Pages ou serviço equivalente.
-   **RF-12 --- Histórico:** alterações de cronograma devem ser
    rastreáveis pelo histórico de commits e pull requests.
-   **RF-13 --- Relatório:** gerar resumo com datas inicial/final,
    quantidade de tarefas, marcos e tarefas atrasadas quando os dados
    necessários estiverem disponíveis.
-   **RF-14 --- Documentação:** explicar como adicionar atividades,
    alterar datas, registrar progresso e aprovar mudanças.

## 5. Requisitos não funcionais

-   **RNF-01 --- Custo:** operar com ferramentas gratuitas e hospedagem
    estática gratuita, dentro dos limites do provedor.
-   **RNF-02 --- Sem backend:** não exigir servidor de aplicação, banco
    de dados, login ou armazenamento externo.
-   **RNF-03 --- Portabilidade:** dados legíveis em qualquer editor de
    texto.
-   **RNF-04 --- Acessibilidade:** incluir tabela textual alternativa ao
    gráfico e não depender apenas de cores.
-   **RNF-05 --- Manutenibilidade:** pipeline e formato de dados
    documentados.
-   **RNF-06 --- Segurança:** não armazenar segredos ou dados pessoais
    desnecessários no repositório público.
-   **RNF-07 --- Reprodutibilidade:** mesmas entradas e versão de
    ferramentas devem produzir artefatos equivalentes.
-   **RNF-08 --- Responsividade:** visualização utilizável em telas
    desktop e móveis.

## 6. Regras de negócio

1.  O identificador de cada tarefa é único e estável; não deve depender
    do título.
2.  Uma dependência deve apontar para uma tarefa existente.
3.  Dependências circulares são inválidas.
4.  Datas finais não podem anteceder datas iniciais.
5.  Marcos têm duração zero e uma data definida.
6.  O percentual concluído é um inteiro de 0 a 100.
7.  A linha de base aprovada é imutável no fluxo normal; alterações
    exigem revisão e nova versão identificada.
8.  Datas planejadas, datas reais e previsões são conceitos diferentes e
    devem ser rotulados separadamente.
9.  O calendário de trabalho (dias úteis, feriados e jornada) deve ser
    declarado; se não for implementado no MVP, as durações serão
    tratadas como dias corridos e isso deve aparecer na documentação.
10. A ferramenta mostra dados e valida consistência; decisões sobre
    replanejamento cabem à equipe.

## 7. Fora do escopo do MVP

-   Banco de dados e API;
-   autenticação e permissões por usuário dentro do site;
-   edição visual interativa do Gantt;
-   sincronização com Microsoft Project, Jira, Trello ou calendário;
-   cálculo avançado de caminho crítico, nivelamento de recursos ou
    simulação probabilística;
-   envio de notificações;
-   gestão financeira completa.

## 8. Critérios de aceite

-   Um integrante consegue criar uma tarefa editando apenas um arquivo
    Markdown.
-   Uma alteração válida gera o Gantt e atualiza a página publicada via
    CI.
-   Uma referência de dependência inexistente impede a publicação e
    aponta o erro.
-   Uma dependência circular impede a publicação.
-   A página apresenta Gantt e tabela acessível com as mesmas tarefas.
-   A linha de base não é sobrescrita silenciosamente por alterações do
    cronograma corrente.
-   A documentação permite que outro integrante reproduza a publicação
    sem instruções verbais.
-   O repositório não contém banco de dados, credenciais ou serviço
    backend obrigatório.

## 9. Decisões técnicas propostas

-   **Fonte:** Markdown com front matter YAML ou uma tabela Markdown
    padronizada. Recomenda-se front matter por tarefa para permitir
    validação consistente.
-   **Geração:** script determinístico executado na CI; pode gerar HTML
    estático e uma visualização Mermaid Gantt ou biblioteca equivalente.
-   **Hospedagem:** GitHub Pages, se o repositório estiver no GitHub e
    as configurações do projeto permitirem.
-   **Validação:** script automatizado antes da etapa de publicação.
-   **Revisão:** pull request para mudanças relevantes na linha de base
    ou dependências.
