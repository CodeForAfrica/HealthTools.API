from flask import Flask, jsonify
from healthtools_ke_api.nurses import nurses_api, index as nurses_index


app = Flask(__name__)
app.register_blueprint(nurses_api, url_prefix='/nurses')


@app.route("/")
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "HealthTools.KE-API",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/nurses": {"methods": ["GET"]}
        }
    }
    return jsonify(msg)

if __name__ == "__main__":
    app.run(debug=True)
