from fabric.api import task
from fabric.api import env, run
from common import virtualenv


@task
def start():
    with virtualenv():
        run('celery -A {} worker -l info'.format(env.name))
