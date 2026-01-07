# Liquid Backend API

API REST serverless para conversão de moedas usando AWS Lambda e DynamoDB.

## Deploy Local

Pré-requisitos:
- Python 3.11+
- Node.js 20+
- AWS CLI configurado
- Serverless Framework instalado globalmente

Instalar dependências:
```bash
npm install
pip install -r requirements.txt
```

Configurar variáveis de ambiente:
```bash
cp ../.env.example ../.env
export AWS_ACCESS_KEY_ID=sua-chave
export AWS_SECRET_ACCESS_KEY=sua-chave-secreta
export JWT_SECRET_KEY=sua-chave-jwt-minimo-32-caracteres
```

Executar testes:
```bash
pytest
```

Deploy para AWS:
```bash
serverless deploy --stage dev
```

## Deploy para AWS

Deploy Manual:
```bash
export AWS_ACCESS_KEY_ID=sua-chave
export AWS_SECRET_ACCESS_KEY=sua-chave-secreta
export JWT_SECRET_KEY=sua-chave-jwt-secreta
serverless deploy --stage dev
```

Deploy via CI/CD:
O deploy automático é feito via GitHub Actions quando há push para main/master.

## Endpoints

- POST /auth/login - Autenticação
- POST /convert - Conversão de moedas (requer autenticação)
- GET /health - Health check (requer autenticação)

## Configuração

Consulte serverless.yml e .env.example para configurações detalhadas.
