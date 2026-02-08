library(
    identifier: 'yat@feature/pre-commit',
    retriever: modernSCM(
        scm: [
            $class: 'GitSCMSource',
            remote: 'https://github.com/lookslikematrix/yat'
        ],
        libraryPath: 'jenkins'
    )
)

pipeline {
    agent any

    stages {
        stage('🔶 pre-commit') {
            agent {
                dockerfile {
                    label 'docker'
                }
            }
            steps {
                preCommit()
            }
        }
        stage('⚒️ Build') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    docker buildx bake
                '''
            }
        }
        // deploy lookslikematrix/yat:latest
    }
}
