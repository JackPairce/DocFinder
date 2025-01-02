FROM node:20-alpine AS base

WORKDIR /usr/src/app

RUN apk add --no-cache git

RUN git clone https://github.com/AimenSayoud/book_library.git .

RUN npm install

RUN npm run build

RUN npm prune --production

FROM node:20-alpine AS production

WORKDIR /usr/src/app

COPY --from=base /usr/src/app/package.json .
COPY --from=base /usr/src/app/.next ./.next
COPY --from=base /usr/src/app/node_modules ./node_modules
COPY --from=base /usr/src/app/next.config.mjs ./next.config.mjs

ARG BACKEND_URL

ENV BACKEND_URL=$BACKEND_URL

EXPOSE 3000

CMD ["npm", "run", "start"]