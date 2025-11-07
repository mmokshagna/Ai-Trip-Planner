# Stage 1: Build React app
FROM node:24-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install -g vite
RUN npm ci || npm install

COPY . .
RUN npm run build

# Stage 2: Serve with Vite (or static)
FROM node:24-alpine

WORKDIR /app
RUN npm install -g vite

COPY --from=build /app .
# EXPOSE 5173
# EXPOSE 3000
# EXPOSE 8000
# EXPOSE 4173
CMD ["npm", "run", "preview"]
#CMD ["npx", "vite", "preview", "--host", "0.0.0.0"]