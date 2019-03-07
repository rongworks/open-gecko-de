#!/bin/env ruby
require 'yaml'

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

  def add_package(args)
    pkg = args[:sub_command] || ''
    conf_path = args['-c'] || ask('config_path')
    #category = opts[:category] || ask('category')
    config = YAML.load_file('../ansible/vars/pkg_base.yml')
    pak = {name:pkg}
    pak['conf_path'] = conf_path if conf_path.length > 0
    #pak['category'] = category if category.length > 0
    puts config
    config['open_gecko_packages'] << pak
    File.open("../conf/pkg_custom.yml", "w") { |file| file.write(config.to_yaml) }
    puts config


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
    command = args[:sub_command] || ''
    puts "Help for: #{command}"
    puts "No command given" if command.length < 1
    topic = commands.include?(command.to_sym) ? "\##{command}":''
    system('rdoc -r -o ri_docs')
    system("ri -d ri_docs Installer#{topic}")
  end

  private

  def ask(question)
    puts question+':'
    STDIN.gets.chomp
  end

  def commands
    self.class.instance_methods(false)
  end

end

def extract_option(array, option, single_key = false)
  result = {}
  if idx = array.index(option)
    if single_key
      result[option] = true
      array.delete_at(idx)
    elsif array.length > idx
      #puts "deleting #{array[idx]}, #{array[idx+1]}"
      result[option] = array[idx+1]
      array.delete_at(idx)
      array.delete_at(idx)
    else
      raise ArgumentError("Malformed argument at #{option}")
    end
  end
  return {args: array, options: result}
end

def parse_options(options_arr)
  opts = {}
  args = options_arr
  %w(-f --force hui).each do |key|
    extraction = extract_option(args, key, true)
    #puts "Extraxt key: #{key} -opts = #{opts}"
    args = extraction[:args]
    opts.merge!(extraction[:options])
  end
  %w(-c).each do |key|
    extraction = extract_option(args, key, false)
    args = extraction[:args]
    opts.merge!(extraction[:options])
  end
  puts "#{args} options: #{opts}"
  opts[:command] = args[0]
  opts[:sub_command] = args[1] unless options_arr.length < 2
  puts "Arguments: #{opts}"
  return opts
end

installer = Installer.new
commands = Installer.instance_methods(false)
args = parse_options(ARGV)
command = args[:command]

if commands.include?(command.to_sym)
  installer.send(command, args)
else
  puts "Command #{command} not recognized, commands: #{commands} \n run open-gecko.rb help <command> to learn more"
end
#execute ARGV[0]
