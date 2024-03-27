This is a slack bot backend that connects to analitiq backend.

### Prerequisites
- Docker and Docker Compose must be installed on your system.
- A basic understanding of Docker, Docker Compose and FastAPI is required.

### Project Structure Overview
- **Slack Backend**: A FastAPI application located inside the `/app` directory.

### Important Files
- `.env`: Contains the environment variables required for the Docker containers.
- `docker-compose.prod.yml`: Docker Compose file used to orchestrate the production deployment.
- `docker-compose.dev.yml`: Docker Compose file used to orchestrate the development deployment.
- `routers/chat.py`: Handles routing of chat information from the front end.
- `main.py`: Incorporates socket.io for real-time communication features.

### Step-by-Step Production Deployment Guide

#### 1. Preparing Environment Variables
- Duplicate the provided `.env` sample. Customize the values to suit your specific environment.

#### 2. Configuring the Docker Compose File
- Examine the `docker-compose.prod.yml` file. It outlines one service: `slack_app_backend`

#### 3. Deploying with Docker Compose
- Open a terminal and navigate to your project's root directory, where your `docker-compose.prod.yml` file is located.
- Execute `docker compose -f docker-compose.prod.yml up -d` to initiate all services specified in the Docker Compose file.

#### 4. Verifying the Deployment
- Once the containers are operational, access the slack app backend's `/slack/check` endpoint. So, if the slack app backend is running at `http://localhost:6002`, try accessing `http://localhost:6002/slack/check` and you should get a text response `Slack app backend is up and running!`

### Step-by-Step Development Deployment Guide
- Duplicate the provided `.env` sample. Customize the values to suit your specific environment.
- To generate a qualified self-signed certificate for development purposes, use [mkcert](https://github.com/FiloSottile/mkcert). **Note**: This tool must be installed on your host machine for the browser to recognize the certificate as valid.
- Please note self-signed certificates must be named as `local-cert.pem`and `local-key.pem` and must be located under certs before executing the docker compose command. You can execute this command from the project root file and update the hostname if needed`mkcert -cert-file certs/local-cert.pem -key-file certs/local-key.pem "domain.local" "*.domain.local"`
- For accessing your services via custom domains like `slack-backend.domain.local` without the `HTTP/HTTPS` in other words the hostname only, you may need to edit your system's hosts file to resolve these domains to your local machine (127.0.0.1).
- For development, please use `docker compose -f docker-compose.dev.yml up -d`

### Creating the eternal access token for slack backend
Slack backend will need to make a few API calls to the infra backend. These API calls are protected and need a valid JWT access token. Since this is a service-service communication, we can issue an eternal access token for the slack backend which can be saved in the env of slack backend.
To get this, we need to designate a username, email and a password for this service user. The username and email could be `slack_backend@example.com` and the password could be a random string. We do not need to remember the password because the service user will only be authenticated via eternal access token and not username-password duo.

Assuming the infra backend is running at `http://localhost:6001` here is the curl command to get the eternal access token:
```
curl --location 'http://localhost:6001/auth/get_eternal_access_token' \
--form 'username="slack_backend@example.com"' \
--form 'email="slack_backend@example.com"' \
--form 'password="password"'
```

The eternal access token then needs to be saved as `ANALITIQ_ACCESS_TOKEN` in slack/.env file.


### Additional Notes
- Regularly check for updates to dependencies and Docker images to ensure your application remains secure and performant.
- Monitor application logs and performance to proactively address any issues or bottlenecks.
- Please note in case you are using localhost subdomain the certificate must be generated with an explict hostnames rather than wildcard, because the browsers do not support it i.e. `mkcert -cert-file certs/local-cert.pem -key-file certs/local-key.pem "localhost" "slack-backend.localhost"`
  This guide aims to facilitate a smooth deployment process, from initial setup to running a fully functional public chat application in both development and production environments.