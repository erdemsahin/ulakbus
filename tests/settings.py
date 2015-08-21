# -*-  coding: utf-8 -*-
"""
project settings for a pyoko based example project
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
import os

RIAK_SERVER = 'localhost'
RIAK_PROTOCOL = 'http'
RIAK_PORT = '8098'
REDIS_SERVER = os.getenv('REDIS_SERVER', '127.0.0.1:6379')
# MODELS_MODULE = '<PYTHON.PATH.OF.MODELS.MODULE>'
