/**
 * AWS S3 Storage Module for Vaultwarden Attachments
 * Author: Adrian Johnson <adrian207@gmail.com>
 */

# S3 Bucket for attachments
resource "aws_s3_bucket" "attachments" {
  bucket_prefix = "${var.name_prefix}-attachments-"
  
  tags = merge(
    var.tags,
    {
      Name = "${var.name_prefix}-attachments"
    }
  )
}

# Enable versioning
resource "aws_s3_bucket_versioning" "attachments" {
  bucket = aws_s3_bucket.attachments.id
  
  versioning_configuration {
    status = var.enable_versioning ? "Enabled" : "Suspended"
  }
}

# Enable encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "attachments" {
  bucket = aws_s3_bucket.attachments.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = var.enable_encryption ? "AES256" : "aws:kms"
    }
  }
}

# Block public access
resource "aws_s3_bucket_public_access_block" "attachments" {
  bucket = aws_s3_bucket.attachments.id
  
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "attachments" {
  count  = length(var.lifecycle_rules) > 0 ? 1 : 0
  bucket = aws_s3_bucket.attachments.id
  
  dynamic "rule" {
    for_each = var.lifecycle_rules
    content {
      id     = rule.value.id
      status = rule.value.enabled ? "Enabled" : "Disabled"
      
      transition {
        days          = rule.value.transition_days
        storage_class = rule.value.storage_class
      }
    }
  }
}

# CORS configuration (if needed)
resource "aws_s3_bucket_cors_configuration" "attachments" {
  count  = var.enable_cors ? 1 : 0
  bucket = aws_s3_bucket.attachments.id
  
  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

