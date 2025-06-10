def call(Map config = [:]) {
    String sourceDirectory = config.get('sourceDirectory', '')
    String yatReleaseName = config.get('yatReleaseName', '')
    String yatReleaseVersion = config.get('yatReleaseVersion', '')
    String yatOutputDirectory = config.get('yatOutputDirectory', '')
    script {
        String environment_arguments = "" +
          "--env SOURCE_DIRECTORY=${sourceDirectory} " +
          "--env YAT_RELEASE_NAME=${yatReleaseName} " +
          "--env YAT_RELEASE_VERSION=${yatReleaseVersion} " +
          "--env YAT_OUTPUT_DIRECTORY=${yatOutputDirectory} "

        docker.image("lookslikematrix/yat-software-composition-analysis:latest").inside(environment_arguments){
            sh '/bin/sh /.yat/run.sh'
        }
        archiveArtifacts(
             artifacts: "${yatOutputDirectory}*.cyclondx.json"
        )
    }
}
