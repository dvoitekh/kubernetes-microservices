import datetime
import uuid
import requests

from flask import request, Response
from functools import wraps

from app import app
from app.models import Application, Log, User
from app.serializers import ApplicationSerializer, LogSerializer


def render_response(body, status):
    return Response(str(body), status=status)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = requests.get(f"{app.config['AUTH_HOST']}/check_login",
                                headers={'Authorization': dict(request.headers).get('Authorization')})
        body = response.json()
        if response.status_code != 200:
            return render_response(body, response.status_code)

        current_user = User.find_by(_id=body['user_id'])
        if current_user is None:
            return render_response({'error': 'User not found'}, 404)
        return f(current_user, *args, **kwargs)
    return decorated_function


# Applications requests
@app.route('/applications', methods=['GET', 'POST'])
@login_required
def applications(current_user):
    if request.method == 'GET':
        applications = Application.where(user_id=current_user._id)
        return ApplicationSerializer(applications).serialize()
    else:
        params = request.get_json()
        application = Application.create(name=params['name'], _id=Application.count() + 1,
                                         secret=uuid.uuid4().hex,
                                         user_id=current_user._id,
                                         created_at=datetime.datetime.now())
        return ApplicationSerializer(application).serialize()


@app.route('/application/<application_id>', methods=['GET', 'DELETE'])
@login_required
def application(current_user, application_id):
    application_id = int(application_id)
    application = Application.find_by(user_id=current_user._id, _id=application_id)
    if application is None:
        return Response("{'errors: ['Record not found']'}", status=404)
    if request.method == 'GET':
        return ApplicationSerializer(application, extra_fields=['secret']).serialize()
    else:
        application.remove()
        Log.remove(application_id=application._id)
        return Response("{'status': 'deleted'}")


# Logs requests
@app.route('/logs/<application_id>', methods=['GET', 'POST'])
@login_required
def logs(current_user, application_id):
    application_id = int(application_id)
    application = Application.find_by(user_id=current_user._id,
                                      _id=application_id)
    if application is None:
        return Response("{'errors: ['Record not found']'}", status=404)
    if request.method == 'GET':
        logs = Log.where(application_id=application_id)
        return LogSerializer(logs).serialize()
    else:
        params = request.get_json()
        log = Log.create(_id=Log.count() + 1,
                         application_id=application_id,
                         request=params['request'],
                         ip_address=params['ip_address'],
                         created_at=datetime.datetime.now())
        return LogSerializer(log).serialize()
