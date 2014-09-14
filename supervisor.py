from fabric.api import task
from fabric.api import env, sudo
from common import virtualenv


@task
def restart_celery():
    with virtualenv():
        sudo('{}/bin/supervisorctl restart celery'.format(env.virtualenv))


@task
def restart_celerybeat():
    with virtualenv():
        sudo('{}/bin/supervisorctl restart celerybeat'.format(env.virtualenv))
