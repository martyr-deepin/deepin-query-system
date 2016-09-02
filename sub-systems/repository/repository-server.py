#!/usr/bin/python3

import json

import apt
from flask import Flask
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

app = Flask(__name__)


class RepositoryServer:

    def __init__(self):
        self.cache = apt.cache.Cache()
        self.cache.update()

    def query(self, package):
        results = []
        p = self.cache[package]
        for v in p.versions:
            uri_index = 0

            for origin in v.origins:
                if origin.archive == 'now':
                    continue

                version = {}
                version['version'] = v.version
                version['deb_url'] = v.uris[uri_index]
                version['repo_url'] = version['deb_url'].split(v.filename)[0].rstrip('/')
                version['repo_codename'] = origin.codename
                version['repo_component'] = origin.component
                version['shell'] = self.__construct_shell(package, **version)
                results.append(version)
                uri_index += 1

        return results

    def __construct_shell(self, pkg_name, **kwargs):
        repo_url = kwargs.get('repo_url')
        codename = kwargs.get('repo_codename')
        component = kwargs.get('repo_component')
        pkg_version = kwargs.get('version')

        shell = "echo 'deb {repo_url} {codename} {component}' | sudo tee -a /etc/apt/sources.list\nsudo apt-get update\nsudo apt-get install {pkg_name}={pkg_version}"\
                .format(**{
                     'repo_url': repo_url,
                     'codename': codename,
                     'component': component,
                     'pkg_name': pkg_name,
                     'pkg_version': pkg_version
                 })

        return shell


@app.route('/repo/package/<string:name>', methods=['GET'])
def package(name):
    repo = RepositoryServer()
    result = repo.query(name)
    ret = {'failed': False, 'result': result}
    return json.dumps(ret)


if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(8080)
    IOLoop.instance().start()
