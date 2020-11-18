FROM node:lts-stretch-slim as builder

RUN mkdir /qmyz-frontend
WORKDIR /qmyz-frontend

RUN npm install vue -g
COPY package.json /qmyz-frontend
RUN npm install

ADD . /qmyz-frontend
RUN npm run build

FROM nginx:alpine
COPY ./qmyz-frontend.conf /etc/nginx/conf.d/qmyz-frontend.conf
COPY --from=builder /qmyz-frontend/dist/ /qmyz-frontend-dist/

EXPOSE 8080
