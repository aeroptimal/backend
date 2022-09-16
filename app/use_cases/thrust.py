import json
from flask import Response

from repos.StaticThrustTakeOff import AircraftThrust

class ThrustResult:
    def __init__(self, json):
        self.json = json

    def execute(self):
        p = float(self.json['p'])
        S = float(self.json['S'])
        Kv = float(self.json['Kv'])
        Cd = float(self.json['Cd'])
        V = float(self.json['V'])
        d = float(self.json['d'])
        P = float(self.json['P'])
        try:
            if self.json.get('Own'):
                Own = float(self.json['Own'])
                thrust = AircraftThrust(S,p,Cd,V,Kv,d,P,Own)
            else:
                Own = ''
                thrust = AircraftThrust(S,p,Cd,V,Kv,d,P,[])
            T1,T2,T3,T4,T5,Town,V0,MaxFlightVelocity = thrust.ComputeThrust()
            data = {
                "T1": T1,
                "T2": T2,
                "T3": T3,
                "T4": T4,
                "T5": T5,
                "Town": Town,
                "V0": V0,
                "MaxFlightVelocity": MaxFlightVelocity,
            }
            return Response(response=json.dumps(data), status=200, mimetype='application/json')
            
        except Exception as e:
            print(e)
            return Response(response=json.dumps({"error":"Computation failed"}), status=400, mimetype='application/json')
