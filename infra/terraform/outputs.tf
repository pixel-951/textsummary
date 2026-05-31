output "server_ipv4" {
  value = hcloud_server.app.ipv4_address
}

output "ssh_command" {
  value = "ssh root@${hcloud_server.app.ipv4_address}"
}