# Status do projeto

Arquitetura em ajuste: as tasks e suas datas ficam no GitHub Project v2. Este repositório mantém apenas o gerador do Gantt e a documentação; o workflow consulta o Project via GraphQL e publica o HTML no GitHub Pages.

Antes de publicar, configure `PROJECT_OWNER`, `PROJECT_NUMBER` e o secret `PROJECTS_TOKEN`, crie no Project os campos de data configurados e habilite Pages para GitHub Actions. O Pages está configurado com origem "GitHub Actions"; itens sem datas aparecem numa lista à parte até serem preenchidos.
