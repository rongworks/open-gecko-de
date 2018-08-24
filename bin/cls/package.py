import io
import os
import sys
import shutil
import subprocess
import errno

from cls.repository import Repository

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
      #TODO: dry option is gone
      if len(self.config) <= 0:
          return
      user_home = os.environ.get('HOME','')
      conf_path = self.config.replace('~',user_home,1).replace('$HOME',user_home)
      dist_path = '../dist/packages'+self.config.replace('~','',1).replace('$HOME','')

      src = dist_path
      dst = conf_path

      if reverse == True:
          src = conf_path
          dst = dist_path


      if not dry:
          dsc=''
          if os.path.isdir(src):
              self.copydir(src, dst)
          else:
              try:
                  os.makedirs(os.path.dirname(dst))
              except OSError as e:
                  if e.errno != errno.EEXIST:
                      raise
              #dst = os.path.join(dst, os.path.basename(conf_path))
              shutil.copy2(src,dst)
      else:
        dsc = "(dry): "
      print(dsc+"copy files "+src+" to "+dst)


  def as_string(self):
      return ", ".join((self.name,self.category,self.info))
