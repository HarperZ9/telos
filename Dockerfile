FROM node:20-alpine

WORKDIR /app

COPY . .

ENV NODE_ENV=production

CMD ["node", "demo/telos-mcp.mjs"]
