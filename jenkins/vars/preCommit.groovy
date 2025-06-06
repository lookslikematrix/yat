def call(Map config = [:]) {
    String target_branch = config.get('target_branch', 'origin/main')
    stage("🔶 pre-commit") {
        docker.image("lookslikematrix/yat-pre-commit:latest").inside("--env TARGET_BRANCH=${target_branch}"){
            sh '/bin/sh /.yat/run.sh'
        }
    }
}
