from fabric.api import task
from fabric.api import run
from common import get_project_config


@task
def dropdb():
    config = get_project_config()
    db_name = '{}_db'.format(config['project'].get('name'))
    run('sudo -i -u postgres /bin/bash -l -c "dropdb {}"'.format(db_name))
