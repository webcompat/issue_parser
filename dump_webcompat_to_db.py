#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from extract_id_title_url import get_webcompat_data
from db import db_session
import json

DB_PATH = 'sqlite:////tmp/test.db'

Base = declarative_base()
Base.query = db_session.query_property()


class Issue(Base):
    '''Issue database class.'''
    __tablename__ = 'webcompat_issues'
    id = Column(String(128), unique=True, primary_key=True)
    summary = Column(String(256))
    url = Column(String(1024))
    body = Column(String(2048))

    def __init__(self, id, summary, url, body):
        self.id = id
        self.summary = summary
        self.url = url
        self.body = body


def main():
    '''Core program.'''
    engine = create_engine(DB_PATH, convert_unicode=True)
    Base.metadata.create_all(bind=engine)
    live = False
    if live:
        data = get_webcompat_data()[1]
    else:
        f = open('webcompatdata-bzlike.json', 'r')
        data = json.load(f)
        f.close()
    # stuff data into database..
    for bug in data['bugs']:
        db_session.add(
            Issue(bug['id'], bug['summary'], bug['url'], bug['body']))
    db_session.commit()


if __name__ == "__main__":
    main()
