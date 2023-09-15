from blueprints.lectionary import blp as LectionaryBlueprint
from blueprints.services import blp as ServicesBlueprint
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

app = Flask(__name__)
CORS(app)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "YorkOrthodox REST API"
app.config["API_VERSION"] = "v0.1"
app.config["OPENAPI_VERSION"] = "3.1.0"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/help"  # Show documentation here
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(LectionaryBlueprint)
api.register_blueprint(ServicesBlueprint)


if __name__ == "__main__":
    # Only use this in testing
    app.run(host="0.0.0.0", port=5000, debug=True)
