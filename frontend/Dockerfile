


# Stage 1: Build stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the React app for production
RUN npm run build

# Stage 2: Production stage with Nginx
FROM nginx:alpine

# Copy custom nginx configuration file
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy built files from build stage to Nginx html directory
COPY --from=build /app/build /usr/share/nginx/html

# Set environment variable for API URL (used in the React app)
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Expose port 80
EXPOSE 80


