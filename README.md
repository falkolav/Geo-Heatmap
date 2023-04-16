# **Full Stack Web Application for Heatmap Generation**

This is a full stack web application that generates a heatmap of usage per organization around the world. The backend is built using Python, FastAPI, and PostgreSQL with PostGIS, while the frontend is built using React, TypeScript, Material/UI, and Leaflet. The application also includes an ETL job that is loaded using the process_data.py script.

![](https://github.com/falkolav/Geo-Heatmap/blob/main/demo.gif)

## **Getting Started**

### **Requirements**

- Docker

### **Installation**

1. Clone this repository to your local machine.
2. Open a terminal window and navigate to the root directory of the cloned repository.
3. Start Docker.
4. Login into docker in your terminal by running **`docker login.`**
5. Run **`docker pull falkolav/geo-heatmap-backend:0.0.1; docker pull falkolav/geo-heatmap-backend:0.0.1; docker pull falkolav/geo-heatmap-backend:0.0.1`** 
6. Run **`docker-compose up --build`--** to start the containers for the database, backend, and front-end. (May cause difficulties on M1 Macs, in which case “brew install gdal” should fix it.)
7. Grab some coffee. This might take a minute or two :)
8. Go to **[http://localhost:3000/](http://localhost:3000/)** to see the application in action. Or test the api at http://localhost:8000/

### **API Endpoints**

### **`GET /organisations`**

Returns a list of unique organization IDs for which usage data is available in the database.

### **`GET /heatmap-data/{org_id}`**

Returns the usage data for a given organization ID in the format required by the frontend.

**Request Parameters:**

- **`org_id`** (string): A string representing the organization ID for which to fetch usage data.

**Response:**

- A list of PointData objects, where each object represents a usage data point with the latitude, longitude, and weight (i.e., usage count) specified.

## **CI/CD Pipeline (not implemented)**

The CI/CD pipeline for this project would be triggered whenever a new commit is pushed to a branch. The pipeline would include the following stages:

1. **Build**: The pipeline would start by building the Docker images for the backend and frontend.
2. **Test**: The pipeline would then run the automated tests for both the backend and frontend.
3. **Deploy**: If all tests pass, the pipeline would deploy the application to a staging environment for further testing.
4. **Release**: After the application has been thoroughly tested in the staging environment, the pipeline would release the application to the production environment.

The pipeline would be implemented using GitHub Actions, which provides a built-in continuous integration and delivery service. The pipeline configuration would be stored in the **`.github/workflows`** directory of the project repository.
