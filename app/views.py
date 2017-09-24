import datetime
from flask import request, Response
from flask_jwt import jwt_required, current_identity
from app import app
from app.models import Application, Log
from app.serializers import ApplicationSerializer, LogSerializer

# To authenticate make the following request:
# POST /auth HTTP/1.1
# Host: localhost:5000
# Content-Type: application/json
# Request Body:
# {
#     "username": "application_id",
#     "password": "application_secret"
# }
#
# And then apply JWT header for the next requests:
# GET /protected_endpoint HTTP/1.1
# Authorization: JWT eyJhbGciOiJ.IUzI1NiIsInR.5cCI6IkpXVCJ9

# Applications requests
@app.route('/applications', methods=['GET', 'POST'])
def applications():
    if request.method == 'GET':
        applications = Application.query.all()
        return ApplicationSerializer(applications).serialize()
    else:
        params = request.get_json()
        application = Application(name=params['name'], id=params['id'],
            secret=params['secret'], created_at=datetime.datetime.now())
        application.save()
        return ApplicationSerializer(application).serialize()

@app.route('/application', methods=['GET', 'DELETE'])
@jwt_required()
def application():
    application = Application.query.filter(Application.id == current_identity.id).first()
    if not(application):
        return Response("{'errors: ['Record not found']'}", status=404)
    if request.method == 'GET':
        return ApplicationSerializer(application, extra_fields=['secret']).serialize()
    else:
        application.remove()
        [log.remove() for log in Log.query.filter(Log.application_id == application.id).all()]
        return Response("{'status': 'deleted'}")


# Logs requests
@app.route('/logs', methods=['GET', 'POST'])
@jwt_required()
def logs():
    if request.method == 'GET':
        logs = Log.query.filter(Log.application_id == current_identity.id).all()
        return LogSerializer(logs).serialize()
    else:
        params = request.get_json()
        log = Log(application_id=current_identity.id, request=params['request'],
            ip_address=params['ip_address'], created_at=datetime.datetime.now())
        log.save()
        return LogSerializer(log).serialize()
