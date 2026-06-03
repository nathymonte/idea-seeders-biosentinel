# BioSentinel

Plataforma web de monitoramento de áreas de reserva ambiental com base em dados de satélite e sensores IoT simulados.

---

## Visão geral

O **BioSentinel** é um protótipo full stack desenvolvido como projeto final do semestre com foco no desafio da indústria espacial.

A proposta da plataforma é monitorar áreas de preservação ambiental utilizando:

- dados de satélite do MapBiomas
- banco de dados geoespacial
- API REST
- frontend web interativo
- simulação de sensores IoT

O sistema permite cadastrar reservas ambientais, importar datasets geográficos e gerar análises de cobertura do solo para apoiar a identificação de:

- perda de vegetação
- expansão urbana
- alterações no uso do solo
- alertas ambientais
- monitoramento preventivo

---

## Tecnologias

### Backend

- Python 3.11
- FastAPI
- SQLAlchemy

### Banco de dados

- PostgreSQL
- PostGIS

### Frontend

- React

### Geoprocessamento

- Rasterio
- GeoPandas
- Shapely

### Infraestrutura

- Docker
- Docker Compose

### Fonte de dados

- MapBiomas Cobertura 10m

---

## Estrutura do projeto

```text
idea-seeders-biosentinel/
│
├── backend/
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│
├── database/
│   ├── init.sql
│   └── seed.sql
│
├── data/
│
├── docs/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Modelo de negócio

O sistema possui as seguintes entidades principais:

### users

Usuários da plataforma.

Exemplo:

- administrador
- analista ambiental

### environmental_reserves

Reservas monitoradas.

Contém:

- nome
- localização
- área
- polígono geográfico

### satellite_datasets

Arquivos de satélite importados.

Exemplo:

- MapBiomas 2023

### land_cover_analysis

Resultado da análise de cobertura do solo.

Exemplo:

- floresta
- pastagem
- área urbana

### alerts

Alertas ambientais.

Exemplo:

- perda de vegetação
- risco de incêndio

### iot_sensor_readings

Leituras de sensores simulados.

Exemplo:

- temperatura
- umidade
- fumaça

---

## Relacionamentos

```text
users
 1 ───── N environmental_reserves

environmental_reserves
 1 ───── N land_cover_analysis

satellite_datasets
 1 ───── N land_cover_analysis

environmental_reserves
 1 ───── N alerts

environmental_reserves
 1 ───── N iot_sensor_readings
```

---

## Como rodar localmente

### 1. Clonar o repositório

```bash
git clone <url-do-repo>
cd idea-seeders-biosentinel
```

---

### 2. Criar ambiente virtual

Windows PowerShell:

```powershell
python -m venv backend/.venv
```

Ativar:

```powershell
.\backend\.venv\Scripts\Activate.ps1
```

---

### 3. Instalar dependências

```bash
pip install -r backend/requirements.txt
```

---

### 4. Subir PostgreSQL + PostGIS

```bash
docker compose up -d
```

Verificar:

```bash
docker ps
```

---

### 5. Entrar no PostgreSQL

```bash
docker exec -it biosentinel-db psql -U biosentinel -d biosentinel
```

---

### 6. Verificar tabelas

Dentro do PostgreSQL:

```sql
\dt public.*
```

---

### 7. Popular com dados de exemplo

```bash
docker exec -i biosentinel-db psql -U biosentinel -d biosentinel < database/seed.sql
```

---

### 8. Rodar backend

```bash
uvicorn backend.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

API raiz:

```text
http://127.0.0.1:8000/
```

---

## Docker útil

Parar containers:

```bash
docker compose down
```

Recriar do zero:

```bash
docker compose down -v
docker compose up -d
```

Ver logs:

```bash
docker logs biosentinel-db
```
## PostgreSQL / PostGIS

### Abrir o terminal do PostgreSQL (psql)

```bash
docker exec -it biosentinel-db psql -U biosentinel -d biosentinel
```

---

### Comandos úteis dentro do psql

Listar tabelas:

```sql
\dt public.*
```

Descrever uma tabela:

```sql
\d environmental_reserves
```

Consultar dados:

```sql
SELECT * FROM users;
```

Ativar modo expandido (melhor visualização):

```sql
\x on
```

Sair do PostgreSQL:

```sql
\q
```

---

### Executar um arquivo SQL

#### PowerShell

```powershell
Get-Content .\database\seed.sql |
docker exec -i biosentinel-db psql -U biosentinel -d biosentinel
```

#### CMD

```cmd
docker exec -i biosentinel-db psql -U biosentinel -d biosentinel < database\seed.sql
```

---

### Reinicializar completamente o banco

Remove o container e o volume do PostgreSQL:

```bash
docker compose down -v
```

Subir novamente:

```bash
docker compose up -d
```

Depois reaplicar os dados de exemplo:

```powershell
Get-Content .\database\seed.sql |
docker exec -i biosentinel-db psql -U biosentinel -d biosentinel
```

---

### Verificar containers em execução

```bash
docker ps
```

---

### Ver logs do PostgreSQL

```bash
docker logs biosentinel-db
```