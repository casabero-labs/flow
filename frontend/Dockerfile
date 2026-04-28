FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
RUN apk add --no-cache gettext

COPY --from=builder /app/dist /usr/share/nginx/html
# Use a fixed nginx.conf with Docker network IP
COPY nginx.conf /etc/nginx/conf.d/default.conf
