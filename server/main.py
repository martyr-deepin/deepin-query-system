import json
import re
import traceback

from flask import Flask
from flask import request
from flask.ext.cors import CORS

from lib.gerrit import Gerrit
from lib.repository import Repository
from lib.project_2_package import Project2Package
from lib.dtask import DTask


app = Flask(__name__)
CORS(app)


@app.route("/query")
def query():
    '''
    result = {
       "packages" : [
          {
             "deb_url" : "http://pools.corp...dde-launcher_3.0.12+r4~g4cd76c7_amd64.deb",
             "repo_codename" : "experimental",
             "repo_component" : "main",
             "version" : "3.0.12+r4~g4cd76c7",
             "repo_site" : "pools.corp.deepin.com"
          }
       ],
       "project" : "dde/dde-launcher",
       "commit" : "a1689d3c4e8502bf6f28c05d6cb28ae31cd94b2d",
       "bugzilla_url" : "https://bugzilla.deepin.io/show_bug.cgi?id=8703",
       "tower_url": "https://tower.im/projects/0/todos/e19f0428c01c490786f8c27acdf9a7d8"
    }
    '''
    try:
        result = {}

        if len(request.args):
            content = request.args.get('content')
        elif len(request.form):
            content = request.form.get('content')
        else:
            content = ''

        print(content)

        # cr
        r = re.compile('https://cr.deepin.io/#/c/\d+.*')
        if r.findall(content):
            print('info: it is a cr url')
            g = Gerrit()
            result = g.query(cl_link=content)

            # get package name from project name
            pro2pkg = Project2Package()
            pkg_name = pro2pkg.query(result.get('project'))
            result['package_name'] = pkg_name

            # get package info
            repo = Repository()
            packages = repo.query(pkg_name, result['commit'])
            result['packages'] = packages

            # get tower-link
            dtask = DTask()
            tower_url = dtask.get_tower_by_bugzilla(result['bugzilla_url'])
            result['tower_url'] = tower_url

        ret_json = {'failed': False, 'result': result}
        return json.dumps(ret_json)

    except Exception as e:
        print(traceback.format_exc())
        ret_json = {'failed': True, 'result': str(e)}
        return json.dumps(ret_json)
