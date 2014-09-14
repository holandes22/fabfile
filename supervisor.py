from fabric.api import task
from fabric.api import env, run
from common import virtualenv


@task
def restart_celery():
    with virtualenv():
        run('{}/bin/supervisorctl restart celery'.format(env.virtualenv))


@task
def restart_celerybeat():
    with virtualenv():
        run('{}/bin/supervisorctl restart celerybeat'.format(env.virtualenv))
