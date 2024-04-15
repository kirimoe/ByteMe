import os
import envparse
from flask import Flask, jsonify, request

from pipeline import get_votes

def create_app():

    result = 0
    
    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def post():
        if request.headers['Content-Type'] != 'application/octet-stream':
            resp = jsonify({'error': 'expecting application/octet-stream'})
            resp.status_code = 400  # Bad Request
            return resp

        bytez = request.data

        with open('bin.exe', 'wb') as f:
            f.write(bytez)

        # Do something with the binary data if needed
        try:
            votes = get_votes('bin.exe')
            if sum(votes) >= 4:
                result = 1
        except Exception as e:
            print(f"Error while analyzing file: {e}")
            result = None
            resp = jsonify({'error': 'error with the file format or processing the file.'})
            resp.status_code = 500
            return resp

        resp = jsonify({'result': result})
        resp.status_code = 200
        return resp

    return app

if __name__ == "__main__":
    app = create_app()

    port = int(os.environ.get("PORT", 8080))

    from gevent.pywsgi import WSGIServer
    from gevent.pool import Pool

    http_server = WSGIServer(('', port), app, spawn=Pool())
    print(f"Server running on port {port}")
    http_server.serve_forever()
