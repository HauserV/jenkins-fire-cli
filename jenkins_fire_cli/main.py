from .config import Config
import fire
from urllib.request import urlretrieve, urlopen
import os
import os.path
import xml.etree.ElementTree as ET
import subprocess as sp
import shlex
import webbrowser


class Entry:

    def __init__(self, config: Config):
        self.config = config

    @property
    def jenkins_cli_base_cmd(self):
        return ["java", "-jar", self.config.jenkins_cli_path, "-s", self.config.jenkins_url,  "-webSocket"]
    
    @property
    def job_dsl_base_cmd(self):
        return ["java", "-jar", self.config.job_dsl_core_path, '-j']

    @property
    def jenkins_env(self):
        env = os.environ.copy()
        env['JENKINS_USER_ID'] = self.config.username
        env['JENKINS_API_TOKEN'] = self.config.token
        return env

    # TODO: currently fire doesn't support pass raw arguments, so the command should pass as string
    # ref: https://github.com/google/python-fire/issues/403
    def run(self, cmd: str):
        sp.call(self.jenkins_cli_base_cmd +
                shlex.split(cmd), env=self.jenkins_env)
    
    def doc(self, open=False):
        url = "{}/manage/cli/".format(self.config.jenkins_url)
        print(url)
        if open:
            webbrowser.open(url)

    def dsl(self, file: str):
        sp.call(self.job_dsl_base_cmd + [file])

    def init(self, jenkins_cli_url: str = None, jenkins_job_dsl_core_url: str = None, force_download=False):
        self._download_job_dsl_core(jenkins_job_dsl_core_url, force_download)
        self._download_jenkins_cli(jenkins_cli_url, force_download)
    
    def _get_job_dsl_core_release_version(self):
        url = 'https://repo.jenkins-ci.org/public/org/jenkins-ci/plugins/job-dsl-core/maven-metadata.xml'
        with urlopen(url) as fp:
            tree = ET.parse(fp)
        return tree.find('./versioning/release').text

    def _download_job_dsl_core(self, url: str = None, force_download=False):
        version = self._get_job_dsl_core_release_version()
        url = url or 'https://repo.jenkins-ci.org/public/org/jenkins-ci/plugins/job-dsl-core/{version}/job-dsl-core-{version}-standalone.jar'.format(
            version=version)
        target = self.config.job_dsl_core_path
        self._download_file(url, target, force_download)

    def _download_jenkins_cli(self, url: str = None, force_download=False):
        url = url or self.config.jenkins_cli_download_url
        target = self.config.jenkins_cli_path
        self._download_file(url, target, force_download)

    def _download_file(self, url: str, target: str, force_download: bool):
        if not force_download and os.path.exists(target):
            return
        print('Download {} to {} ...'.format(url, target))
        urlretrieve(url, target)


def main():
    config = Config()
    entry = Entry(config)
    fire.Fire(entry)

    
if __name__ == '__main__':
    main()
