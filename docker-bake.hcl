group "default" {
  targets = [
    "yat-pre-commit",
    "yat-software-composition-analysis"
  ]
}

variable "YAT_PREFIX" {
  default = "lookslikematrix/yat-"
}

target "yat-pre-commit" {
  context = "stages/pre-commit"
  tags = ["${YAT_PREFIX}pre-commit:latest"]
}

target "yat-software-composition-analysis" {
  context = "stages/software-composition-analysis"
  tags = ["${YAT_PREFIX}software-composition-analysis:latest"]
}
