from flask import Flask, request
from flask_restplus import Api, Resource, fields, marshal

from astral import Location
import redis
from datetime import datetime,timezone

app = Flask(__name__)
api = Api(app)

r = redis.StrictRedis(charset="utf-8", decode_responses=True)

loc = Location(('Warsaw', 'Poland', 52.22977, 21.01178,'Europe/Warsaw',110))

#models
model_operation = api.model('Operation',{
    'operation': fields.String,
})
model_color = api.model('Color', {
    'color': fields.String,
})

@api.route('/operations')
class Operations(Resource):
    def get(self):
        operations = r.lrange('operations',0,-1)
        return operations,200

    @api.doc(body=model_operation)
    @api.response(201, 'Saved')
    @api.response(400, 'Operation field not found in request body')
    def post(self):
        data = request.get_json()
        if 'operation' in data:
            r.lpush('operations',data['operation'])
            return {},201
        
        return {},400
    
    @api.response(200, 'Deleted')
    def delete(self):
        r.delete('operations')
        return {},200

@api.route('/color')
class Color(Resource):
    @api.marshal_with(model_color)
    def get(self):
        azimuth = loc.solar_azimuth(datetime.now(tz=loc.tz))
        lightness = 100-abs(180-azimuth)/18*10
        hsl = "hsl({},{}%,{}%)".format(240,100,round(lightness,2))
        return {'color':hsl}
if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run(host='0.0.0.0')