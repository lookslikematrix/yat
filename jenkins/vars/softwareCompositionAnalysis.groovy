def call(Map config = [:]) {
    String sourceDirectory = config.get('sourceDirectory', '')
    String yatReleaseName = config.get('yatReleaseName', '')
    String yatReleaseVersion = config.get('yatReleaseVersion', '')
    String yatOutputDirectory = config.get('yatOutputDirectory', '')
    script {
        def String image_name = "yat-software-composition-analysis:latest"
        def String[] files = [
            "software-composition-analysis/Dockerfile",
            "software-composition-analysis/run.sh",
            "software-composition-analysis/yat.yml"
        ]

        for(file in files) {
            fileContent = libraryResource file
            writeFile(
                file: ".yat/" + file,
                text: fileContent
            )
        }

        dir(".yat/software-composition-analysis") {
            docker.build(image_name)
        }

        def String[] environment_variables = [
            "SOURCE_DIRECTORY=${sourceDirectory}",
            "YAT_RELEASE_NAME=${yatReleaseName}",
            "YAT_RELEASE_VERSION=${yatReleaseVersion}",
            "YAT_OUTPUT_DIRECTORY=${yatOutputDirectory}"
        ]
        String environment_arguments = ""
        for (environment_variable in environment_variables) {
            environment_arguments += "--env ${environment_variable} "
        }

        docker.image(image_name).inside(environment_arguments){
            sh '/bin/sh /.yat/run.sh'
        }

        archiveArtifacts(
             artifacts: "${yatOutputDirectory}*${yatReleaseName}_${yatReleaseVersion}.cyclondx.json"
        )
    }
}
