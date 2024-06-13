# Perguntas adicionais relacionadas com a sua proposta

## Atividade 1 - Processo de Pipeline de Dados

### 1. Você já utilizou algum orquestrador de processos? O seu processo está estruturado para ser executado automaticamente com uma periodicidade definida? Por exemplo, duas vezes por semana?

**Resposta:**
 - Conheço orquestradores de processos, já trabalhei com Apache Airflow e Databricks.
 - No momento os processos precisam ser executado manualmente, entretanto com poucos ajustes os processos construídos estariam prontos para serem executado automaticamente.
 - Os processos atualmente não estou configurados para rodar duas vezes por semana, porém com alguns ajustes isso poderia ser realizado, desde iniciar os processos com crontab (o que não é recomendado para grande escala), criar um arquivo especifico para gerenciamento de scripts ou até mesmo utilizar algo mais robusto como o Apache Airflow.


### 2. Conhece a ferramenta Airflow? Se sim, poderia nos explicar como seria possível integrar o seu processo com o Airflow?

**Resposta:**
 - Conheço o Airflow, trabalhei durante 1 ano com essa ferramenta.
 - Precisaríamos ter algumas implementações essenciais para integrar os processos ao Airflow, a primeira seria configurar o Airflow no nosso sistema e a segunda seria a adaptação dos processos (scripts) para o modelo que o Airflow opera, com DAGs e Tasks.


### 3. Muitas fontes de dados são inconsistentes. Assim, é possível que dados incompletos, “sujos”, ou até mesmo incorretos entrem no banco de dados. Poderia nos explicar um pouco sobre como lidar com estas situações?

**Resposta:**
 - Existe algumas formas de lidarmos com dados sujos. Ter bem definido o que se espera em cada campo é algo essencial, assim conseguimos trabalhar com definições que nos ajudam no tratamento dos dados. 
   - Exemplo, se uma coluna espera valores inteiros, podemos validar e apenas inserir valores inteiros nesse campo, assim podemos criar default values para quando esse padrão não é encontrado.
   - Exemplo, caso o valor que recebemos seja uma string, podemos tentar converter para inteiro. Caso falhe podemos definir como 0, nulo e em alguns casos até mesmo como a média ou mediana dos outros valores que temos no dataframe.

### 4. Se, ao invés de utilizar uma ‘view’ (requisito 2), fosse necessário utilizar uma ‘table’, sua implementação ou a sua estratégia seriam alteradas? Você tomaria alguma outra decisão no desenvolvimento?

**Resposta:**
 - Aqui poderíamos adaptar o processo que faz a criação da view para ao invés de criar uma view, criar uma tabela nova e assim popular os dados necessários nessa tabela.
 - Sim, seria tomado outra decisão no desenvolvimento. Adicionariamos etapas a mais para garantir que a nova tabela seja populada assim que as outras Tasks forem executadas.


 ## Atividade 2 – Integração de Serviços - Desenvolvimento de API

### 1. Você já hospedou algum serviço web (específico para ser usado como backend) utilizando a nuvem? 

**Resposta:**
 - Já sim. Gosto de trabalhar com a combinação MySQL e PhpMyAdmin, então esse par é costumo hospedar nos meus projetos. Assim como também adicionar o Redash para gerênciamento de queries, pequenos alertas e possbilidade de um ambiente para acesso mais analítico.

### 2. Você conhece Terraform? Se sim, poderia nos explicar como seria possível disponibilizar esta API usando o Terraform e uma “plataforma de nuvem” de sua escolha?

**Resposta:**
 - Eu conheço o Terraform, porém nunca trabalhei com o Terraform ou com processos mais robustos de DevOps.
 - No entando, seria um prazer aprender mais sobre a ferramenta e aplicar os conhecimentos em projetos dentro da Veeries.
 - Minha experiência com DevOps inclui o uso de AWS EC2, implementação de Docker com containers para executar sistemas e aplicações, e hospedagem de sites. Também trabalhei com AWS SQS, um sistema de filas.


### 3. Você conhece formas de autenticação e autorização para API? Poderia nos explicar como isso poderia ser implementado na sua proposta?

**Resposta:**

 - Conheço sim. A implementação de autenticação e autorização para a API foi um tópico que pensei muito antes de implementar a API pois estava em dúvida se utilizaria Flask, FastAPI ou Django. No final optei pela simplicidade e flexibilidade que o Framework Flask traria ao nosso projeto.
 - Claro, primeiro teríamos que adaptar a nossa API para que o acesso a ela seja autorizado para quem realizasse requests com um token válido. Os tokens poderiam ser gerados e gerênciados de diversas formas, uma forma simples seria manualmente dentro da aplicação caso poucos clientes fossem utilizar. Ou até mesmo poderíamos deixar o sistema mais robusto com usuários e ciclagem de tokens, ou seja somente usuários autorizados poderiam gerar os tokens para acessar a API e também periodicamente um novo token teria que ser emitido, melhorando a segurança na nossa aplicação.