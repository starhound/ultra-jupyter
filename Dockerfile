# Start from the official JupyterHub Docker image
FROM quay.io/jupyterhub/jupyterhub:latest

# Switch to root to install dependencies
USER root

# Install DockerSpawner
RUN pip install dockerspawner

# Copy JupyterHub configuration file
COPY jupyterhub_config.py /etc/jupyterhub/jupyterhub_config.py

# Switch back to the JupyterHub user
USER ${NB_USER}

# Expose port for JupyterHub
EXPOSE 8000

# Start JupyterHub
CMD ["jupyterhub", "-f", "/etc/jupyterhub/jupyterhub_config.py"]
