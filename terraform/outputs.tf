output "ip_publica" {
  description = "IP publica de la instancia EC2"
  value       = aws_instance.amg_ec2.public_ip
}

output "id_instancia" {
  description = "ID de la instancia"
  value       = aws_instance.amg_ec2.id
}

output "id_security_group" {
  description = "ID del Security Group"
  value       = aws_security_group.amg_sg.id
}