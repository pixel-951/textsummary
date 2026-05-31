terraform {
  required_version = ">= 1.6.0"

  required_providers {
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.63"
    }
  }
}

provider "hcloud" {
  token = var.hcloud_token
}

data "hcloud_ssh_key" "default" {
  name = var.existing_ssh_key_name
}

resource "hcloud_firewall" "web" {
  name = var.firewall_name

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = var.ssh_allowed_ips
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "80"
    source_ips = ["0.0.0.0/0", "::/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "443"
    source_ips = ["0.0.0.0/0", "::/0"]
  }
}

resource "hcloud_server" "app" {
  name        = var.server_name
  image       = "ubuntu-24.04"
  server_type = var.server_type
  location    = var.location

  ssh_keys = [
    data.hcloud_ssh_key.default.id
  ]

  firewall_ids = [
    hcloud_firewall.web.id
  ]

  user_data = file("${path.module}/cloud-init.yaml")
}