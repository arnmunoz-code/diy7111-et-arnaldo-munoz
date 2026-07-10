variable "region" {
  description = "Región de AWS donde se despliega"
  type        = string
  default     = "us-east-1"
}

variable "tipo_instancia" {
  description = "Tipo de instancia EC2 (small según el encargo)"
  type        = string
  default     = "t3.small"
}

variable "key_name" {
  description = "Par de llaves existente en el Learner Lab"
  type        = string
  default     = "vockey"
}

variable "proyecto" {
  description = "Prefijo para nombrar los recursos"
  type        = string
  default     = "amg-vzeta"
}
