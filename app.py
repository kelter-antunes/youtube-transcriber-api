from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_caching import Cache
from werkzeug.exceptions import HTTPException

from src._errors import InvalidAPIUsage, TranscriptionError
from src._resources import Transcript, TranslatedTranscript, TranscriptMetadata

def create_app():
    app = Flask(__name__)
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    app.config['DEBUG'] = True  # Enable Flask debug mode
    CORS(app)

    # Configure caching
    app.config['CACHE_TYPE'] = 'simple'  # In-memory cache (for demonstration)
    cache = Cache(app)

    api_v1 = Api(app, prefix='/v1')
    api_v1.add_resource(Transcript, "/transcripts", resource_class_kwargs={'cache': cache})
    api_v1.add_resource(TranscriptMetadata, "/metadata", resource_class_kwargs={'cache': cache})
    api_v1.add_resource(TranslatedTranscript, "/translations", resource_class_kwargs={'cache': cache})

    app.register_error_handler(InvalidAPIUsage, InvalidAPIUsage)
    app.register_error_handler(TranscriptionError, TranscriptionError)

    @app.errorhandler(HTTPException)
    @app.errorhandler(InvalidAPIUsage)
    @app.errorhandler(TranscriptionError)
    def handle_exception(e):
        return jsonify(message=e.description), e.code

    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify(status='ok'), 200

    return app

if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000)
