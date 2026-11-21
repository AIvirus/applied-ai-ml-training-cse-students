"""
llm.py - talks to the AI model (Google Gemini).

If MOCK_MODE is on, or the API call fails, it returns the "mock" answer that the caller
prepared, so the app keeps working without internet or without an API key.
"""

import logging

from app import config

logger = logging.getLogger("study_buddy.llm")
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=config.GEMINI_API_KEY)
    return _client


def current_mode():
    return "mock" if config.MOCK_MODE else "real"


def ask_llm(prompt, system=None, temperature=0.3, json_output=False, mock_answer=""):
    """
    Send a prompt to Gemini and return (answer_text, mode).
    mode is "real" when Gemini answered, "mock" when the pretend answer was used.
    """
    if not config.MOCK_MODE:
        try:
            from google.genai import types

            settings = types.GenerateContentConfig(
                system_instruction=system,
                temperature=temperature,
                response_mime_type="application/json" if json_output else None,
            )
            response = _get_client().models.generate_content(
                model=config.GEMINI_MODEL, contents=prompt, config=settings
            )
            return (response.text or "").strip(), "real"
        except Exception as error:  # network problem, bad key, rate limit, model name changed...
            # Log the type of error only. Never log the API key.
            logger.warning("Gemini call failed (%s). Using mock answer.", type(error).__name__)

    return mock_answer, "mock"
