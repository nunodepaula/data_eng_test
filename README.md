# data_eng_test

Teste prático consistindo na implementação de uma pipeline ETL simplificada entre dois bancos de dados, com uma API e um script ETL.

## Como rodar o projeto

### Requisitos

* Docker instalado na máquina
* Python versão 3.12

### Passo a passo

1. O primeiro passo é a criação de Virtual Environment Python, para isolar nosso ambiente de execução, então, usando python 3.12, execute o seguinte comando no terminal:

    ```powershell
    python -m venv .venv
    ```

    O nome do Virtual Environment é arbitrário, se python 3.12 não for o principal na sua máquina, utilize o caminho até ele.

2. Após a criação do Venv, ative-o:

    windows:
    ```powershell
    .\.venv\Scripts\activate
    ```
    linux:
    ```powershell
    source .venv/bin/activate
    ```

3. Para iniciar os bancos de dados, rode o seguinte comando no terminal:

    ```powershell
    docker-compose up -d
    ```

    Ao rodar esse comando, as bases de dados fonte e alvo devem iniciar-se. É possível verificar através do comando ```docker-compose ps```, obtendo algo como:

![alt text](docs/image.png)

4. Instalar as dependências do projeto. Nesse projeto, usei poetry como gestor de dependências, então recomendo utilizá-lo também, logo caso não o tenha, use pip para instalá-lo ```pip install poetry```

    Em seguida, instale as dependências do projeto usando poetry:

    ```powershell
    poetry install
    ```

5. com todas as dependências instaladas, inicie a API de comunicação à Base de dados Fonte:

    ```powershell
    uvicorn etl.api.app:app
    ```

6. Para executar o script, execute o seguinte comando na linha de comando:

    ```powershell
    etl -date 2024-10-01
    ```

    Onde o valor 2024-10-01 é apenas um exemplo. No banco de dados fonte, há dados entre 01/10/2024 e 22/10/2024. Atente para especificar a data no formato YYYY-MM-DD e apenas uma data de cada vez.

# Problema

## Sumário

O teste prático consiste na implementação de uma pipeline de ETL simplificado envolvendo dois bancos de dados (Fonte e Alvo), uma API isolando o banco de dados fonte e um script de ETL para transferir dadosde um para o outro.

Deverão ser criados dois bancos de dados, Fonte e Alvo, ambos em postgresql. O banco de dados Fonte deverá ser acessado através de uma API escrita em fastapi. O script de ETL deve acessar a API usando a biblioteca httpx e escrever os resultados no banco de dados Alvo utilizando a biblioteca sqlalchemy (e, opcionalmente, pandas).

## Banco de Dados Fonte

Criar um banco de dados postgresql. O banco deverá conter as seguintes tabelas e colunas:

  * data
    * timestamp
    * wind_speed
    * power
    * ambient_temprature

Inserir dados aleatórios nela com frequência 1-minutal e intervalo de 10 dias. Especificar na entrega do teste o período de dados contido no banco.

## Banco de Dados Alvo

Criar outro banco de dados postgresql. O banco deverá conter as seguintes tabelas e colunas:

  * signal
    * id
    * name
  * data
    * timestamp
    * signal_id
    * value

Esse banco deverá ser criado utilizando-se a biblioteca sqlalchemy. Cabe ao candidato estabelecer relações apropriadas entre as tabelas, bem como inserir dados auxiliares necessários a execução do processo de ETL.

## Conector

Criar uma API em fastapi para expor dados do banco de dados Fonte.

Deverá ser implementada uma rota que permita a consulta aos dados da tabela data, filtrados por intervalo de tempo. A rota deverá permitir a seleção de uma ou mais variáveis a serem retornadas.

A API poderá conter rotas-extras.

## ETL

Escrever um script em python para executar o processo de ETL:

  * Recebe uma data como input,
  * Consulta dados para variáveis wind_speed e power via API para o dia daquela data. O script deverá se consultar a API utilizando a biblioteca httpx.
  * Agrega o dado 10-minutal com agregações de média, mínimo, máximo e desvio padrão. A transformação de dados pode ser implementada com qualquer biblioteca, desde que ela seja executada de forma eficiente. Recomenda-se a utilização do pandas ou similar.
  * Salva o dado no banco de dados Alvo. A escrita no banco de dados deverá utilizar a biblioteca sqlalchemy para se conectar ao banco. A escrita do dado no banco pode ser feita com qualquer tecnologia, mas recomenda-se o uso do pandas em conjunto com o sqlalchemy.

## Bonus: Dagster

Orquestrar o script de ETL utilizando o dagster. Implementar:

  * Recurso para acessar banco de dados Fonte.
  * Recurso para acessar banco de dados Alvo.
  * Asset particionado diário para executar o processo de ETL.
  * Job e Schedule.
  * Essa etapa não é obrigatória.
