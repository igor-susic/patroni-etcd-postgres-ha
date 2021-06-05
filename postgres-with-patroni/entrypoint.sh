# Get Docker IP adress
readonly DOCKER_IP=$(hostname --ip-address)
export PATRONI_POSTGRESQL_CONNECT_ADDRESS="$DOCKER_IP:5432"
export PATRONI_REST_API_CONNECT_ADDRESS="$DOCKER_IP:8008"

# Executing configuration script
python3 $PYTHON_CONFIGURATION_SCRIPT

# Launch patroni
exec patroni $POSTGRES_CONFIGURATION_YAML