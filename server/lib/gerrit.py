import json
import re

import requests

from utils.singleton import Singleton

GERRIT_BASE = 'https://cr.deepin.io'


class Gerrit(Singleton):

    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True

    def __get_json(self, path):
        url = '%s%s' % (GERRIT_BASE, path)
        r = requests.get(url)
        text = r.text.lstrip(')]}\'\n')  # remove magic word
        data = json.loads(text)

        return data

    def query(self, cl_link=None, change_num=None):
        result = {}

        if cl_link:
            r = re.compile('https://cr.deepin.io/#/c/(\w+).*')
            l = r.findall(cl_link)

            if not len(l):
                err = 'not a cr link: %s' % cl_link
                raise Exception(err)

            change_num = int(l[0])

        if change_num:
            change_num = int(change_num)

        d = self.__get_json('/changes/%d?o=current_revision' % change_num)
        commit = d.get('current_revision')
        project = d.get('project')
        result['commit'] = commit
        result['project'] = project

        d = self.__get_json('/changes/%d?o=CURRENT_REVISION&o=COMMIT_FOOTERS' % change_num)
        commit_msg = d.get('revisions').get(commit).get('commit_with_footers')
        r = re.compile('(https://bugzilla.deepin.io/show_bug.cgi\?id=\d+)')
        l = r.findall(commit_msg)

        if len(l):
            result['bugzilla_url'] = l[0]
        else:
            result['bugzilla_url'] = ''

        return result
