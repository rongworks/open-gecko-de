from cls.repository import Repository
from cls.package import Package
from cls.custom_file import CustomFile

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

    def read_files(self):
        custom_files = []
        filekey = 'custom_files'
        for cfile in self.data.get(filekey):
            cf = CustomFile()
            cf.src = self.data[filekey][cfile]['src']
            cf.dst = self.data[filekey][cfile]['dst']
            custom_files.append(cf)
        return custom_files
