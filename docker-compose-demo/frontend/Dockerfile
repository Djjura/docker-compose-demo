FROM node:18-alpine

WORKDIR /app

COPY package.json ./
RUN npm install

COPY public ./public
COPY src ./src

RUN npm install react-scripts

EXPOSE 3000

CMD ["npm", "start"]
