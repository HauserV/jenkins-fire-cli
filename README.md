# jenkins-fire-cli
A Jenkins command line tool built with python-fire that wraps the jenkins-cli and job-dsl-core.

## Prerequisite 
You need to ensure `Java` and `Python>=3.8` are in the PATH to use this tool. 

## Install
It can be installed by the following command.
```bash
pip install jenkins-fire-cli
```

## Get Started

### Provision
You need to set Jenkins site url and user credential for the first time

```bash
jenkins-fire-cli config set jenkins.url http://your-jenkins-site
jenkins-fire-cli config set user.name john.doe

# user.token is optional, but you will be asked to type it when it is missing
# either api token or user's password will be OK, but it's recommneded to use token for the sake of security
jenkins-fire-cli config set user.token passw0rd 
```

Before you start to run Jenkins commands, don't forget to run the `init` command for the first time, which will download `jenkins-cli.jar` and `job-dsl-core-standalone.jar` automatically.

```bash
jenkins-fire-cli init
```

### Run jenkins-cli commnads
As `jenkins-fire-cli` is a wrapper of `jenkins-cli` and `job-dsl-core` to make them easier to use, 
you can find the document of `jenkins-cli` in your Jenkins site or run the following command to open in browser.

```bash
jenkins-fire-cli doc --open
```

You can use the `run` sub-command to execute `jenkins-cli` command, for example

```bash
jenkins-fire-cli run list-jobs  
# It is equivalent to "java -jar jenkins-cli.jar -s http://localhost:9090/ -webSocket list-jobs"

# For command with multiple arguments you need to quote them with ""
jenkins-fire-cli run "get-job my-job"  
```

### Run job-dsl commands

You can also run the `job-dsl` command. For example you have a `job-dsl` script with the following content.

```groovy
// file: /tmp/sample.dsl
pipelineJob('job-dsl-plugin') {
  definition {
    cpsScm {
      scm {
        git {
          remote {
            url('https://github.com/jenkinsci/job-dsl-plugin.git')
          }
          branch('*/master')
        }
      }
      lightweight()
    }
  }
}
```

Then you can run the following command to generate the job XML configuration.

```bash
jenkins-fire-cli dsl /tmp/sample-dsl.groovy
```

Then you will find a file named `job-dsl-plugin.xml` is generated. 
Now you can run anthor command to create this job in jenkins:

```bash
jenkins-file-cli run 'create-job job-dsl-plugin' < job-dsl-plugin.xml
```

Then you will find a new job named `job-dsl-plugin` has been created in jenkins.

### Environment Variables

If you want to use this tool in CI system, you may use the following environment variable instead of global setting.

* `JENKINS_USER_ID`: equivalent to `user.name`
* `JENKINS_API_TOKEN`: equvalent to `user.token`
* `JENKINS_URL`: equvalent to `jenkins.url`
* `JENKINS_JOB_DSL_PATH`: path to the job-dsl jar package, you may skip `init` when this is set 
* `JNEKINS_CLI_PATH`: path to the jenkins-cli jar package, you may skip `init` when this is set 
