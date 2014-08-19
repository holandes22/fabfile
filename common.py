import os
import yaml
from contextlib import contextmanager

from fabric.operations import prompt
from fabric.context_managers import prefix
from fabric.api import env, local, cd, require, task


def get_project_config():
    here = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    with open(os.path.join(here, 'Fabfile.yml')) as f:
        return yaml.load(f)


@contextmanager
def virtualenv():
    verify_settings_type_is_set()
    verify_aws_keys_are_set()
    require('settings_file')
    config = get_project_config()
    activate_script = os.path.join(config['project'].get('virtualenv'), 'bin', 'activate')
    with cd('/vagrant'):
        eid = 'export AWS_ACCESS_KEY_ID={}'.format(env.aws_access_key_id)
        ekey = 'export AWS_SECRET_ACCESS_KEY={}'.format(env.aws_secret_access_key)
        with prefix('source {} && export SECRET_KEY=dev && {} && {} && export PYTHONPATH=/vagrant'.format(activate_script, eid, ekey)):
            yield


@task
def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    hostname = local('vagrant ssh-config | grep HostName', capture=True)
    port = local('vagrant ssh-config | grep Port', capture=True)
    env.hosts = ['{}:{}'.format(hostname.split()[1], port.split()[1]), ]

    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].strip('"')


def verify_settings_type_is_set():
    if not 'settings_type' in env:
        env.settings_type = prompt(
            'Settings type to [prod|dev]',
            default='dev'
        )
    config = get_project_config()
    name = config['project'].get('name')
    if env.settings_type == 'dev':
        env.settings_file = '{}.settings.dev'.format(name)
    else:
        env.settings_file = '{}.settings.prod'.format(name)


def verify_aws_keys_are_set():
    if not 'aws_access_key_id' in env:
        env.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
    if not 'aws_secret_access_key' in env:
        env.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
