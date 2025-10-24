# Etapa 1: base da imagem com Node.js
FROM node

# Diretório de trabalho dentro do container
WORKDIR /

# Copia os arquivos de dependência
COPY package*.json ./

# Instala as dependências do projeto
RUN npm install

# Copia o restante dos arquivos da aplicação
COPY . .

# Expõe a porta da API
EXPOSE 80

# Comando padrão para iniciar a API
CMD ["node", "index.js"]
