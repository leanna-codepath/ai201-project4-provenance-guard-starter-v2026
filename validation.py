"""
Input validation for /submit and /appeal.

Every check here runs BEFORE either signal is called. A request that fails
raises InvalidInput, which app.py turns into a 4xx response plus a
`rejected` entry in the audit log.

Status codes:
    400  the request itself is malformed (not JSON, wrong types, missing fields)
    413  the text is longer than the detector can actually read
    422  the request is well-formed, but the text can't be judged
"""

import re
import unicodedata
import uuid

from flask import request

import config

_ENGLISH_WORD = re.compile(r"^[A-Za-z]+(?:'[A-Za-z]+)?[.,;:!?\"')]*$")
_ALLOWED_CONTROL = {"\n", "\r", "\t"}


class InvalidInput(Exception):
    def __init__(self, status: int, error: str, message: str, creator_id=None):
        super().__init__(message)
        self.status = status
        self.error = error
        self.message = message
        self.creator_id = creator_id


def _json_object() -> dict:
    """
    The body, guaranteed to be a dict.

    Returns an InvalidInput exception if the payload body is empty, unparseable,
    form-encoded, or a non-JSON content type.
    """
    payload = request.get_json(silent=True)
    if payload is None:
        raise InvalidInput(400, "invalid_json",
                           "Send a JSON object with Content-Type: application/json.")
    
    if not isinstance(payload, dict):
        raise InvalidInput(400, "not_object",
                           "The request body must be a JSON object.")
    return payload


def _creator_id(payload: dict) -> str:
    """
    Ensures the creator_id exists

    Returns an InvalidInput exception if the creator_id is not a string or does not exist
    """

    creator_id = payload.get("creator_id")
    if not isinstance(creator_id, str) or not creator_id.strip():
        raise InvalidInput(400, "missing_creator_id",
                           "Send a non-empty 'creator_id' string.")
    
    creator_id = creator_id.strip()

    return creator_id


def _text(payload: dict, creator_id: str) -> str:
    """
    Ensures valid text input form.

    Returns an InvalidInput exception if the text is not a string, is empty, is too long, too short, has control characters
    or doesn't have enough english words to be significant.
    """

    text = payload.get("text")

    if not isinstance(text, str):
        raise InvalidInput(400, "missing_text", "Send a 'text' string.", creator_id)

    text = text.strip()

    if not text:
        raise InvalidInput(400, "empty_text", "'text' is empty.", creator_id)

    if len(text) > config.MAX_TEXT_CHARS:
        raise InvalidInput(413, "text_too_long",
                           f"Text must be at most {config.MAX_TEXT_CHARS:,} characters "
                           f"(you sent {len(text):,}). Submit it in parts.", creator_id)

    if any(unicodedata.category(c) == "Cc" and c not in _ALLOWED_CONTROL for c in text):
        raise InvalidInput(422, "control_characters",
                           "Text contains control characters. Send plain text.", creator_id)

    tokens = text.split()
    english_words = [t for t in tokens if _ENGLISH_WORD.match(t)]

    if len(english_words) < config.MIN_TEXT_WORDS:
        raise InvalidInput(422, "too_few_words",
                           f"Text needs at least {config.MIN_TEXT_WORDS} English words "
                           f"to be checked. This checker reads English prose only.",
                           creator_id)

    if len(english_words) / len(tokens) < config.MIN_ENGLISH_RATIO:
        raise InvalidInput(422, "unsupported_text",
                           "Most of this text isn't English words, so it can't be "
                           "judged reliably.", creator_id)

    return text


def validate_submission() -> tuple[str, str]:
    """
    Returns (text, creator_id) or raises InvalidInput.
    
    """

    payload = _json_object()
    creator_id = _creator_id(payload)
    text = _text(payload, creator_id)
    return text, creator_id


def validate_appeal() -> tuple[str, str]:
    """
    Returns (content_id, reasoning) or raises InvalidInput.

    """
    payload = _json_object()

    content_id = payload.get("content_id")
    if not isinstance(content_id, str) or not content_id.strip():
        raise InvalidInput(400, "missing_content_id",
                           "Send the content_id from your submission.")
    content_id = content_id.strip()

    try:
        uuid.UUID(content_id)
    except ValueError:
        raise InvalidInput(400, "invalid_content_id",
                           "That doesn't look like a content_id from this service.")

    reasoning = payload.get("reasoning")
    if not isinstance(reasoning, str) or not reasoning.strip():
        raise InvalidInput(400, "missing_reasoning",
                           "Tell us why you think the label is wrong.")
    reasoning = reasoning.strip()

    return content_id, reasoning