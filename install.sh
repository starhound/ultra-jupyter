#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt-get update

# Install Docker and Docker Compose if not already installed
echo "Installing Docker and Docker Compose..."
sudo apt-get install -y docker.io docker-compose

# Pull the custom JupyterHub and notebook images
echo "Pulling custom Docker images..."
docker pull starhound/ultra-jupyter
docker pull starhound/ultra-jupyter-notebook