# Django Application with Scrapy Integration

## Deploying a Django application with Scrapy integration using Docker

### Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Deployment Steps](#deployment-steps)
4. [Option 1 - Using DockerHub](#option-1---using-dockerhub)
5. [Option 2 - Using a Private Repository](#option-2---using-a-private-repository)
6. [Common Errors and Solutions](#common-errors-and-solutions)
7. [Conclusion](#conclusion)

## Introduction

This repository contains a Django application with Scrapy integration, along with PostgreSQL as the database backend. The application is containerized using Docker for easy deployment and scaling.

## Prerequisites

To deploy this application, you'll need the following:

- Docker installed on your local machine or server.
- Docker Compose to manage multi-container applications.

## Deployment Steps

Follow these steps to deploy the Django application with Scrapy integration using Docker:

1. Clone this repository to your local machine or server.

2. Navigate to the project directory:

   ```bash
   cd django-scrapy-app
   ```

3. Run the containers:

   ```bash
    docker-compose up -d
   ```

4. Verify that the containers are running:

   ```bash
   docker ps
   ```

5. The Django application should now be accessible at <http://localhost:8000> in your browser.

## Option 1 - Using DockerHub

If you prefer to use pre-built Docker images from DockerHub, follow these steps instead of Step 3 above:

1. Create a DockerHub account (if you don't have one already).

2. Pull the pre-built images from DockerHub:

   ```bash
   docker-compose pull
   ```

3. Run the containers:

   ```bash
   docker-compose up -d
   ```

## Option 2 - Using a Private Repository

If you have a private repository with pre-built Docker images, follow these steps instead of Step 3 above:

1. Authenticate Docker with your private repository:

   ```bash
   docker login my.private.repo.com
   ```

2. Modify the docker-compose.yml file to use the appropriate image tags from your private repository.

3. Run the containers:

   ```bash
    docker-compose up -d
   ```

## Common Errors and Solutions

Here are some common errors you may encounter during deployment and their possible solutions:

- Error: Database connection error
- Solution:
  - Ensure that PostgreSQL credentials in the Django settings and Scrapy settings are correct.
  - Make sure the PostgreSQL container is running and accessible by the Django and Scrapy containers.

- Error: Port 8000 is already in use
- Solution:
  - Check if there is any other application already running on port 8000 and stop it.
  - Alternatively, you can change the exposed port in the docker-compose.yml file to a different port.

- Error: Cannot find 'gunicorn'
- Solution:
  - Ensure that the Gunicorn package is listed in the requirements.txt file, and the container rebuild is performed using docker-compose up -d --build.

- Error: Unable to access the application
- Solution:
  - Check if the Django application container is running using docker ps.
  - Verify that the correct IP address and port are used to access the application.

## Conclusion

You have successfully deployed the Django application with Scrapy integration using Docker. Choose either Option 1 (DockerHub) or Option 2 (Private Repository) based on your preference and infrastructure requirements. If you encounter any issues or have any questions, feel free to reach out for assistance.
