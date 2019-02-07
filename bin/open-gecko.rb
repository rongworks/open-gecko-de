#!/bin/env ruby

module Installer
  attr_accessor :commands, :infos

  def initialize
    self.commands = []
    self.infos = []
  end

  def command(name,description,&block)
    commands << {name:name.to_s,description:description,block:block}
  end

  def description(name, &block)
    infos << {name:name, block: block}
  end

  def command_names
    commands.collect {|c| c[:name]}
  end

  def execute(name)
    call_item(name,@commands)
  end

  def describe(name)
    call_item(name,@infos)
  end

  def call_item(name, collection)
    item = get_item(name.to_s,collection)
    if item.nil?
      puts "#{name} not found in #{command_names}"
    else
      item[:block].call
    end
  end

  def get_item(name, collection)
    c = collection.select {|c| c[:name] == name}.first
    return c
  end

end

#installer = Installer.new

include Installer
initialize

command :help, 'Show help' do
  puts "I am the help command"
end

description :help do
  puts "I am the description of help"
end

command :install, 'Install' do
  puts "Something else"
end

command :update, 'Update' do
  puts "update"
end

execute ARGV[0]
