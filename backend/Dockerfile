# Build the Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install requirements
RUN pip install -r requirements.txt

# Create env variables and add .env.dev
ARG DB_USERNAME
ARG DB_PASSWORD

ENV DB_USERNAME=$DB_USERNAME
ENV DB_PASSWORD=$DB_PASSWORD


# Copy the application code
COPY . .