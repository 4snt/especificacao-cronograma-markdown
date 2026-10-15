# CI e publicação estática

## 1. Objetivo

Validar os arquivos do cronograma, gerar os artefatos de visualização e
publicar uma página estática sem banco de dados ou backend.

## 2. Fluxo de CI

1.  Disparar em pull request e em push para a branch principal.
2.  Fazer checkout do repositório.
3.  Instalar uma versão fixada das ferramentas de geração.
4.  Validar o esquema dos arquivos Markdown.
5.  Validar IDs duplicados, datas, status, percentuais e dependências.
6.  Detectar ciclos no grafo de dependências.
7.  Gerar a página HTML, Gantt e tabela alternativa.
8.  Em pull request, executar validações sem publicar.
9.  Na branch principal, publicar os artefatos estáticos.
10. Registrar data/hora da geração e versão do commit.

## 3. Artefatos

-   página inicial com resumo do cronograma;
-   gráfico de Gantt;
-   tabela acessível com atividades e datas;
-   lista de marcos;
-   legenda de estados;
-   informação de última atualização e commit de origem.

## 4. Critérios de falha

A CI deve falhar antes da publicação se encontrar: - campo obrigatório
ausente; - ID repetido; - data malformada; - fim anterior ao início; -
progresso fora do intervalo de 0 a 100; - estado não reconhecido; -
dependência apontando para ID inexistente; - dependência circular; -
marco com intervalo de datas inválido.

A mensagem de erro deve apontar o arquivo e o campo sempre que possível.

## 5. Hospedagem

Preferência inicial: GitHub Pages, se o projeto estiver hospedado no
GitHub. Como alternativa, qualquer serviço de hospedagem estática capaz
de publicar os arquivos gerados atende à arquitetura.

A configuração do repositório deve habilitar a publicação por CI e
conceder somente as permissões mínimas necessárias. Não inserir tokens
pessoais nos arquivos Markdown nem no histórico do Git.

## 6. Estratégia de implementação

A implementação pode usar um script pequeno para ler front matter,
validar os dados e gerar HTML com Mermaid Gantt ou outra biblioteca de
visualização estática. A escolha da biblioteca é decisão técnica
posterior; o formato de entrada deve permanecer independente dela.

Se Mermaid for utilizado, validar as limitações de sintaxe e a forma
como o renderer trata dependências, datas e progresso. Manter a tabela
textual como alternativa obrigatória.

## 7. Definição de pronto da pipeline

-   CI executa sem intervenção manual.
-   Dados inválidos bloqueiam a publicação.
-   Pull requests mostram falhas de validação.
-   A branch principal publica a versão mais recente.
-   A página publicada não depende de API ou banco.
-   A geração pode ser reproduzida localmente seguindo a documentação.
