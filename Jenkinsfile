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
        stage('Test') {
            parallel {
                stage('Simple test') {
                    steps {
                        sh 'make PY=python3 test'
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

