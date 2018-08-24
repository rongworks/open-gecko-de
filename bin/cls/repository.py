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
