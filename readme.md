# Integração Simple de API Flask

## Passo a passo para iniciar o projeto e implementar as soluções do Processamento de Dados e disponibilização da API

### 1. Criando ambiente virtual e instalando dependencias

O primeiro passo é criar um ambiente virtual para importar todas as bibliotecas e executar os scripts
 - Crie um novo ambiente virtual executando o código: `python3 -m venv venv`

Abra o ambiente virtual para que possamos instalar as bibliotecas externas.
 - Execute: `source venv/bin/activate`

Insta-le as bibliotecas externas.
 - Execute: `pip install -r requirements.txt`


### 2. Executando scripts do Processamento de Dados

Agora com os requisitos mínimos vamos iniciar o Processamento de Dados.
O Processamento de Dados é responsável pela construção de algumas tabelas essenciais assim como a população dessas tabelas.

Mude para o diretório de processamento de dados.
 - Execute: `cd pipeline_process`

Vamos executar o primeiro Script para que possamos popular a tabela `state_municipality`.
 - Excute: `python3 process_state_municipality.py`

Agora vamos para o segundo Script, o qual é responsável por popular as tabelas `harvest_area` e `production`, assim como criar a view `productivity`.
 - Execute: `python3 process_harvest_production.py`

### 3. Disponbilizando APIs

Agora com todos os ETLs já executados, tabelas populadas, views construídas estamos preparados para disponibilizar o acesso aos nossos cliente via nossa API.

Mude para o diretório de APIs.
 - Execute: `cd ../apis_system_integration`

Suba a API Harvest Production.
 - Execute: `python3 api_harvest_production.py`

Parece que está tudo pronto. Vamos acessar alguns endpoints e realizar algumas consultas.

### 4. Acessando endpoints

Esses são os endpoints disponbilizamos pela nossa API:
  - Path: `/`
    - Descrição: Esse endpoint retorna quais são os paths disponíveis da nossa api.
    - Método: `GET`
  - Path: `/harvested_area?year={year}&municipality_id={id}`
    - Descrição: Esse endpoint retorna o valor de uma área colhida de um município de um ano.
    - Método: `GET`
  - Path: `/productivity?year={year}&state_uf={state}`
    - Descrição: Esse endpoint retorna o(s) valor(es) de produtividade de um ou mais estados brasileiros de um ano.
    - Método: `GET`
  - Path: `/produced_quantity?year={year}&municipality_id={id}`
    - Descrição: Esse endpoint retorna o(s) valor(es) de quantidade produzida de um ou mais municípios de um ou mais anos.
    - Método: `GET`

Vamos pegar a área colhida do município Alta Floresta D'Oeste que fica em Rondônia.
 - Abra a url: http://127.0.0.1:5000/harvested_area?year=2018&municipality_id=1100015

Agora vamos ver a produtividade dos estados do Pará e Amazonas no ano de 2019.
 - Abra a url: http://127.0.0.1:5000/productivity?year=2019&state_uf=AM&state_uf=PA

Vamos selecionar também a quantidade produzida para os anos de 2018 e 2019 dos municípios de Alta Floresta D'Oeste, estado de Rondônia, e Belterra, estado do Pará.
 - Abra a url: http://127.0.0.1:5000/produced_quantity?year=2018&year=2019&municipality_id=1100015&municipality_id=1501451

Nossa última, porém não menos importante url será para verificar o limite de requisição devido ao pacote do cliente.
 - Abra a url: http://127.0.0.1:5000/produced_quantity?year=2018&year=2019&year=2020&year=2021&year=2022&year=2023&municipality_id=1100015&municipality_id=1501451&municipality_id=1501600&municipality_id=1201709&municipality_id=1501725&municipality_id=1501758&municipality_id=1501782&municipality_id=1501808&municipality_id=1501907&municipality_id=1501956&municipality_id=1502004&municipality_id=1502103&municipality_id=1502152&municipality_id=1502202&municipality_id=1502301&municipality_id=1502400&municipality_id=1502509&municipality_id=1502608

 Perfeito!

 Concluímos todas as etapas!

 Muito obrigado!
