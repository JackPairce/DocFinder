# DocFinder

## Introduction

DocFinder is a web application designed to help you find and manage your documents efficiently.

## Prerequisites

Before you can start the app, you need to have Docker installed on your system. Follow the instructions below to install Docker based on your operating system.

### Installing Docker

#### Windows

1. Download Docker Desktop for Windows from [Docker's official website](https://www.docker.com/products/docker-desktop).
2. Run the installer and follow the on-screen instructions.
3. Once the installation is complete, start Docker Desktop.

#### macOS

1. Download Docker Desktop for Mac from [Docker's official website](https://www.docker.com/products/docker-desktop).
2. Open the downloaded `.dmg` file and drag the Docker icon to your Applications folder.
3. Start Docker Desktop from the Applications folder.

#### Linux

1. Update your package index:

    ```sh
    sudo apt-get update
    ```

2. Install Docker using the following command:

    ```sh
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

3. Start the Docker service:

    ```sh
    sudo systemctl start docker
    ```

4. Enable Docker to start on boot:

    ```sh
    sudo systemctl enable docker
    ```

## Starting the App

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/DocFinder.git
    ```

2. Navigate to the project directory:

    ```sh
    cd DocFinder
    ```

3. Build the Docker image:

    ```sh
    docker compose build
    ```

4. Run the Docker container:

    ```bash
    docker compose up
    ```

    This code initializes and starts the application.
    Note that it will take some time to preprocess the data and populate the database.

    To monitor the application startup process, use the following command:

    ```sh
    docker logs -f docfind-backend
    ```

5. Open your web browser and go to `http://localhost:3000` to access the app.

## Shutting Down the App

To stop and remove all running containers, networks, and volumes associated with the app, use the following command:

```sh
docker compose down
```
