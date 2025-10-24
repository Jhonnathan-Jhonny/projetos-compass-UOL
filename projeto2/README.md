# Leitor de RSS com Node.js e AWS S3 - Squad 6

API Node.js que consome um feed RSS, armazena os dados em um arquivo `data.json` no AWS S3 e exibe as informações em uma página HTML. Na inicialização do servidor, o endpoint `GET /rss/api/feed` gera e salva o `data.json` no S3, e o `GET /rss/data` recupera os dados para o frontend.

## Membros

- David Nobrega Rodrigues
- Jhonnathan Jhonny Rufino Rodrigues
- Lucas de Medeiros Trindade
- Maria Beatriz Targino De Azevedo Silva

## Objetivo

- Consumir o feed RSS do [Jornal da Ciência](https://jcnoticias.jornaldaciencia.org.br/feed/).
- Gerar `data.json` com até 5 notícias (título, link, resumo, data).
- Armazenar o `data.json` no AWS S3.
- Exibir os dados do S3 em uma página HTML sem interação manual.

## Tecnologias

- Node.js: Plataforma da API.
- Express: Framework para rotas e servidor.
- rss-parser: Parsing do feed RSS.
- @aws-sdk/client-s3: Integração com AWS S3.
- HTML/CSS/JavaScript: Frontend (`index.html`, `style.css`, `script.js`).
- Docker: Conteinerização.

## Estrutura do Projeto
```bash
/ 
├── src/
│   ├── controllers/
│   │   └── rssController.js  # Lógica da API
│   ├── routes/
│   │   └── rss.routes.js     # Rotas da API
│   ├── services/
│   │   └── s3Service.js      # Integração S3
│   ├── templates/
│   │   └── index.html        # Página HTML do frontend
│   │   └── script.js         # Lógica do frontend
│   │   └── style.css         # Estilização do frontend
├── .gitignore
├── index.js
├── package.json
├── package-lock.json
└── README.md
```

## Como Executar

### Requisitos

- Node.js (v16+)
- Docker
- Git
- Conta AWS com bucket S3 configurado
- IDE (ex.: VS Code)

### Configuração

1. Clone o repositório:
   ```bash
   git clone https://github.com/Compass-pb-aws-2025-MAIO/sprints-2-3-pb-aws-maio.git
   cd sprints-2-3-pb-aws-maio
   ```
2. Crie o arquivo .env na raiz:
    ```plaintext
    AWS_REGION=us-west-2
    AWS_BUCKET_NAME=nome-do-seu-bucket
    AWS_ACCESS_KEY_ID=sua-chave
    AWS_SECRET_ACCESS_KEY=sua-chave-secreta
    Substitua pelos valores corretos do AWS S3.
    ```

#### Execução Local

1. instale as dependências:
    ```bash
    npm install
    ```
2. Inicie o servidor:
    ```bash
    node index.js
    ```
    - o servidor roda na porta 80
    - Acesse: http://localhost:80

#### Execução com docker:

1. Construa a imagem:
    ```bash
    docker build -t <nome_da_imagem>
    ```
2. Exxecute a imagem em um conteiner:
    ```bash
    docker run -dp 80:80 <nome_da_imagem>
    ```


## Dificuldades Encontradas
- Aprendizado e aplicação do Node.js no contexto do projeto.
- Configuração e utilização do Docker para conteinerização.
- Compreensão e desenvolvimento de uma API funcional.