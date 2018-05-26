# -*- coding: utf-8 -*-
import yaml
import io
import os
import sys
import shutil
import subprocess
import argparse

class Package:

  def __init__(self):
    self.name = ""
    self.repository = None
    self.category = "undefined"
    self.url = ""
    self.info = "A package"
    self.config = ""
    self.selected = False
    self.single_file = False

  def install(self,dry=False):
      cmd = self.repository.command +' '+ self.name
      if self.selected:
          if dry:
            print(cmd)
          else:
            subprocess.call(cmd.split(' '))
          self.copy_config(dry)



  def prepare_config(self,dry=True):
      self.copy_config(dry,True)

  def copydir(self, src, dest, ignore=None):
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                self.copydir(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

  def copy_config(self,dry=False,reverse=False):
      if len(self.config) <= 0:
          return
      user_home = os.environ.get('HOME','')
      conf_path = self.config.replace('~',user_home,1).replace('$HOME',user_home)
      dist_path = '../dist/packages/'+self.name

      src = os.path.join(dist_path, os.path.basename(conf_path))
      dst = conf_path

      if reverse == True:
          src = conf_path
          dst = os.path.join(dist_path, os.path.basename(conf_path))
      print("copy files "+src+" to "+dst)
      if os.path.isdir(src):
          self.copydir(src, dst)
      else:
          try:
              os.makedirs(os.path.dirname(dst))
          except OSError as e:
              if e.errno != os.errno.EEXIST:
                  raise
          #dst = os.path.join(dst, os.path.basename(conf_path))
          shutil.copy2(src,dst)

  def as_string(self):
      return ", ".join((self.name,self.category,self.info))

class Repository:

  def __init__(self):
      self.name = ""
      self.command = ""
      self.info = ""
      self.child_packages = []

  def as_string(self):
      return ", ".join((self.name,self.command,self.info))

  def list(self):
      str = self.name + ": \n"
      for package in self.child_packages:
          str += package.as_string() + "\n"
      return str

  def addpkg(self,pkg):
      self.child_packages.append(pkg)


class Parser:

    def __init__(self,data):
        self.data = data

    def repositories_from_yaml(self):
        key = 'repositories'
        repositories = []
        data = self.data
        for rkey in data[key]:
            repo = self.build_repo(rkey,data[key][rkey])
            repositories.append(repo)
        return repositories

    def read_packages(self):
        data = self.data
        pkg_key = 'packages'
        repo_key = 'repositories'
        repositories = {}
        for repo in data.get(repo_key):
            if repo not in repositories:
                repositories[repo] = self.build_repo(repo,data[repo_key][repo])
        packages = []
        for pkg in data[pkg_key]:
            package = self.build_package(pkg,data[pkg_key][pkg],repositories)
            packages.append(package)
            package.repository.addpkg(package)
        return packages

    def build_repo(self,name,data):
        repository = Repository()
        repository.name = name
        repository.command = data.get('command','')
        repository.info = data.get('info','')
        return repository

    def build_package(self,name,data,repositories):
        package = Package()
        package.name = name
        package.repository = repositories.get(data.get('repository'))
        package.category = data.get('category','')
        package.url = data.get('url','')
        package.info = data.get('info','')
        package.config = data.get('config','')
        package.selected = data.get('selected',False)
        return package

class InstallManager:

    def __init__(self):
        self.packages = []
        self.repositories = []
        self.categories = {}

    def parse_config(self,file):
        with open(file, 'r') as stream:
            data_loaded = yaml.load(stream)
            #print(data_loaded)
            #print("---------")

        parser = Parser(data_loaded)
        #repositories = repositories_from_yaml(data_loaded)
        self.packages = parser.read_packages()

        for package in self.packages:
            if not package.category in self.categories:
                self.categories[package.category] = [package]
            else:
                self.categories[package.category].append(package)

    def list_categories(self):
        for ckey in self.categories:
            cat_pkgs = self.categories[ckey]
            print("===== "+ckey+" =====")
            for package in cat_pkgs:
                print(package.as_string())

    def install_packages(self):
        installable = ["system"]
        for ckey in self.categories:
            if ckey in "system" or input("Install packages from category: "+ckey+"? (yes/no)") in ["y","yes"]:
                installable.append(ckey)
        for ikey in installable:
            cat_pkgs = self.categories[ikey]
            for package in cat_pkgs:
                package.install()

    def prepare_config(self,dry):
        for package in self.packages:
            if package.selected == True:
                package.prepare_config(dry)

# Main
user_home = os.environ.get('HOME','')
app_name = 'Open Gecko DE'
version = '0.4.0'
description = "Installer script for installing custom OpenBox-Desktop\n \
  usage: open-gecko.py COMMAND [PATH]\n \
  COMMANDS: \n \
    info = show this text \n \
    categories = list categories and packages \n \
    install = Install "+app_name+ "\n \
  PATH: \n \
    path = path to config file"

pkg_file = '../conf/packages.yml'

def info():
    print(app_name)
    print(version)
    print(description)
    print('config: '+pkg_file)

def list_categories():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.list_categories()

def install():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.install_packages()
def prepare_config():
    install_manager = InstallManager()
    install_manager.parse_config(pkg_file)
    install_manager.prepare_config(True)

command = 'info'
if len(sys.argv) > 1:
    command = command = sys.argv[1]
    if len(sys.argv) > 2:
        pkg_file = sys.argv[2]

if command == 'info':
    info()
elif command == 'categories':
    list_categories()
elif command == 'install':
    install()
    subprocess.call(['sudo','cp','../dist/open-gecko.desktop','/usr/share/xsessions/open-gecko.desktop'])
elif command == 'prepare_config':
    prepare_config()
else:
   print("Wrong arguments")
   info()
