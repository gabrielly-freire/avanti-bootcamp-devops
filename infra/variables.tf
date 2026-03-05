variable "app_name" {
  type    = string
  default = "farmacia-app-dev"
}

variable "service_name" {
  type    = string
  default = "farmacia"
}

variable "instance_type" {
  type    = string
  default = "free"
}

variable "container_port" {
  type    = number
  default = 5000
}

variable "docker_image_name" {
  type    = string
  default = "gabriellyfreire/farmacia-app"
}

variable "docker_image_tag" {
  type    = string
  default = "latest"
}
  