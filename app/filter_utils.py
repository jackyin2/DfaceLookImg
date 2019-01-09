# -*- coding:utf-8 -*-

from flask_script import Manager
from app import app

manager = Manager(app)


def qiepian(str, index):
    length = len(str)
    return str[index:length]
def pingjie(str, strP):
    return strP+str

env = app.jinja_env
env.filters['qiepian'] = qiepian
env.filters['pingjie'] = pingjie


if __name__ == "__main__":
    manager.run()







