FROM ubuntu:20.04

# Set environement variables
ENV PYTHON_CONFIGURATION_SCRIPT=/opt/configure-patroni.py
ENV POSTGRES_CONFIGURATION_YAML=/opt/postgres.yml
ENV ENTRYPOINT_SCRIPT_LOCATION=/opt/entrypoint.sh
ENV CONFIGURATION_ENDPOINT=/opt/
ENV POSTGRES_VERSION=13
#ENV PATRONI_LOG_DIR=/tmp/patroni

# Execute everything that we need for setup
RUN apt-get update &&\
    apt-get install -y python3.9 &&\
    apt-get install -y python3-pip &&\
    apt-get install -y python3-psycopg2 &&\
    apt-get install -y lsb-core &&\
    apt-get install -y wget &&\
    pip3 install patroni[etcd3] &&\
    pip3 install ruamel.yaml &&\
    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' &&\
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - &&\
    apt-get update &&\
    apt-get -y install postgresql-$POSTGRES_VERSION postgresql-contrib-$POSTGRES_VERSION
#    mkdir $PATRONI_LOG_DIR &&\
#    chown -R postgres: $PATRONI_LOG_DIR

# Switch to postgres USER
USER postgres

# Copy files that we need to execute
COPY configuration/* $CONFIGURATION_ENDPOINT

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Port's that will be exposed
EXPOSE 5432 8008

# Run entrypoint
ENTRYPOINT $ENTRYPOINT_SCRIPT_LOCATION