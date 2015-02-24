# -*-  coding: utf-8 -*-
"""
We created a Falcon based WSGI server.
Integrated session support with beaker.
Then route all requests to workflow engine.

We process request and response objects for json data in middleware layer,
so activity methods (which will be invoked from workflow engine)
can read json data from request.context.in
and writeback to request.context.out

"""
# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from wsgiref import simple_server

from zengine.engine import ZEngine
from zaerp.zdispatch.conf import dispatcher_app

__author__ = 'Evren Esat Ozkan'


class WFEngine(ZEngine):
    def save_workflow(self):
        if 'workflows' in self.current.request.session:
            self.current.request.session['workflows'][self.current.workflow_name] = self.serialize_workflow()
            self.current.request.session.save()  # TODO: check if this is realy neccessary


class Connector(object):
    """
    this is a callable object to catch all requests and map them to workflow engine.
    domain.edu.tr/show_dashboard/blah/blah/x=2&y=1 will invoke a workflow named show_dashboard
    """
    # def __init__(self):
    # self.logger = logging.getLogger('dispatch.' + __name__)
    def __init__(self):
        engine_configuration = {
            ''
        }
        self.engine = ZEngine()

    def __call__(self, req, resp, wf_name):
        self.engine.set_current(request=req, response=resp, workflow_name=wf_name)
        self.engine.load_or_create_workflow()
        self.engine.run()


workflow_connector = Connector()
dispatcher_app.add_route('^(?P<wf_name>\w+)/', workflow_connector)


# Useful for debugging problems in your API; works with pdb.set_trace()
if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, dispatcher_app)
    httpd.serve_forever()
