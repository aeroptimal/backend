import json
from flask_socketio import SocketIO
from flask import Response
from secrets import token_hex

from conf import settings

from repos.MeshGen import YplusCalculator

class MeshYplus:
    def __init__(self, json):
        self.json = json
    
    def execute(self):
        rho = self.json['rho']
        V = self.json['V']
        mu = self.json['mu']
        yplus = self.json['yplus']
        if not (0.1 <= V <= 340):
            return Response(response=json.dumps({"error":"Invalid input on Velocity"}), status=400, mimetype='application/json')
        if not (0 <= rho):
            return Response(response=json.dumps({"error":"Invalid input on Density"}), status=400, mimetype='application/json')
        if not (0 <= mu):
            return Response(response=json.dumps({"error":"Invalid input on Dynamic Viscosity"}), status=400, mimetype='application/json')
        if not (0 <= yplus):
            return Response(response=json.dumps({"error":"Invalid input on Y+"}), status=400, mimetype='application/json')
        
        repo = YplusCalculator(rho,V,mu,yplus)
        DeltaS = repo.ComputeDeltaS()
        data = {
            "DeltaS": DeltaS
        }
        return Response(response=json.dumps(data), status=200, mimetype='application/json')

class MeshResult:
    def __init__(self, params, socketio: SocketIO, user):
        self.params = params
        self.socketio = socketio
        self.user = user

    def execute(self):
        # msh = self.files['msh']
        # vtk = self.files['vtk']
        # su2 = self.files['su2']
        # foam = self.files['foam']
        # files = {
        #     "msh":base64.b64encode(msh.read()).decode('utf-8'),
        #     "vtk":base64.b64encode(vtk.read()).decode('utf-8'),
        #     "su2":base64.b64encode(su2.read()).decode('utf-8'),
        #     "foam":base64.b64encode(foam.read()).decode('utf-8'),
        # }

        status = self.params['status']

        if not status:
            self.socketio.emit(self.user,{'status':False})
        else:
            self.socketio.emit(self.user,self.params)
        return Response(json.dumps({}), status=200, mimetype='application/json')

class MeshRequest:
    def __init__(self, json):
        self.json = json

    def execute(self):
        file                = self.json['file']
        DomainHeight        = self.json['DomainHeight']
        WakeLength          = self.json['WakeLength']
        firstLayerHeight    = self.json['firstLayerHeight']
        growthRate          = self.json['growthRate']	
        MaxCellSize         = self.json['MaxCellSize']

        if not (10 <= DomainHeight <= 30):
            return Response(response=json.dumps({"error":"Invalid input on Domain Height"}), status=400, mimetype='application/json')
        if not (10 <= WakeLength <= 30):
            return Response(response=json.dumps({"error":"Invalid input on Wake Length"}), status=400, mimetype='application/json')
        if not (0.00001 <= firstLayerHeight <= 0.0005):
            return Response(response=json.dumps({"error":"Invalid input on First Layer Height"}), status=400, mimetype='application/json')
        if not (1.05 <= growthRate <= 1.2):
            return Response(response=json.dumps({"error":"Invalid input on Growth Rate"}), status=400, mimetype='application/json')
        if not (0.4 <= MaxCellSize <= 0.8):
            return Response(response=json.dumps({"error":"Invalid input on Max Cell Size"}), status=400, mimetype='application/json')
        
        
        id = token_hex(16)
        #%These Values can be played with to improve mesh quality
        BLHeight            = 0.1 #%0.1  %Fraction of chord length - Height of BL block
        LeadingEdgeGrading  = 1.8 #% 2 / 0.1 
        TrailingEdgeGrading = 0.8 #% 10
        inletGradingFactor  = 2.3 #% 0.5
        TrailingBlockAngle  = 5 #%20	%Degrees positive ang

        file = file.split(',')[-1]

        queue = settings.AWS_CLIENT.get_queue_by_name(QueueName=settings.OPENFOAM_QUEUE)
        msg = json.dumps({
            "file": file,
            "DomainHeight":DomainHeight,
            "WakeLength":WakeLength,
            "firstLayerHeight":firstLayerHeight,
            "growthRate":growthRate,
            "MaxCellSize":MaxCellSize,
            "BLHeight":BLHeight,
            "LeadingEdgeGrading":LeadingEdgeGrading,
            "TrailingEdgeGrading":TrailingEdgeGrading,
            "inletGradingFactor":inletGradingFactor,
            "TrailingBlockAngle":TrailingBlockAngle,
            "id":id
        })

        queue.send_message(MessageBody=msg)
        return Response(json.dumps({"id":id}), status=201, mimetype='application/json')