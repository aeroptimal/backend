import json
from flask import Response

from repos.StaticThrustTakeOff import AircraftThrust, TakeOffRun

def Round(x):
    xx = []
    for i in x:
        try:
            xx.append(round(i,2))
        except:
            xx.append("")
    return xx
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
class TakeoffResult:
    def __init__(self, json):
        self.json = json

    def execute(self):
        mass = float(self.json['mass'])
        rrc = float(self.json['rrc'])
        p2 = float(self.json['p2'])
        S2 = float(self.json['S2'])
        Cltakeoff = float(self.json['Cltakeoff'])
        Clmax = float(self.json['Clmax'])
        Cd = float(self.json['Cd'])
        T1 = self.json['T1']
        T2 = self.json['T2']
        T3 = self.json['T3']
        T4 = self.json['T4']
        T5 = self.json['T5']
        Own = float(self.json['Own'])
        Town = self.json['Town']
        V0 = self.json['V0']
        T = float(self.json['T']) 
        Ts = int(self.json['Ts'])
        try:
            if Ts == 1:
                takeoff = TakeOffRun(mass,rrc,p2,S2,Cltakeoff,Clmax,Cd,[],Ts,[],[],[],[],[],[],[],T)
                names,xx,tt = takeoff.ComputeTakeOffRunStatic()
                data = {
                    "names": names,
                    "xx": xx,
                    "tt": tt,
                }
                return Response(response=json.dumps(data), status=200, mimetype='application/json')
            else:
                takeoff = TakeOffRun(mass,rrc,p2,S2,Cltakeoff,Clmax,Cd,Own,Ts,T1,T2,T3,T4,T5,Town,V0,0)
                names,xx,tt = takeoff.ComputeTakeOffRunDynamic()

                xx = Round(xx)
                tt = Round(tt)
                data = {
                    "names": names,
                    "xx": xx,
                    "tt": tt,
                }
                return Response(response=json.dumps(data), status=200, mimetype='application/json')
            
        except Exception as e:
            print(e)
            return Response(response=json.dumps({"error":"Computation failed"}), status=400, mimetype='application/json')
