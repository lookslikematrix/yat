def call() {
    script {
        sh '''#!/bin/bash
            set -e
            python -m yat
        '''
    }
}
