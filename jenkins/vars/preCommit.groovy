def call(Map config = [:]) {
    String target_branch = config.get('target_branch', 'origin/main')
    script {
        String environment_arguments = "" +
          "--env TARGET_BRANCH=${target_branch}"

        docker.image("lookslikematrix/yat-pre-commit:latest").inside(environment_arguments){
            sh '/bin/sh /.yat/run.sh'
        }
    }
}
