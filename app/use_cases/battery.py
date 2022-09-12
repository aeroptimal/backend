from flask import Response
import json

from repos.Batteries import Battery

class BatteryResult:
    def __init__(self, params):
        self.params = params

    def execute(self):
        calc = int(self.params['calc'])
        typeb = int(self.params['type'])
        var1 = float(self.params['var1'])
        var2 = float(self.params['var2'])
        h = float(self.params['h'])
        k = float(self.params['k']) if typeb == 6 else ''
        if not (0 <= var1):
            return Response(response=json.dumps({"error":"Invalid input"}), status=400, mimetype='application/json')
        if not (0 <= var2):
            return Response(response=json.dumps({"error":"Invalid input"}), status=400, mimetype='application/json')
        if typeb == 6 and not (0 <= k):
            return Response(response=json.dumps({"error":"Invalid K value"}), status=400, mimetype='application/json') 
        if not (0 <= h):
            return Response(response=json.dumps({"error":"Invalid H value"}), status=400, mimetype='application/json') 
        repo = Battery(calc,typeb,h,var1,var2,k)
        val = repo.ComputeVal()
        IP,CP,TP = repo.GenPlotCord()
        data = {
            "value": val,
            "IP": IP,
            "CP": CP,
            "TP": TP,
        }
        print(data)
        return Response(response=json.dumps(data), status=200, mimetype='application/json')

