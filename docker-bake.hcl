group "default" {
  targets = [
    "yat"
  ]
}

target "yat" {
  tags = ["lookslikematrix/yat:latest"]
}
