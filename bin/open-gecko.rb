#!/bin/env ruby

class Installer
  #attr_accessor :commands, :infos

  # This will install Open Gecko to your local Machine
  # args:
  # * ladida
  # * ladida2
  def install(args)
    puts "Installing -- TODO: Not implemented"
    puts "TODO: Run ansible"
  end

  # Install to virtual Machine
  # Run vagrant and provision with ansible
  def vm_install(args)
    puts "Installing to Varant VM (Virtualbox) -- TODO: Check for Vagrant/Virtualbox"
    success = system("vagrant up --provision")
    puts "Succesfully installed Open Gecko to Vagrant VM" if success
  end

  # Here to help
  def help(args)
    opts = parse_options(args)
    command = opts[:sub_command] || ''
    puts "Help for: #{command}"
    puts "No command given" if command.length < 1
    topic = list.include?(command.to_sym) ? "\##{command}":''
    system('rdoc -r -o ri_docs')
    system("ri -d ri_docs Installer#{topic}")
  end

  private

  def list
    self.class.instance_methods(false)
  end

  def parse_options(options_arr)
    opts = { command: options_arr[0] }
    opts[:sub_command] = options_arr[1] unless options_arr.length < 2
    return opts
  end
end

installer = Installer.new
commands = Installer.instance_methods(false)
command = ARGV[0].to_sym

if commands.include?(command)
  installer.send(command, ARGV)
else
  puts "Command #{command} not recognized, commands: #{commands} \n run open-gecko.rb help <command> to learn more"
end
#execute ARGV[0]
