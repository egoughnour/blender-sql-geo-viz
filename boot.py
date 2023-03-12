import subprocess
import docker
import json
import os
import re


def get_docker_socket_as_env_dict(status_result):
    socket_output_pattern = r"^INFO\[\d*?] socket: (?P<socket>.*?)$"
    docker_env_dict = {}
    matches = re.finditer(socket_output_pattern, status_result.stdout, re.MULTILINE)
    for _, match in enumerate(matches, start=1):
        docker_env_dict["DOCKER_HOST"] = match.group('socket')
        if docker_env_dict["DOCKER_HOST"]:
            break
    return docker_env_dict

def get_colima_status_and_socket():
    status_arg_list = ['colima', 'status']
   
    is_running = False
    docker_dict = None
    status_result = subprocess.run(status_arg_list, capture_output=True)
    if b'Running' in status_result.stdout or b'running' in status_result.stdout:
        print('Colima is already running')
        docker_dict = get_docker_socket_as_env_dict(status_result)
        is_running = True
    else:
        is_running = False
    return docker_dict,is_running

def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    host = os.getenv('DB_HOST', config['db']['host'])
    port = os.getenv('DB_PORT', config['db']['port'])
    database = os.getenv('DB_NAME', config['db']['name'])
    username = os.getenv('DB_USERNAME', config['db']['username'])
    password = os.getenv('DB_PASSWORD', config['db']['password'])

    # Check if Colima is already installed
    result = subprocess.run(['brew', 'ls', '--versions', 'colima'], capture_output=True)
    
    docker_env_dict = None
    colima_start_args = ['colima', 'start']

    if result.returncode == 0:
        print('Colima is already installed')

        # Check if Colima is already running
        # also get the actual socket then pass it in the docker.from_env environment var dict
        docker_env_dict, is_running = get_colima_status_and_socket()
        if not is_running:
            # Start the Colima daemon
            subprocess.run(colima_start_args, check=True)
            docker_env_dict, is_running = get_colima_status_and_socket()
    else:
        # Install Colima using Homebrew
        subprocess.run(['brew', 'install', 'colima'], check=True)

        # Start the Colima daemon
        subprocess.run(colima_start_args, check=True)
        docker_env_dict, is_running = get_colima_status_and_socket()

    # Start Docker
    docker_result = subprocess.run(['docker', 'info'], capture_output=True)
    if docker_result.returncode == 0:
        print('Docker is already running')
    else:
        subprocess.run(['open', '-a', 'Docker'], check=True)


    # Start the local Docker daemon
    client = docker.from_env(environment=docker_env_dict)

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
    same_container = client.containers.get(container_name)
    assert(same_container.id == container.id)

    # Check if database already exists
    check_db_cmd = f"psql -U {username} -tAc \"SELECT 1 FROM pg_database WHERE datname='{database}'\""
    output = container.exec_run(check_db_cmd)

    if not output.output.decode("utf-8").strip():
        # If database does not exist, create it
        create_db_cmd = f"createdb -U {username} {database}"
        container.exec_run(create_db_cmd)
        print(f"Database {database} created successfully!")
    else:
        # If database already exists, print message and exit
        print(f"Database {database} already exists!")