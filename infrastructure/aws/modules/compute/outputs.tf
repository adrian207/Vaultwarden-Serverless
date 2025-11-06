output "cluster_name" {
  value = aws_ecs_cluster.main.name
}

output "cluster_arn" {
  value = aws_ecs_cluster.main.arn
}

output "service_name" {
  value = aws_ecs_service.main.name
}

output "service_id" {
  value = aws_ecs_service.main.id
}

output "alb_dns_name" {
  value = aws_lb.main.dns_name
}

output "alb_zone_id" {
  value = aws_lb.main.zone_id
}

output "alb_arn" {
  value = aws_lb.main.arn
}

output "ecs_security_group_id" {
  value = aws_security_group.ecs_tasks.id
}

output "alb_security_group_id" {
  value = aws_security_group.alb.id
}

