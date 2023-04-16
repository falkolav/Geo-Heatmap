# Build the Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install libgdal dependency in order for Fiona installation to work
RUN apt-get update
RUN apt-get install -y gdal-bin libgdal-dev g++

# Install requirements
RUN pip install -r requirements.txt


# Copy the application code
COPY . .