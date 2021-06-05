FROM ubuntu:20.04

# Set environement variables
ENV PYTHON_CONFIGURATION_SCRIPT=/opt/configure-patroni.py
ENV POSTGRES_CONFIGURATION_YAML=/opt/postgres.yml
ENV ENTRYPOINT_SCRIPT_LOCATION=/opt/entrypoint.sh

# Execute everything that we need for setup
RUN apt-get update &&\
    apt-get -y upgrade &&\
    apt-get install -y python3.9 &&\
    apt-get install -y python3-pip &&\
    apt-get install -y python3-psycopg2 &&\
    pip3 install patroni[etcd3] &&\
    pip3 install ruamel.yaml &&\
    apt-get install -y postgresql postgresql-contrib

# Switch to postgres USER
USER postgres

# Copy files that we need to execute
COPY postgres.yml $POSTGRES_CONFIGURATION_YAML
COPY configure-patroni.py $PYTHON_CONFIGURATION_SCRIPT
COPY entrypoint.sh $ENTRYPOINT_SCRIPT_LOCATION

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

# Port's that will be exposed
EXPOSE 5432 8008

# Run entrypoint
ENTRYPOINT $ENTRYPOINT_SCRIPT_LOCATION