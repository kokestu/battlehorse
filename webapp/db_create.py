# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 20:21:49 2015

@author: Jonathan
"""

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from app import db
import os.path

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, \
    api.version(SQLALCHEMY_MIGRATE_REPO))