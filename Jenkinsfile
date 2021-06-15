pipeline {
    agent {
        label 'linux'
    }

    stages {
        stage('Check code') {
            steps {
                echo 'Check for best coding standards'
                sh 'shellcheck --version'
                sh 'make PY=python3 check'
            }
        }
        stage('Test - prepare') {
            steps {
                sh 'make PY=python3 venv_prod'
            }
        }
        stage('Test - run') {
            parallel {
                stage('Test print to terminal - short') {
                    steps {
                        sh 'make PY=python3 SCRIPT_PARAM="-f sharesListExample.py -s"'
                    }
                }
                stage('Test print to terminal - detailed') {
                    steps {
                        sh 'make PY=python3 SCRIPT_PARAM="-f sharesListExample.py -d"'
                    }
                }
                stage('Test print to terminal - latest prices') {
                    steps {
                        sh 'make PY=python3 SCRIPT_PARAM="-f sharesListExample.py --latest-prices"'
                    }
                }
            }
        }
        // stage('Build docker image') {
        //     steps {
        //         sh 'make docker_build'
        //     }
        // }
    }
}

