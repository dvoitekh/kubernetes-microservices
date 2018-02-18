import datetime
import uuid

from flask import request, Response
from flask_jwt import jwt_required, current_identity

from app import app
from app.models import Application, Log, User
from app.serializers import ApplicationSerializer, LogSerializer, UserSerializer

# First create user:
# POST /users endpoint
# Host: localhost:5000
# Content-Type: application/json
# Request Body:
# {
#     "username": "user@example.com",
#     "password": "passw_1234"
# }
#
# Then to authenticate make the following request:
# POST /auth HTTP/1.1
# Host: localhost:5000
# Content-Type: application/json
# Request Body:
# {
#     "username": "user@example.com",
#     "password": "passw_1234"
# }
#
# And then apply JWT header for the next requests:
# GET /protected_endpoint HTTP/1.1
# Authorization: JWT eyJhbGciOiJ.IUzI1NiIsInR.5cCI6IkpXVCJ9


@app.route('/users', methods=['POST'])
def users():
    params = request.get_json()
    users_count = len(User.query.all())
    user = User(id=users_count + 1, username=params['username'],
                password=params['password'], created_at=datetime.datetime.now())
    user.save()
    return UserSerializer(user).serialize()


# Applications requests
@app.route('/applications', methods=['GET', 'POST'])
@jwt_required()
def applications():
    if request.method == 'GET':
        applications = Application.query.filter(Application.user_id == current_identity.id).all()
        return ApplicationSerializer(applications).serialize()
    else:
        params = request.get_json()
        application = Application(name=params['name'], id=params['id'],
                                  secret=uuid.uuid4().hex,
                                  user_id=current_identity.id,
                                  created_at=datetime.datetime.now())
        application.save()
        return ApplicationSerializer(application).serialize()


@app.route('/application/<application_id>', methods=['GET', 'DELETE'])
@jwt_required()
def application(application_id):
    application = Application.query.filter(Application.user_id == current_identity.id and
                                           Application.id == application_id).first()
    if not(application):
        return Response("{'errors: ['Record not found']'}", status=404)
    if request.method == 'GET':
        return ApplicationSerializer(application, extra_fields=['secret']).serialize()
    else:
        application.remove()
        for log in Log.query.filter(Log.application_id == application.id).all():
            log.remove()
        return Response("{'status': 'deleted'}")


# Logs requests
@app.route('/logs/<application_id>', methods=['GET', 'POST'])
@jwt_required()
def logs(application_id):
    application = Application.query.filter(Application.user_id == current_identity.id and
                                           Application.id == application_id).first()
    if not(application):
        return Response("{'errors: ['Record not found']'}", status=404)
    if request.method == 'GET':
        logs = Log.query.filter(Log.application_id == application_id).all()
        return LogSerializer(logs).serialize()
    else:
        params = request.get_json()
        log = Log(application_id=application_id, request=params['request'],
                  ip_address=params['ip_address'],
                  created_at=datetime.datetime.now())
        log.save()
        return LogSerializer(log).serialize()
