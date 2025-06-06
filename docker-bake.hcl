group "default" {
  targets = ["yat-pre-commit"]
}

target "yat-pre-commit" {
  context = "stages/pre-commit"
  tags = ["lookslikematrix/yat-pre-commit:latest"]
}
