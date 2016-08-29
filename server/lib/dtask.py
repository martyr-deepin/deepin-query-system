import re

import requests

from utils.singleton import Singleton

DTASK_BASE = 'https://tools.deepin.io/dtask'


class DTask(Singleton):

    def __init__(self):
        if hasattr(self, '_init'):
            return
        self._init = True

    def get_tower_by_bugzilla(self, bugzilla_url):
        tower_url = ''
        r = re.compile('https://bugzilla.deepin.io/show_bug.cgi\?id=(\d+)')
        l = r.findall(bugzilla_url)

        if len(l):
            bugzilla_id = l[0]
            url = '%s/links' % (DTASK_BASE)
            p = {
                'bugzilla': bugzilla_id,
                'tower_todo': '-'
            }
            r = requests.get(url, data=p)
            rs = r.json().get('result')
            if len(rs):
                todo_guid = rs[0]
                tower_url = 'https://tower.im/projects/0/todos/%s' % todo_guid

        return tower_url
