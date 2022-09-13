from .config import Config
from fire import Fire
from urllib.request import urlretrieve
import os.path

class Commands:

    def __init__(self, config: Config):
        self.config = config
    
    def init(self, jenkins_cli_url: str = None, jenkins_job_dsl_core_url: str = None, force_download=False):
        self._download_job_dsl_core(jenkins_job_dsl_core_url, force_download)
        self._download_jenkins_cli(jenkins_cli_url, force_download)
    
    def _download_job_dsl_core(self, url: str = None, force_download=False):
        # TODO: read latest version from https://repo.jenkins-ci.org/public/org/jenkins-ci/plugins/job-dsl-core/maven-metadata.xml
        url = url or 'https://repo.jenkins-ci.org/public/org/jenkins-ci/plugins/job-dsl-core/1.18/job-dsl-core-1.18-standalone.jar'
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
