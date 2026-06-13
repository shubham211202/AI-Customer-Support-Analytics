# Stage 1: Build
FROM node:20-alpine AS build

WORKDIR /app

# Copy package.json and package-lock.json first to cache dependencies
COPY package*.json ./

RUN npm ci

# Copy the rest of the frontend source
COPY . .

# Build the frontend assets (Vite generates optimized production build in dist/)
RUN npm run build

# Stage 2: Serve
FROM nginx:1.25-alpine

# Remove the default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy static assets from build stage to nginx html folder
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
