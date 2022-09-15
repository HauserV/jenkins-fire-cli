import os
from os.path import expanduser, join
import sys
import json
import getpass

USER_HOME = expanduser("~")


def eprint(text):
    print(text, file=sys.stderr)


class Config:

    def __init__(self, user_home=USER_HOME):
        self.user_home = user_home
        self.config_home = join(self.user_home, '.jenkins-fire-cli')
        self.config_file = join(self.config_home, 'config.json')
        self.jar_libs = join(self.config_home, 'jar_libs')

        os.makedirs(self.config_home, exist_ok=True, mode=0o755)
        os.makedirs(self.jar_libs, exist_ok=True, mode=0o755)

    def set(self, path: str, value):
        config = self._load_config()
        keys = path.split('.')

        next_config = config
        for key in keys[:-1]:
            next_config = next_config.setdefault(key, dict())
        next_config[keys[-1]] = value
        self._write_config(config)

    def get(self, path: str):
        config = self._load_config()
        next_config = config
        for key in path.split('.'):
            if type(next_config) is not dict:
                break
            next_config = next_config.get(key, None)
        return next_config

    def show(self):
        print(self._read_config())

    @property
    def username(self):
        return os.environ.get('JENKINS_USER_ID', self.get('user.name'))

    @property
    def token(self):
        return os.environ.get('JENKINS_API_TOKEN', self.get('user.token')) or getpass.getpass()

    @property
    def job_dsl_core_path(self):
        return os.environ.get('JENKINS_JOB_DSL_PATH', join(self.jar_libs, 'job-dsl-core-standalone.jar'))

    @property
    def jenkins_url(self):
        url = os.environ.get('JENKINS_URL', self.get('jenkins.url')) or 'http://localhost:8080'
        return url.rstrip('/')

    @property
    def jenkins_cli_download_url(self):
        return '{}/jnlpJars/jenkins-cli.jar'.format(self.jenkins_url)

    @property
    def jenkins_cli_path(self):
        return os.environ.get('JENKINS_CLI_PATH', join(self.jar_libs, 'jenkins-cli.jar'))

    def _read_config(self):
        try:
            with open(self.config_file, 'r', encoding='utf-8') as fp:
                return fp.read()
        except FileNotFoundError:
            return ''

    def _load_config(self):
        s = self._read_config()
        if not s:
            return dict()
        try:
            return json.loads(s)
        except json.JSONDecodeError as e:
            eprint('Fail to parse configuration, please check {}'.format(
                self.config_file))
            raise e

    def _write_config(self, config):
        with open(self.config_file, 'w') as fp:
            json.dump(config, fp, sort_keys=True, indent=2)
        # use file mode 600 as token is save in it
        os.chmod(self.config_file, 0o600)
