from flask import request
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_mail import Mail

from manage import create

from use_cases.mesh import MeshResult,MeshRequest,MeshYplus
from use_cases.airfoil import AirfoilResult
from use_cases.battery import BatteryResult
from use_cases.login import LoginResult, SignupResult, Activate
from use_cases.news import NewsResult
from use_cases.user import UserResult, UpdateResult, PasswordResult, PasswordReset, PasswordRestore
from use_cases.contact import ContactResponse
from use_cases.thrust import ThrustResult, TakeoffResult

app = create()

socketio = SocketIO(app)
CORS(app)
socketio.init_app(app, cors_allowed_origins="*")
mail = Mail(app)

@socketio.on('connect')
def connect():
    pass

@app.route('/news', methods=['GET'])
def news():
    uc = NewsResult()
    response = uc.execute()
    return response

@app.route('/airfoil', methods=['POST'])
def airfoil():
    params = request.get_json()
    uc = AirfoilResult(params)
    response = uc.execute()
    return response

@app.route('/battery', methods=['POST'])
def battery():
    params = request.get_json()
    uc = BatteryResult(params)
    response = uc.execute()
    return response

@app.route('/thrust', methods=['POST'])
def thrust():
    params = request.get_json()
    uc = ThrustResult(params)
    response = uc.execute()
    return response

@app.route('/takeoff', methods=['POST'])
def takeoff():
    params = request.get_json()
    uc = TakeoffResult(params)
    response = uc.execute()
    return response

@app.route('/mesh/result/<user>',methods=['POST'])
def mesh_result(user):
    params = request.get_json()
    uc = MeshResult(params, socketio, user)
    response = uc.execute()
    return response

@app.route('/mesh/yplus',methods=['POST'])
def mesh_yplus():
    params = request.get_json()
    uc = MeshYplus(params)
    response = uc.execute()
    return response

@app.route('/mesh', methods=['POST'])
def mesh():
    params = request.get_json()
    uc = MeshRequest(params)
    response = uc.execute()
    return response

@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    uc = LoginResult(params)
    response = uc.execute()
    return response

@app.route('/user', methods=['GET'])
def user():
    token = request.headers.get('Authorization')[7:]
    uc = UserResult(token)
    response = uc.execute()
    return response

@app.route('/update', methods=['POST'])
def update():
    token = request.headers.get('Authorization')[7:]
    params = request.get_json()
    uc = UpdateResult(params, token)
    response = uc.execute()
    return response

@app.route('/password', methods=['POST'])
def password():
    token = request.headers.get('Authorization')[7:]
    params = request.get_json()
    uc = PasswordResult(params, token)
    response = uc.execute()
    return response

@app.route('/password/reset', methods=['POST'])
def password_reset():
    params = request.get_json()
    uc = PasswordReset(params)
    response = uc.execute()
    return response

@app.route('/password/restore', methods=['POST'])
def password_restore():
    token = request.headers.get('Authorization')[7:]
    params = request.get_json()
    uc = PasswordRestore(params, token)
    response = uc.execute()
    return response

@app.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    uc = SignupResult(params)
    response = uc.execute()
    return response

@app.route('/activate', methods=['POST'])
def activate():
    token = request.headers.get('Authorization')[7:]
    uc = Activate(token)
    response = uc.execute()
    return response

@app.route('/contact', methods=['POST'])
def contact():
    params = request.get_json()
    uc = ContactResponse(params)
    response = uc.execute()
    return response    


if __name__ == '__main__':
    socketio.run(app,debug=True,port=8000,host='0.0.0.0')
