from fabric.api import task
from fabric.api import env, run, require
from fabric.operations import prompt
from common import virtualenv


def verify_migration_app_is_set():
    if not 'schemamigration_app' in env:
        env.schemamigration_app = prompt(
            'App name for Schema migration:',
            default='',
        )


def verify_migration_initial_is_set():
    if not 'schemamigration_initial' in env:
        env.schemamigration_initial = prompt('Initial? [y|n]:', default='n')


@task
def migrate():
    # if app == '', south will look for all migrations in all apps
    verify_migration_app_is_set()
    with virtualenv():
        run(
            'python manage.py migrate {} --settings={}'.format(
                env.schemamigration_app,
                env.settings_file,
            )
        )


@task
def schemamigration():
    initial = ''
    verify_migration_app_is_set()
    verify_migration_initial_is_set()
    app = env.schemamigration_app
    initial = '--initial' if env.schemamigration_initial == 'y' else '--auto'
    with virtualenv():
        run(
            'python manage.py schemamigration {} {} --settings={}'.format(
                initial,
                app,
                env.settings_file
            )
        )


@task
def django_shell():
    with virtualenv():
        run('python manage.py shell --settings={}'.format(env.settings_file))


@task
def collectstatic():
    with virtualenv():
        run(
            'python manage.py collectstatic --settings={}'.format(
                env.settings_file
            )
        )


@task
def collectstatic_aws():
    require('aws_access_key_id', 'aws_secret_access_key')
    collectstatic()


@task
def syncdb():
    with virtualenv():
        run(
            'python manage.py syncdb --noinput --settings={}'.format(
                env.settings_file
            )
        )


@task
def createsuperuser():
    with virtualenv():
        run(
            'python manage.py createsuperuser --settings={}'.format(
                env.settings_file
            )
        )


@task
def runserver():
    with virtualenv():
        run(
            'python manage.py runserver [::]:8000 --settings={}'.format(
                env.settings_file
            )
        )
