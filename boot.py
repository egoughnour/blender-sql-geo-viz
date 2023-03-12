import subprocess
import docker
import json
import os

with open('config.json', 'r') as f:
    config = json.load(f)
host = os.getenv('DB_HOST', config['db']['host'])
port = os.getenv('DB_PORT', config['db']['port'])
database = os.getenv('DB_NAME', config['db']['name'])
username = os.getenv('DB_USERNAME', config['db']['username'])
password = os.getenv('DB_PASSWORD', config['db']['password'])

# Check if Colima is already installed
result = subprocess.run(['brew', 'ls', '--versions', 'colima'], capture_output=True)
if result.returncode == 0:
    print('Colima is already installed')

    # Check if Colima is already running
    status_result = subprocess.run(['colima', 'status'], capture_output=True)
    if b'Running' in status_result.stdout:
        print('Colima is already running')
    else:
        # Start the Colima daemon
        subprocess.run(['colima', 'start'], check=True)
else:
    # Install Colima using Homebrew
    subprocess.run(['brew', 'install', 'colima'], check=True)

    # Start the Colima daemon
    subprocess.run(['colima', 'start'], check=True)

# Start Docker
docker_result = subprocess.run(['docker', 'info'], capture_output=True)
if docker_result.returncode == 0:
    print('Docker is already running')
else:
    subprocess.run(['open', '-a', 'Docker'], check=True)


# Start the local Docker daemon
client = docker.from_env()

# Pull the latest Docker image of Postgres with PostGIS
image_name = 'postgis/postgis'
client.images.pull(image_name)

# Run a container based on the PostGIS image
container_name = 'my-postgres-container'
port_mapping = {'5432/tcp': port}
environment = {'POSTGRES_PASSWORD': password}
volumes = {'/data/postgres': {'bind': '/var/lib/postgresql/data', 'mode': 'rw'}}
container = client.containers.run(
    image_name,
    name=container_name,
    detach=True,
    ports=port_mapping,
    environment=environment,
    volumes=volumes
)

print('Started container:', container.id)

# Get running container by name
container = client.containers.get(container_name)

# Run command to create database in container
create_db_cmd = f"createdb -U postgres {database}"
container.exec_run(create_db_cmd)

# Confirm database creation
list_dbs_cmd = "psql -U postgres -c '\l'"
output = container.exec_run(list_dbs_cmd)
print(output.output.decode("utf-8"))