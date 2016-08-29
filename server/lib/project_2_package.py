import os

from utils.singleton import Singleton

MAP = {
    'dde/dde-launcher': 'dde-launcher'
}


class Project2Package(Singleton):

    def __init__(self):
        pass

    def __default(self, project):
        return os.path.basename(project)

    def query(self, project):
        package = MAP.get(project)

        if package is None:
            package = self.__default(project)

        return package
