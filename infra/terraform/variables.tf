variable "hcloud_token" {
  description = "Hetzner Cloud API token"
  type        = string
  sensitive   = true
}

variable "existing_ssh_key_name" {
  description = "Name of an existing SSH key in Hetzner Cloud"
  type        = string
}

variable "server_name" {
  description = "Name of the Hetzner server"
  type        = string
  default     = "textsummary-prod"
}

variable "server_type" {
  description = "Hetzner server type"
  type        = string
  default     = "ccx23"
}

variable "location" {
  description = "Hetzner location"
  type        = string
  default     = "fsn1"
}

variable "firewall_name" {
  description = "Name of the Hetzner firewall"
  type        = string
  default     = "textsummary-terraform-firewall"
}

variable "ssh_allowed_ips" {
  description = "CIDR blocks allowed to SSH into the server"
  type        = list(string)
  default     = ["0.0.0.0/0", "::/0"]
}