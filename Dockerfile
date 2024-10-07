# Stage 1: Install dependencies and build the app
FROM node:lts-alpine AS build
WORKDIR /app

# Copy only package.json and package-lock.json for better caching
COPY package*.json ./

# Install dependencies
RUN npm ci --omit=dev

# Copy the rest of the application source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Create a minimal runtime image
FROM nginx:alpine-slim AS runtime

# Copy Nginx configuration
COPY ./nginx.conf /etc/nginx/nginx.conf

# Copy the built app from the build stage to the nginx container
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 8080
EXPOSE 8080
