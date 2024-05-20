c = get_config()

# Set the JupyterHub bind URL
c.JupyterHub.bind_url = 'http://:8005'
c.JupyterHub.hub_ip = '0.0.0.0'
c.JupyterHub.hub_connect_ip = 'jupyterhub'  # Use the service name in the Docker network

# Configure authenticator (DummyAuthenticator for testing)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = "admin"  # Set the static password
c.Authenticator.admin_users = {'admin'}
c.Authenticator.allowed_users = {'admin'}

# Configure spawner
from dockerspawner import DockerSpawner
c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'ultra-jupyter-notebook'  # Use the custom user container image
c.DockerSpawner.network_name = 'ultra-jupyter-network'  # Use the correct network name
c.DockerSpawner.notebook_dir = '/home/jovyan/work'
c.DockerSpawner.remove = True
c.DockerSpawner.volumes = {
    'ultra-jupyterhub-{username}': '/home/jovyan/work',
}
c.DockerSpawner.debug = False  # Enable debug for more detailed logs

# Increase the timeout for slow starting servers
c.DockerSpawner.http_timeout = 60
c.DockerSpawner.start_timeout = 120

# Set the cookie secret
c.JupyterHub.cookie_secret_file = '/srv/jupyterhub/jupyterhub_cookie_secret'

# Debugging
c.JupyterHub.log_level = 'DEBUG'
