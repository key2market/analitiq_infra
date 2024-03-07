FROM node:18-alpine as build-stage
WORKDIR /app
COPY package.json .
RUN npm install
COPY . .
# Use the build argument to set the environment variable
ARG FASTAPI_HOST
ENV VITE_SERVER_ADRESS=${FASTAPI_HOST}
RUN npm run build

FROM nginx:alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build-stage /app/dist .
COPY --from=build-stage /app/src/nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]
