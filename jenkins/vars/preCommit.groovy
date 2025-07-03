def call(Map config = [:]) {
    String target_branch = config.get('target_branch', 'origin/main')
    script {
        def String image_name = "yat-pre-commit:latest"
        def String[] files = [
            "pre-commit/Dockerfile",
            "pre-commit/run.sh",
            "pre-commit/yat.yml"
        ]

        for(file in files) {
            fileContent = libraryResource file
            writeFile(
                file: ".yat/" + file,
                text: fileContent
            )
        }

        dir(".yat/pre-commit") {
            docker.build(image_name)
        }

        def String[] environment_variables = [
            "TARGET_BRANCH=${target_branch}"
        ]
        String environment_arguments = ""
        for (environment_variable in environment_variables) {
            environment_arguments += "--env ${environment_variable} "
        }

        docker.image(image_name).inside(environment_arguments){
            sh '/bin/sh /.yat/run.sh'
        }
    }
}
