import json

import environ
from django.conf import settings
from django.core.management import call_command

from .db_setup_utility import (configure_json, create_db_and_user,
                               db_configuration, db_settings, get_connection,
                               serialized_data, update_settings)

env = environ.Env(
  DEBUG=(bool, False)
)
environ.Env.read_env()


DATABASE_NAME = env('DEFAULT_DATABASE_NAME')
DATABASE_USER = env('DATABASE_USER')
DATABASE_PASSWORD = env('DATABASE_PASSWORD')
DATABASE_HOST = env('DATABASE_HOST')
DATABASE_PORT = env('DATABASE_PORT')


def local_db_setup(serializer, password):
    db_name, user = serialized_data(serializer)

    connection = get_connection(
        DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT
    )

    create_db_and_user(connection, db_name, user, password)

    new_db_settings = db_settings(db_name, user, password, DATABASE_HOST, DATABASE_PORT)

    db_json = json.dumps(new_db_settings, indent=4)
    configured_json = configure_json(db_json, db_name)

    new_db_configuration = db_configuration(db_name, user, password, DATABASE_HOST, DATABASE_PORT)

    settings.DATABASES[db_name] = new_db_configuration

    update_settings(configured_json)

    call_command('migrate', database=db_name, app_label='users')


def prod_db_setup(serializer, password):
    db_name, user = serialized_data(serializer)

    connection = get_connection(
        DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT
    )

    create_db_and_user(connection, db_name, user, password)

    connection.close()

    new_db_configuration = db_configuration(db_name, user, password, DATABASE_HOST, DATABASE_PORT)

    settings.DATABASES[db_name] = new_db_configuration

    new_db_settings = db_settings(db_name, user, password, DATABASE_HOST, DATABASE_PORT)

    db_json = json.dumps(new_db_settings, indent=4)
    configured_json = configure_json(db_json, db_name)

    update_settings(configured_json)

    call_command('migrate', database=db_name, app_label='users')
