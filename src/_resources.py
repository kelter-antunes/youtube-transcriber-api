from flask import request, current_app as app
from flask_restful import Resource

from src._errors import InvalidAPIUsage, TranscriptionError
from src._settings import LANGUAGE_CODES, TRANSCRIPT_OUTPUT_TYPES
from src._parser import parse_transcript
from src._transcript import retrieve_transcript, build_transcript

class Transcript(Resource):
    def __init__(self, cache=None):
        self.cache = cache

    def get(self):
        video_id, language_codes, output_type, include_line_break, include_sfx = self._parse_request_args()

        # Always cache the response
        cache_key = (request.path, request.query_string)
        cached_data = self.cache.get(cache_key)
        if cached_data:
            if app.config['DEBUG']:
                print("HIT: Cache hit for key", cache_key)
            return cached_data

        if not video_id:
            raise InvalidAPIUsage(error_messages["noVideoId"])

        output_type = output_type.lower()
        if output_type not in TRANSCRIPT_OUTPUT_TYPES:
            raise InvalidAPIUsage(error_messages["invalidOutput"])

        transcript_list = retrieve_transcript(video_id)

        if not language_codes:
            response_data = {
                "videoId": video_id,
                "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx) for transcript in transcript_list]
            }
        else:
            try:
                transcript = transcript_list.find_transcript([language_codes])
                response_data = {
                    "videoId": video_id,
                    "transcripts": [build_transcript(transcript, output_type, include_line_break, include_sfx)]
                }
            except NoTranscriptFound:
                raise TranscriptionError(error_messages["noTranscriptFoundForLanguage"])

        # Cache the response
        self.cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour

        if app.config['DEBUG']:
            if not cached_data:
                print("MISS: Cache miss for key", cache_key)

        return response_data, 200

    def _parse_request_args(self):
        video_id = request.args.get('id')
        language_codes = request.args.get('lang')
        output_type = request.args.get('type', 'text')
        include_line_break = bool(request.args.get('lb', 0))
        include_sfx = bool(request.args.get('sfx', 0))
        return video_id, language_codes, output_type, include_line_break, include_sfx


class TranslatedTranscript(Resource):
    def __init__(self, cache=None):
        self.cache = cache

    def get(self):
        video_id, language_code = self._parse_request_args()

        # Always cache the response
        cache_key = (request.path, request.query_string)
        cached_data = self.cache.get(cache_key)
        if cached_data:
            if app.config['DEBUG']:
                print("HIT: Cache hit for key", cache_key)
            return cached_data

        if not video_id:
            raise InvalidAPIUsage(error_messages["noVideoId"])
        if not language_code:
            raise InvalidAPIUsage(error_messages["noTargetLanguage"])

        transcript_list = retrieve_transcript(video_id)
        transcript = transcript_list.find_transcript(LANGUAGE_CODES)

        try:
            translated_transcript = transcript.translate(language_code)
        except YOUTUBE_API_ERRORS as e:
            raise TranscriptionError(e.cause)

        response_data = {
            "videoId": video_id,
            "sourceLanguage": transcript.language_code,
            "targetLanguage": language_code,
            "transcripts": parse_transcript(translated_transcript.fetch())
        }

        # Cache the response
        self.cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour

        if app.config['DEBUG']:
            if not cached_data:
                print("MISS: Cache miss for key", cache_key)

        return response_data, 200

    def _parse_request_args(self):
        video_id = request.args.get('id')
        language_code = request.args.get('lang')
        return video_id, language_code


class TranscriptMetadata(Resource):
    def __init__(self, cache=None):
        self.cache = cache

    def get(self):
        video_id = request.args.get('id')

        # Always cache the response
        cache_key = (request.path, request.query_string)
        cached_data = self.cache.get(cache_key)
        if cached_data:
            if app.config['DEBUG']:
                print("HIT: Cache hit for key", cache_key)
            return cached_data

        if not video_id:
            raise InvalidAPIUsage(error_messages["noVideoId"])

        transcript_list = retrieve_transcript(video_id)

        response_data = {
            "videoId": video_id,
            "transcripts": [
                {
                    "language": transcript.language,
                    "languageCode": transcript.language_code,
                    "isGenerated": transcript.is_generated,
                    "isTranslatable": transcript.is_translatable
                } for transcript in transcript_list
            ]
        }

        # Cache the response
        self.cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour

        if app.config['DEBUG']:
            if not cached_data:
                print("MISS: Cache miss for key", cache_key)

        return response_data, 200
