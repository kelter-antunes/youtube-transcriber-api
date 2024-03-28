import re
import json

from typing import Optional
from youtube_transcript_api.formatters import *

from ._settings import TRANSCRIPT_OUTPUT_TYPES


def parse_transcript(
    transcript: dict,
    output_type: str = "text",
    include_line_break: Optional[bool] = False,
    include_sfx: Optional[bool] = False
):
    """
    parse_transcript parses a transcript and return it in the specified format

    :param `transcript`: a dictionary object returned by transcript.fetch()
    :param `formatter`: transcript can be formatted as `text`, `json`, `srt`, or `webvtt`.
    :param `include_line_break`: boolean to indicate if transcript should contain line breaks. This only applies if formatter=`text`.
    :param `include_sfx`: boolean to indicate if transcript should contain sound effects information eg. [Music], [Cheering].
    :return: returns a parsed transcript in the specified format (JSON for `JSON` and string for the rest)
    """

    formatter = TRANSCRIPT_OUTPUT_TYPES.get(output_type)
    if formatter is None:
        raise ValueError("Invalid output_type specified")

    parsed_transcript = formatter.format_transcript(transcript)

    if not include_sfx:
        # Remove sound effects information
        parsed_transcript = re.sub(r"\[[^\]]*\]", "", parsed_transcript)

    if not include_line_break and output_type == "text":
        # Remove line breaks if include_line_break is False
        parsed_transcript = parsed_transcript.replace("\n", " ")

    if output_type == "json":
        # Convert to JSON if output_type is JSON
        parsed_transcript = json.loads(parsed_transcript)

    return parsed_transcript
