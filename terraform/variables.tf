variable "aws_region" {
  description = "Região para criação os recursos aws"
  type        = string
  default     = "us-east-1"
}

variable "bucket_name" {
  description = "Nome do bucket"
  type        = string
  default     = "meu-data-lake-queimadas-nasa-2026"
}

variable "enviroment" {
  description = "Ambiente do projeto"
  type        = string
  default     = "dev"
}

variable "NASA_MAP_KEY" {
  description = "Chave de segurança da API NASA"
  type        = string
  sensitive   = true
}