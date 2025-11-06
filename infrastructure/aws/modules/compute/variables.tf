variable "name_prefix" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "private_subnet_ids" {
  type = list(string)
}

variable "public_subnet_ids" {
  type = list(string)
}

variable "container_image" {
  type = string
}

variable "container_port" {
  type = number
}

variable "container_cpu" {
  type = number
}

variable "container_memory" {
  type = number
}

variable "desired_count" {
  type = number
}

variable "min_capacity" {
  type = number
}

variable "max_capacity" {
  type = number
}

variable "environment_variables" {
  type = map(string)
}

variable "secrets" {
  type    = list(map(string))
  default = []
}

variable "health_check_path" {
  type = string
}

variable "health_check_interval" {
  type = number
}

variable "certificate_arn" {
  type = string
}

variable "domain_name" {
  type = string
}

variable "enable_autoscaling" {
  type = bool
}

variable "cpu_threshold" {
  type = number
}

variable "memory_threshold" {
  type = number
}

variable "s3_bucket_arn" {
  type = string
}

variable "enable_deletion_protection" {
  type    = bool
  default = false
}

variable "tags" {
  type = map(string)
}

