# frontend/Dockerfile

# 1. Usar Node.js
FROM node:22-alpine

# 2. Pasta de trabalho
WORKDIR /app

# 3. Copia os arquivos de dependências
COPY package.json package-lock.json ./

# 4. Instala as dependências
RUN npm install

# 5. Copia o resto do código
COPY . .

# 6. Expõe a porta do Vite
EXPOSE 5173

# 7. Roda em modo desenvolvimento (para o Alpha é mais fácil agora)
# Em produção real faríamos o "build", mas vamos simplificar
CMD ["npm", "run", "dev", "--", "--host"]