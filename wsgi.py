from fabric.api import env, run, task
from common import virtualenv


PID_PATH = '/tmp/gunicorn.pid'


@task
def stopwsgi():
    run('kill `cat {}`'.format(PID_PATH))


@task
def startwsgi():
    with virtualenv():
        args = '-w 9 -k gevent --max-requests 250 --preload --pid={}'.format(
            PID_PATH
        )
        run('python manage.py run_gunicorn 0.0.0.0:8000 --settings={} {}'.format(env.settings_file, args))
