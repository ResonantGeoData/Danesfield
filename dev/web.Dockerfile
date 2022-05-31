FROM node:16

COPY client/package*.json /opt/vue-project/
COPY client/yarn.lock /opt/vue-project/

RUN yarn

EXPOSE 8080

WORKDIR /opt/vue-project

CMD ["yarn", "run", "serve"]
