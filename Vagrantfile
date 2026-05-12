# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-21.10"
  config.vm.hostname = "k3s"
  config.vm.network "private_network", ip: "192.168.50.4"

  config.vm.provision "shell", inline: <<-SHELL
    curl -sfL https://get.k3s.io | sh -
    # Give kubeconfig read access
    chmod 644 /etc/rancher/k3s/k3s.yaml
  SHELL

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = 2
  end
end
