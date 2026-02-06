library(
    identifier: 'yat@main',
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
            steps {
                preCommit()
            }
        }
    }
}
