import marshmallow as mm
from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from util import get_services

blp = Blueprint(
    "services", __name__, description="Services for the parish in York, England"
)


class ServiceSchema(mm.Schema):
    date = mm.fields.Str()
    commemoration = mm.fields.Str()
    description = mm.fields.Str()


class ServicesQueryArgsSchema(mm.Schema):
    date = mm.fields.Date(required=True)
    num_services = mm.fields.Int(required=True)



@blp.route("/services")
class Services(MethodView):
    """An end-point to provide upcoming services and events."""

    @blp.arguments(ServicesQueryArgsSchema, location="query")
    @blp.response(200, ServiceSchema(many=True))
    def get(self, params):
        return jsonify(get_services(**params))
