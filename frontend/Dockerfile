# Use Node.js runtime as a parent image
FROM node:16-alpine

# Copy the package.json and package-lock.json files to the container
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install && npm cache clean --force

# Copy the remaining frontend files to the container
COPY . .

EXPOSE 3000

# Set the command to run when the container starts
CMD [ "npm", "run" "start" ]
