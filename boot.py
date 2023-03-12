import subprocess
import docker

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
port_mapping = {'5432/tcp': 5432}
environment = {'POSTGRES_PASSWORD': 'mysecretpassword'}
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
