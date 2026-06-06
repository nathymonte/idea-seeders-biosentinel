# BioSentinel

BioSentinel é uma plataforma de monitoramento ambiental baseada em dados de satélite do MapBiomas, desenvolvida como projeto acadêmico para a disciplina de Engenharia de Software.

O sistema permite visualizar reservas ambientais, analisar a cobertura do solo e gerar relatórios ambientais utilizando dados geoespaciais armazenados em PostgreSQL/PostGIS.

---

## Tecnologias Utilizadas

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL + PostGIS

### Frontend

- React
- Vite
- React Router
- React Leaflet
- Recharts

### Infraestrutura

- Docker
- Docker Compose

---

## Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd idea-seeders-biosentinel
```

---

### 2. Subir o banco de dados

```bash
docker compose up -d
```

O banco será criado automaticamente utilizando:

- `backend/database/init.sql`
- `backend/database/seed.sql`

Não é necessário executar scripts manualmente.

---

### 3. Executar o Backend

Criar ambiente virtual:

```bash
cd backend

python -m venv .venv
```

Ativar o ambiente virtual:

#### Windows

```bash
.venv\Scripts\activate
```

Instalar dependências:

```bash
pip install -r requirements.txt
```

Executar a API:

```bash
uvicorn backend.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

### 4. Executar o Frontend

Em outro terminal:

```bash
cd frontend

npm install

npm run dev
```

Aplicação:

```text
http://localhost:5173
```

---

## Credenciais de Demonstração

Usuário:

```text
admin@biosentinel.com
```

Senha:

```text
Admin1234
```

---

## Reservas Disponíveis

O banco já é carregado com três reservas de demonstração:

- Reserva Cantareira Demo
- Reserva Amazônia Demo
- Reserva Pantanal Demo

As análises ambientais já estão persistidas no banco e podem ser visualizadas imediatamente após iniciar o sistema.

---

## Reiniciar Ambiente do Zero

Caso seja necessário recriar completamente o banco:

```bash
docker compose down -v

docker compose up -d
```

---

## Acesso às Funcionalidades

### Login

```text
/login
```

### Dashboard de Monitoramento

```text
/map
```

### Relatórios Ambientais

```text
/report/{id}
```

Exemplos:

```text
/report/1
/report/2
/report/3
```

---

## Observação

O arquivo GeoTIFF original do MapBiomas não é distribuído junto ao projeto devido ao seu tamanho.

As análises utilizadas na demonstração já estão armazenadas no banco através do script `seed.sql`, permitindo a execução completa do sistema sem a necessidade do arquivo raster original.