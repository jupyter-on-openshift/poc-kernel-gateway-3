import os

from jupyterhub.spawner import LocalProcessSpawner

config = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

class CustomLocalProcessSpawner(LocalProcessSpawner):

    #cmd = [ 'jupyter', 'lab' ]

    args = [ '--config=%s' % config ]

    def user_env(self, env):
        env['USER'] = 'default'
        env['HOME'] = '/opt/app-root/data/%s' % self.user.name
        env['SHELL'] = '/bin/bash'
        return env
    
    def get_env(self):
        env = super().get_env()
        if self.user_options.get('env'):
            env.update(self.user_options['env'])
        env['LD_LIBRARY_PATH'] = os.environ['LD_LIBRARY_PATH']
        env['LD_PRELOAD'] = os.environ['LD_PRELOAD']
        env['NSS_WRAPPER_PASSWD'] = os.environ['NSS_WRAPPER_PASSWD']
        env['NSS_WRAPPER_GROUP'] = os.environ['NSS_WRAPPER_GROUP']
        env['PYTHONUNBUFFERED'] = os.environ['PYTHONUNBUFFERED']
        env['PYTHONIOENCODING'] = os.environ['PYTHONIOENCODING']
        env['KG_URL'] = os.environ['KG_URL']
        env['KG_AUTH_TOKEN'] = os.environ['KG_AUTH_TOKEN']
        return env

    def make_preexec_fn(self, name):
        def preexec():
            home = '/opt/app-root/data/%s' % name
            if not os.path.exists(home):
                os.mkdir(home)
            os.chdir(home)
        return preexec

c.JupyterHub.spawner_class = CustomLocalProcessSpawner
