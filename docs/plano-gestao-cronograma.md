# Plano de Gestão do Cronograma

## 1. Finalidade

Definir como a equipe irá planejar, estimar, sequenciar, aprovar,
acompanhar e comunicar o cronograma. Este documento é a especificação de
processo do responsável pelo Plano de Gestão do Cronograma, no recorte
do Domínio 3 --- Cronograma.

## 2. Abordagem

Usar planejamento predominantemente preditivo para representar a
sequência de atividades e marcos, com atualização incremental conforme a
equipe aprende e executa o trabalho. A abordagem pode ser ajustada se o
tipo de projeto exigir ciclos adaptativos.

O Gantt é uma visualização de comunicação e análise; não substitui
conversas da equipe nem a validação das estimativas.

## 3. Processo de elaboração

1.  Identificar entregas e decompor o trabalho em atividades
    gerenciáveis, respeitando o escopo acordado.
2.  Definir o resultado verificável de cada atividade.
3.  Estimar duração considerando esforço, disponibilidade, incerteza e
    dependências.
4.  Sequenciar as atividades e registrar predecessoras.
5.  Identificar marcos de decisão, revisão e entrega.
6.  Construir o cronograma inicial e verificar se a data final é
    plausível.
7.  Revisar com os integrantes e registrar as premissas.
8.  Aprovar e identificar a linha de base.
9.  Acompanhar o realizado e atualizar previsões com justificativas.
10. Comunicar impactos e solicitar aprovação quando houver mudança
    relevante.

## 4. Estimativas

-   Toda estimativa deve ter unidade explícita (por exemplo, dias
    corridos ou dias úteis).
-   Quando houver incerteza relevante, registrar premissa e/ou intervalo
    estimado em vez de sugerir precisão falsa.
-   Estimar com participação de quem executará a atividade, sempre que
    possível.
-   Revisar estimativas diante de informação nova, sem apagar o
    histórico da decisão.

## 5. Dependências

Registrar dependências lógicas e justificáveis. Para o MVP, recomenda-se
começar com dependência término-início (FS: uma tarefa começa depois de
terminar a predecessora). Dependências mais avançadas e defasagens podem
ficar para versões futuras.

Não usar dependência apenas para forçar uma data desejada. Se duas
tarefas podem ocorrer em paralelo, não criar uma relação artificial.

## 6. Linha de base e mudanças

A linha de base é a versão do cronograma aprovada para comparação. Ela
deve registrar pelo menos identificador/versão, data de aprovação,
início e fim planejados, marcos e premissas.

Uma mudança relevante deve indicar: - o que mudou; - motivo; -
atividades e marcos afetados; - impacto na data final e em outras
dependências; - quem revisou/aprovou; - data da decisão.

A linha de base deve ser preservada em campos específicos ou registrada
no histórico de decisões do Project. Não sobrescrever silenciosamente a
linha de base durante atualizações rotineiras.

## 7. Acompanhamento e previsão

Em uma cadência combinada pela equipe, revisar: - tarefas concluídas, em
andamento, bloqueadas e não iniciadas; - datas planejadas versus datas
reais; - marcos próximos; - dependências bloqueadas; - desvios e
previsão de conclusão; - ações corretivas ou replanejamento necessário.

O percentual concluído deve ser usado com critério: uma tarefa pode
permanecer em 0% por algum tempo e depois ser concluída; não inferir
automaticamente o progresso a partir do tempo decorrido.

## 8. Comunicação

O GitHub Project é a referência compartilhada para o cronograma atual. O
repositório gera e publica a visualização estática. Mudanças
significativas devem ser comunicadas no canal da equipe e registradas no
histórico do Project. O Gantt deve ser acompanhado por uma tabela legível
e indicação da data da última geração.

## 9. Papéis

-   **Responsável pelo cronograma:** mantém este plano, valida
    consistência, prepara a linha de base e consolida previsões.
-   **Responsáveis pelas atividades:** fornecem estimativas, atualizam
    andamento e sinalizam impedimentos.
-   **Equipe:** revisa sequência, dependências e viabilidade.
-   **Professor/partes interessadas:** recebem a visualização e fornecem
    feedback conforme combinado.

Os nomes e a distribuição final das tarefas devem ser confirmados pelo
grupo. A lista de participantes informada para o Domínio 3 é: Alan Lima,
Juan Pablo, Pávila Miranda, Janaina Alves, Hudson Junior e Murilo
Escobedo.

## 10. Indicadores mínimos

-   quantidade de atividades por estado;
-   marcos planejados e realizados;
-   tarefas atrasadas, quando datas reais/estado estiverem disponíveis;
-   diferença entre data final da linha de base e previsão atual;
-   dependências bloqueadas.

Não apresentar indicadores que os dados disponíveis não permitam
calcular de forma confiável.
