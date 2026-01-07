# Liquid - API de Conversão de Moedas

API REST para conversão de moedas desenvolvida com Python (AWS Lambda) e frontend em Next.js/React.

## Descrição

API de conversão de moedas com autenticação JWT, cache de taxas no DynamoDB e integração com API externa de taxas de câmbio.

Arquitetura:
- Backend: Python 3.11 + AWS Lambda (Serverless Framework)
- Frontend: Next.js 16 + React 19 + TypeScript
- Banco de Dados: AWS DynamoDB
- Autenticação: JWT (JSON Web Tokens)
- Deploy: AWS API Gateway + Lambda

## Como Rodar Localmente

### Pré-requisitos

- Python 3.11+
- Node.js 20+
- AWS CLI configurado
- Conta AWS com permissões adequadas

### Backend

Instalar dependências:
```bash
cd backend
npm install
pip install -r requirements.txt
```

Configurar variáveis de ambiente:
```bash
cp ../.env.example ../.env
```

Executar testes:
```bash
pytest
```

### Frontend

Instalar dependências:
```bash
cd frontend
npm install
```

Configurar variável de ambiente:
```bash
echo "NEXT_PUBLIC_API_URL=https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev" > .env.local
```

Executar em desenvolvimento:
```bash
npm run dev
```

Acessar: http://localhost:3000

## Deploy para AWS

### Deploy Automático (CI/CD)

O projeto possui CI/CD configurado via GitHub Actions.

Configurar Secrets no GitHub:
1. Vá em Settings → Secrets and variables → Actions
2. Adicione as seguintes secrets (Esses dados eu passo no privado):
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - JWT_SECRET_KEY
   - AWS_DEFAULT_REGION

Deploy automático:
- Push para main/master → Deploy automático para dev
- Ou use "Run workflow" manualmente no GitHub Actions

### Deploy Manual

Configurar credenciais AWS:
```bash
export AWS_ACCESS_KEY_ID=sua-chave
export AWS_SECRET_ACCESS_KEY=sua-chave-secreta
export AWS_DEFAULT_REGION=us-east-1
```

Configurar variáveis de ambiente:
```bash
export JWT_SECRET_KEY=sua-chave-jwt-secreta-minimo-32-caracteres
export EXCHANGE_RATE_API_URL=https://api.exchangerate-api.com/v4/latest
export ALLOWED_ORIGIN=https://seu-dominio.com
```

Fazer deploy:
```bash
cd backend
serverless deploy --stage dev
serverless deploy --stage prod
```

Verificar endpoints:
```bash
serverless info --stage dev
```

## Endpoints da API

Base URL: https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev

### POST /auth/login

Autentica um usuário e retorna um token JWT.

Request:
```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

Response 200:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "admin",
    "username": "admin"
  }
}
```

Response 401:
```json
{
  "error": "Invalid credentials"
}
```

Exemplo cURL:
```bash
curl -X POST https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}'
```

### POST /convert

Converte um valor de uma moeda para outra. Requer autenticação.

Headers:
```
Authorization: Bearer {token_jwt}
Content-Type: application/json
```

Request:
```json
{
  "amount": 100,
  "from": "USD",
  "to": "BRL"
}
```

Response 200:
```json
{
  "amount": 100,
  "from": "USD",
  "to": "BRL",
  "rate": 5.2,
  "converted_amount": 520.0
}
```

Response 400:
```json
{
  "error": "Invalid currency. Must be one of: USD, BRL, EUR, GBP, JPY."
}
```

Response 401:
```json
{
  "error": "Authorization token required"
}
```

Exemplo cURL:
```bash
curl -X POST https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"amount":100,"from":"USD","to":"BRL"}'
```

### GET /health

Verifica o status da API. Requer autenticação.

Headers:
```
Authorization: Bearer {token_jwt}
```

Response 200:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00.000000",
  "service": "liquid-api"
}
```

Exemplo cURL:
```bash
curl -X GET https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/health \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## Moedas Suportadas

Por padrão: USD, BRL, EUR, GBP, JPY


## Variáveis de Ambiente

Consulte o arquivo .env.example na raiz do projeto para ver todas as variáveis disponíveis.

Variáveis obrigatórias em produção:
- JWT_SECRET_KEY - Chave secreta para JWT (mínimo 32 caracteres)
- AWS_ACCESS_KEY_ID - Credenciais AWS
- AWS_SECRET_ACCESS_KEY - Credenciais AWS

## Testes

Backend:
```bash
cd backend
pytest
pytest --cov=. --cov-report=html
```

Frontend:
```bash
cd frontend
npm test
npm run test:coverage
```

## Tecnologias

Backend: Python 3.11, AWS Lambda + Gateway API, DynamoDB, Serverless Framework
Frontend: Next.js 16, React 19, TypeScript, Tailwind CSS
Autenticação: JWT, bcrypt
Testes: pytest, Jest, Testing Library
CI/CD: GitHub Actions

## Autor

Danilo Salve
danilo.salve@codenity.com.br
