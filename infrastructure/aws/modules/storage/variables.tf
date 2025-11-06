variable "name_prefix" {
  description = "Prefix for resource names"
  type        = string
}

variable "enable_versioning" {
  description = "Enable bucket versioning"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable server-side encryption"
  type        = bool
  default     = true
}

variable "enable_cors" {
  description = "Enable CORS configuration"
  type        = bool
  default     = false
}

variable "lifecycle_rules" {
  description = "S3 lifecycle rules"
  type = list(object({
    enabled         = bool
    id              = string
    transition_days = number
    storage_class   = string
  }))
  default = []
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {}
}

