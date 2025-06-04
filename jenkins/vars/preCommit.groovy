def call(Map config = [:]) {
    stage("🔶 pre-commit") {
        scriptDir = new File(getClass().protectionDomain.codeSource.location.path).parent
        echo scriptDir

        docker.image("python:latest").inside {
            sh """#!/bin/bash
                set -e
                echo "🔶 pre-commit"
                echo "The script you are running has:"
                echo "basename: [\$(basename "\$0")]"
                echo "dirname : [\$(dirname "\$0")]"
                echo "pwd     : [\$(pwd)]"
            """
        }
    }
}
