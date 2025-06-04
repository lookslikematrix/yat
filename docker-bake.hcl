group "default" {
  targets = ["yat-pre-commit"]
}

target "yat-pre-commit" {
  context = "stages/pre-commit"
  tags = ["yat-pre-commit:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
