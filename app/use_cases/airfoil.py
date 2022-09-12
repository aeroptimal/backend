from flask import Response
import json
import base64
from io import StringIO

from repos.AirfoilRoutine import AirfoilOpt

class AirfoilResult:
    def __init__(self, json):
        self.json = json

    def execute(self):
        cl = self.json['cl']
        Re = self.json['Re']
        xf = self.json['xf']
        n = int(self.json['n'])
        if not (0.2 <= cl <= 1.8):
            return Response(response=json.dumps({"error":"Invalid input on Lift Coefficient"}), status=400, mimetype='application/json')
        if not (80000 <= Re <= 500000):
            return Response(response=json.dumps({"error":"Invalid input on Reynolds Number"}), status=400, mimetype='application/json')
        if not (1 <= xf <= 2):
            return Response(response=json.dumps({"error":"Invalid input on Metodology"}), status=400, mimetype='application/json')
        if not (50 <= n <= 500):
            return Response(response=json.dumps({"error":"Invalid input on Number of Points"}), status=400, mimetype='application/json')
        repo = AirfoilOpt(cl, Re, xf)
        t, m, p, a, e, filename = repo.ComputeOpt()
        x,y = repo.Coordinates(n)
        dat = ''
        f = StringIO()
        for i in range(len(x)):
            dat = dat + "%0.5f    %0.5f\n" %(x[i],y[i])
            f.write("%0.5f    %0.5f\n" %(x[i],y[i]))
        dat_file = base64.b64encode(f.getvalue().encode('utf-8')).decode('utf-8')

        CSV = ''
        g = StringIO()
        for i in range(len(x)):
            CSV = CSV + str(round(x[i],5)) + ',' + str(round(y[i],5)) + '\n'
            g.write(str(round(x[i],5)) + ',' + str(round(y[i],5)) + '\n')
        csv_file = base64.b64encode(g.getvalue().encode('utf-8')).decode('utf-8')
        data = {
            "t": t,
            "m": m,
            "p": p,
            "a": a,
            "e": e,
            "filename": filename,
            "x": x,
            "y": y,
            "dat": dat_file,
            "csv": csv_file,
        }
        return Response(response=json.dumps(data), status=200, mimetype='application/json')
