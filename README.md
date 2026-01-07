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

- Node.js 20+

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

O frontend roda localmente e se conecta ao backend já deployado na AWS.

## Deploy para AWS

### Deploy Automático (CI/CD)

O projeto possui CI/CD configurado via GitHub Actions.

Configurar Secrets no GitHub:
1. Vá em Settings → Secrets and variables → Actions
2. Adicione as seguintes secrets:
   - AWS_ACCESS_KEY_ID: Sua chave de acesso AWS (ex: AKIAIOSFODNN7EXAMPLE)
   - AWS_SECRET_ACCESS_KEY: Sua chave secreta AWS (ex: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY)
   - JWT_SECRET_KEY: Chave secreta para JWT (mínimo 32 caracteres)
   - AWS_DEFAULT_REGION: us-east-1 (opcional, padrão é us-east-1)

Importante ao configurar as secrets:
- NÃO inclua espaços antes ou depois dos valores
- NÃO inclua aspas ao redor dos valores
- Copie e cole os valores exatamente como aparecem no AWS IAM
- Verifique se não há caracteres invisíveis ou quebras de linha

Deploy automático:
- Push para main/master → Deploy automático para dev
- Ou use "Run workflow" manualmente no GitHub Actions

### Deploy Manual

Configurar credenciais AWS:
```bash
export AWS_ACCESS_KEY_ID=sua-chave
export AWS_SECRET_ACCESS_KEY=sua-chave-secreta
export AWS_DEFAULT_REGION=us-east-1
export JWT_SECRET_KEY=sua-chave-jwt-secreta-minimo-32-caracteres
```

Fazer deploy:
```bash
cd backend
serverless deploy --stage dev
```

## Endpoints da API

Base URL: https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev

### POST /auth/login

Autentica um usuário e retorna um token JWT.

**Exemplo de chamada:**
```bash
curl -X POST https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"sua-senha"}'
```

**Request:**
```json
{
  "username": "admin",
  "password": "sua-senha"
}
```

**Response 200:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "user_id": "admin",
    "username": "admin"
  }
}
```

**Response 401:**
```json
{
  "error": "Invalid credentials"
}
```

### POST /convert

Converte um valor de uma moeda para outra. Requer autenticação.

**Exemplo de chamada:**
```bash
curl -X POST https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/convert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -d '{"amount":100,"from":"USD","to":"BRL"}'
```

**Headers:**
```
Authorization: Bearer {token_jwt}
Content-Type: application/json
```

**Request:**
```json
{
  "amount": 100,
  "from": "USD",
  "to": "BRL"
}
```

**Response 200:**
```json
{
  "amount": 100,
  "from": "USD",
  "to": "BRL",
  "rate": 5.2,
  "converted_amount": 520.0
}
```

**Response 400:**
```json
{
  "error": "Invalid currency. Must be one of: USD, BRL, EUR, GBP, JPY."
}
```

**Response 401:**
```json
{
  "error": "Authorization token required"
}
```

### GET /health

Verifica o status da API. Requer autenticação.

**Exemplo de chamada:**
```bash
curl -X GET https://kb9t8qu7ni.execute-api.us-east-1.amazonaws.com/dev/health \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Headers:**
```
Authorization: Bearer {token_jwt}
```

**Response 200:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-01T00:00:00.000000",
  "service": "liquid-api"
}
```

**Response 401:**
```json
{
  "error": "Authorization token required"
}
```

## Moedas Suportadas

USD, BRL, EUR, GBP, JPY

## Testes

Backend:
```bash
cd backend
pytest
```

Frontend:
```bash
cd frontend
npm test
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
