FROM node:20-alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN chmod +x node_modules/.bin/* || true

EXPOSE 3000

CMD ["npm", "run", "dev"]
