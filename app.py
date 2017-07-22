'''
    FLASK API
    ---------
    This provides an API for the GTDM guild to manage events.
'''

import flask
import flask_sqlalchemy
import flask_restless
import config
from time import time

app = flask.Flask(__name__)
app.config['DEBUG'] = config.DEBUG
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
db = flask_sqlalchemy.SQLAlchemy(app)

access_passwords = ['ccIf5$xzAA9(AXJ(`a4R\eF~@BB3S_X8', 'Q>jL:8h>cu2k>#,2f$N~p$nHYBBFpY/T']

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    type = db.Column(db.Integer)
    name = db.Column(db.Unicode, nullable=False)
    location = db.Column(db.Unicode)
    host = db.Column(db.Unicode(80))
    time = db.Column(db.Integer)
    autoremove = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<Event {}>'.format(self.name)


class Type(db.Model):
    type = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.Unicode, nullable=False)

    def __repr__(self):
        return '<Event Type {}>'.format(self.name)

db.create_all()

def auth_func(**kwargs):
    if flask.request.headers.get('X-Secret-Key', '') not in access_passwords:
        raise flask_restless.ProcessingException(description='Not authenticated!', code=401)


def expire_func(**kwargs):
    timestamp = int(time()) #current time
    Event.query.filter(Event.time < timestamp - 86400,
                       Event.autoremove == True).delete()  # check for items older than 24 hours
    db.session.commit()  # commit to the database


def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db, preprocessors=dict(POST=[auth_func], PATCH_SINGLE=[auth_func], DELETE_SINGLE=[auth_func]))

manager.create_api(Event, methods=['GET', 'POST', 'PATCH', 'DELETE'],
                             preprocessors=dict(GET_MANY=[expire_func]))
manager.create_api(Type,  methods=['GET', 'POST', 'PATCH', 'DELETE'])

app.after_request(add_cors_headers)

if __name__ == '__main__':
    app.run()
