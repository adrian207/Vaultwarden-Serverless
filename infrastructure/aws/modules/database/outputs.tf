output "cluster_identifier" {
  description = "Cluster identifier"
  value       = aws_rds_cluster.main.id
}

output "cluster_endpoint" {
  description = "Cluster writer endpoint"
  value       = aws_rds_cluster.main.endpoint
}

output "reader_endpoint" {
  description = "Cluster reader endpoint"
  value       = aws_rds_cluster.main.reader_endpoint
}

output "cluster_arn" {
  description = "Cluster ARN"
  value       = aws_rds_cluster.main.arn
}

output "master_password" {
  description = "Master password"
  value       = random_password.master_password.result
  sensitive   = true
}

output "security_group_id" {
  description = "Security group ID"
  value       = aws_security_group.rds.id
}

