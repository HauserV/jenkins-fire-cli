import os
from os.path import expanduser, join
import sys
import json

USER_HOME = expanduser("~")


def eprint(text):
    print(text, file=sys.stderr)


class Config:

    def __init__(self, user_home=USER_HOME):
        self.user_home = user_home
        self.config_home = join(self.user_home, '.jenkins_file_cli')
        self.config_file = join(self.config_home, 'config.json')
        self.jar_libs = join(self.user_home, 'jar_libs')

    def init(self):
        os.makedirs(self.config_home, exist_ok=True, mode=0o755)
        os.makedirs(self.jar_libs, exist_ok=True, mode=0o755)
    
    def set(self, path: str, value):
        config = self._load_config()
        keys = path.split('.')

        sub_config = config
        for key in keys[:-1]:
            sub_config = sub_config.setdefault(key, dict())
        sub_config[keys[-1]] = value
        self._write_config(config)

    def show(self):
        print(self._read_config())

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
    
    
    
