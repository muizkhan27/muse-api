import os

import psycopg2


def configure_json(data, db_name):
    data = '\n' + '\'' + str(db_name) + '\'' + ': ' + str(data) + ','
    return data


def serialized_data(serializer):
    db_name = serializer.data['subdomain']
    user = serializer.data['name'].replace(' ', '').lower()
    return db_name, user


def get_connection(db, user, password, host, port):
    return psycopg2.connect(
        database=db,
        user=user,
        password=password,
        host=host,
        port=port,
    )


def create_db_and_user(connection, db_name, user, password):
    with connection.cursor() as cursor:
        connection.autocommit = True
        cursor.execute(f'CREATE DATABASE {db_name}')
        cursor.execute(f"CREATE USER {user} WITH PASSWORD '{password}';")
        cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {user};")


def db_configuration(name, user, password, host, port):
    return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
        'ATOMIC_REQUESTS': False,
        'AUTOCOMMIT': True,
        'CONN_MAX_AGE': 0,
        'CONN_HEALTH_CHECKS': False,
        'OPTIONS': {},
        'TIME_ZONE': None,
        'TEST': {
            'CHARSET': None,
            'COLLATION': None,
            'MIGRATE': True,
            'MIRROR': None,
            'NAME': None
        }
    }


def db_settings(db_name, user, password, host, port):
    return {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
    }


def update_settings(configured_json):
    with open('musetax_api/settings.py', 'r') as f:
        data = f.readlines()

    for i, line in enumerate(data):
        if line.strip().startswith('DATABASES'):
            data[i] = '\tDATABASES = {' + configured_json + '\n'

    updated_settings_path = os.path.join(os.getcwd(), 'musetax_api', 'updated_settings.py')
    with open(updated_settings_path, 'w') as f:
        f.writelines(data)

    os.replace('musetax_api/updated_settings.py', 'musetax_api/settings.py')
