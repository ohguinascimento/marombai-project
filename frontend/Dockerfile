# --- ESTÁGIO 1: Build ---
FROM node:20-alpine AS build-stage
WORKDIR /app

# Define o argumento de build para a URL da API
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copia apenas os arquivos de dependências primeiro para aproveitar o cache do Docker
COPY package*.json ./
RUN npm install

# Copia o restante do código e gera o build de produção
COPY . .
RUN npm run build

# --- ESTÁGIO 2: Produção ---
# Usamos Nginx para servir os arquivos estáticos de forma ultra-rápida
FROM nginx:stable-alpine AS production-stage

# Copia a configuração personalizada do Nginx para suportar SPA Routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copia os arquivos compilados do estágio anterior
COPY --from=build-stage /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]