# Exemplo de cronograma inicial

> **Atenção:** este cronograma é apenas um exemplo técnico para testar o
> formato. Não representa datas aprovadas nem atribui compromissos reais
> aos integrantes.

  -------------------------------------------------------------------------------------------
  ID         Atividade      Início       Fim          Responsável   Dependências   Estado
                                                      sugerido                     
  ---------- -------------- ------------ ------------ ------------- -------------- ----------
  T-001      Levantar       2026-10-19   2026-10-20   Equipe        ---            Não
             requisitos e                                                          iniciada
             premissas                                                             

  T-002      Definir        2026-10-21   2026-10-22   Responsável   T-001          Não
             formato dos                              técnico                      iniciada
             dados                                                                 

  M-001      Aprovar linha  2026-10-23   2026-10-23   Equipe        T-001, T-002   Marco
             de base                                                               

  T-003      Implementar    2026-10-26   2026-10-29   Responsável   M-001          Não
             validação e                              técnico                      iniciada
             geração                                                               

  T-004      Configurar CI  2026-10-30   2026-11-02   Responsável   T-003          Não
             e publicação                             técnico                      iniciada

  T-005      Validar Gantt  2026-11-03   2026-11-04   Equipe        T-004          Não
             e documentação                                                        iniciada

  M-002      Apresentação   2026-11-05   2026-11-05   Equipe        T-005          Marco
             da solução                                                            
  -------------------------------------------------------------------------------------------

## Pendências antes de aprovar

-   Confirmar escopo e entregáveis do trabalho da disciplina.
-   Confirmar disponibilidade e responsáveis por atividade.
-   Rever estimativas e calendário acadêmico.
-   Validar a sequência e as dependências.
-   Aprovar a linha de base com o grupo.
