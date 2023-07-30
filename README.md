# Django Application with Scrapy Integration

## Deploying a Django application with Scrapy integration using Docker

### Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Deployment Steps](#deployment-steps)
4. [Option 1 - Using DockerHub](#option-1---using-dockerhub)
5. [Option 2 - Using a Private Repository](#option-2---using-a-private-repository)
6. [Pushing Image to Registry or DockerHub](#pushing-image-to-registry-or-dockerhub)
7. [Common Errors and Solutions](#common-errors-and-solutions)
8. [Conclusion](#conclusion)

## Introduction

This repository contains a Django application with Scrapy integration, along with PostgreSQL as the database backend. The application is containerized using Docker for easy deployment and scaling.

## Prerequisites

To deploy this application, you'll need the following:

- [Docker installed on your local machine or server.](./InstallDocker.txt)
- [Docker Compose to manage multi-container applications.](./InstallDockerCompose.txt)

## Deployment Steps

You need git on local system so install it on centos system

```bash
yum install git
git --version
```

Follow these steps to deploy the Django application with Scrapy integration using Docker:

1. Clone this repository to your local machine or server.

   ```bash
   git clone  git@github.com:vaibhavkumar779/kostya-toldot.git
   ```

2. Navigate to the project directory:

   ```bash
   cd kostya-toldot
   ```

3. Run the containers:

   ```bash
    docker-compose up -d
   ```

4. Verify that the containers are running:

   ```bash
   docker ps
   ```

5. The Django application should now be accessible at <http://localhost:8000/admin> in your browser. Remember that to use it on your url make it available to public. Then replace localhost with your IP. Now login to your admin with username='root', password='654zz321xx'

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

## Pushing Image to Registry or DockerHub

The Image can created locally, this command should be run locally where Dockerfile is present.

   ```bash
    docker-compose build
   ```

Then We can push this image to repository we want.

### Pushing Docker Image to Docker Hub

1. Log in to Docker Hub using the Docker CLI:

   ```bash
   docker login
   ```

2. Tag your Docker image with your Docker Hub username and the desired repository name:

   ```bash
   docker-compose tag <service-name> <docker-hub-username>/<repository-name>:<tag>
   ```

3. Push the tagged image to Docker Hub:

   ```bash
    docker-compose push <service-name>
   ```

### Pushing Docker Image to a Private Container Registry

1. Log in to the private container registry using the Docker CLI. The exact command may vary depending on the registry provider, but it is similar to the Docker Hub login command:

   ```bash
   docker login <registry-url>
   ```

2. Tag your Docker image with the private registry URL and the desired repository name:

   ```bash
   docker-compose tag <service-name> <registry-url>/<repository-name>:<tag>
   ```

3. Push the tagged image to the private container registry:

   ```bash
    docker-compose push <service-name>
   ```

   **Note:** Before pushing an image to a private container registry, ensure that you have proper authentication and permissions to access the registry. Different container registry providers have their own authentication methods, so consult the documentation of your specific registry for more details.

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
