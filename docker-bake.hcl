group "default" {
  targets = ["yat-precommit"]
}

target "yat-precommit" {
  context = "stages/pre-commit"
  tags = ["yat-precommit:latest"]
  platforms = ["linux/amd64", "linux/arm64"]
}
