from .config import Config
from fire import Fire
from urllib.request import urlretrieve, urlopen
import os.path
import xml.etree.ElementTree as ET


class Commands:

    def __init__(self, config: Config):
        self.config = config

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


if __name__ == '__main__':
    config = Config()
    entry = Commands(config)
    Fire(entry)
