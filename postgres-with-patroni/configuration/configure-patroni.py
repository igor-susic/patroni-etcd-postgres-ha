import os
from ruamel.yaml import YAML


def setup_patroni_postgres_yml():
    """
    Replaces variables within postgres.yml with the dynamic configuration
    that is passed to this script through environment variables.
    """
    # Load Patroni postgres configuration file
    yaml = YAML()
    yaml.allow_duplicate_keys = True
    yaml.preserve_quotes = True

    try:
        assert os.environ.get("POSTGRES_CONFIGURATION_YAML")
        assert os.environ.get("SUPERUSER_USERNAME")
        assert os.environ.get("SUPERUSER_PASSWORD")
        assert os.environ.get("ADMIN_PASSWORD")
        assert os.environ.get('ETCD_HOST')
        assert os.environ.get('ETCD_PORT')
        assert os.environ.get("REPLICATION_USERNAME")
        assert os.environ.get("REPLICATION_PASSWORD")
        assert os.environ.get("PG_REWIND_USERNAME")
        assert os.environ.get("PG_REWIND_PASSWORD")
        assert os.environ.get("PATRONI_POSTGRESQL_CONNECT_ADDRESS")
        assert os.environ.get("PATRONI_REST_API_CONNECT_ADDRESS")
        assert os.environ.get("POSTGRES_VERSION")
    except AssertionError as e:
        raise AttributeError("One of the variables is missing, will about this script. Error: %s" % e)

    with open(os.environ.get("POSTGRES_CONFIGURATION_YAML")) as configuration:
        patroni_config = yaml.load(configuration)

        # Load some global settings
        patroni_config['scope'] = os.environ.get("CLUSTER_NAME")
        patroni_config['name'] = os.environ.get("NODE_NAME")
        patroni_config['namespace'] = os.environ.get("NAMESPACE")

        # Load ETCD3 host
        patroni_config['etcd3']['host'] = f"{os.environ.get('ETCD_HOST')}:{os.environ.get('ETCD_PORT')}"

        # Users done on bootstrap
        patroni_config['bootstrap']['users']['admin']['password'] = os.environ.get("ADMIN_PASSWORD")

        # Superuser user
        patroni_config['postgresql']['authentication']['superuser']['username'] = os.environ.get("SUPERUSER_USERNAME")
        patroni_config['postgresql']['authentication']['superuser']['password'] = os.environ.get("SUPERUSER_PASSWORD")

        # Replicas will use this user to access master via streaming replication
        patroni_config['postgresql']['authentication']['replication']['username'] = os.environ.get("REPLICATION_USERNAME")
        patroni_config['postgresql']['authentication']['replication']['password'] = os.environ.get("REPLICATION_PASSWORD")

        # User for pg_rewind
        patroni_config['postgresql']['authentication']['rewind']['username'] = os.environ.get("PG_REWIND_USERNAME")
        patroni_config['postgresql']['authentication']['rewind']['password'] = os.environ.get("PG_REWIND_PASSWORD")

        # Connection point for postgres
        patroni_config['postgresql']['connect_address'] = os.environ.get("PATRONI_POSTGRESQL_CONNECT_ADDRESS")

        # Connection point for Patroni REST API
        patroni_config['restapi']['connect_address'] = os.environ.get("PATRONI_REST_API_CONNECT_ADDRESS")

        # Edit connection rules for replication user
        pg_hba = patroni_config['bootstrap']['pg_hba']
        pg_hba[0] = f"host replication {os.environ.get('REPLICATION_USERNAME')} 0.0.0.0/0 md5"
        patroni_config['bootstrap']['pg_hba'] = pg_hba

        # Set binary directory depending on the Postgres version
        patroni_config['postgresql']['bin_dir'] = f"/usr/lib/postgresql/{os.environ.get('POSTGRES_VERSION')}/bin"

        # Set data directory
        patroni_config['postgresql']['data_dir'] = f"/var/lib/postgresql/{os.environ.get('POSTGRES_VERSION')}/data"

    with open(os.environ.get("POSTGRES_CONFIGURATION_YAML"), 'w') as configuration:
        # Save back changes to disk
        yaml.dump(patroni_config, configuration)


if __name__ == "__main__":
    setup_patroni_postgres_yml()
