Vagrant.configure("2") do |config|
  config.vm.box = "archlinux/archlinux"

  config.vm.provision "shell",
    inline: "pacman -Su python3 rsync --needed --noconfirm"

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "ansible/open-gecko-base.yml"
    ansible.extra_vars = {
      ansible_python_interpreter: "/usr/bin/python3",
   }

  end
end
