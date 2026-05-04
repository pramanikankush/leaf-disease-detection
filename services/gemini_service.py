"""
Gemini Vision API service for plant leaf disease analysis.

Sends leaf images to Google Gemini with a structured prompt
and returns the raw text response for downstream parsing.
"""

import os

import google.generativeai as genai
from PIL import Image
from utils.config import APIConfig


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------
_ANALYSIS_PROMPT = """You are a plant disease expert.

Analyze the given plant leaf image and respond STRICTLY in JSON format:

{
  "disease_name": "...",
  "confidence": "...%",
  "is_healthy": true/false,
  "symptoms": ["...", "..."],
  "treatment": ["...", "..."],
  "prevention": ["...", "..."]
}

Rules:
- Confidence must be realistic (0-100%)
- If healthy, set disease_name to "Healthy" and is_healthy to true
- Keep treatment practical and concise
- No explanation outside JSON
"""


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------
class GeminiServiceError(Exception):
    """Raised when the Gemini API call fails."""


def _get_model() -> genai.GenerativeModel:
    """Configure and return the Gemini generative model using centralized API key."""
    try:
        api_key = APIConfig.get_gemini_api_key()
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.5-flash")
    except RuntimeError as e:
        raise GeminiServiceError(str(e)) from e


def analyze_leaf(image: Image.Image) -> str:
    """Send a leaf image to Gemini Vision and return the raw response text.

    Parameters
    ----------
    image : PIL.Image.Image
        The leaf photograph to analyse.

    Returns
    -------
    str
        Raw text returned by the model (expected to be JSON).

    Raises
    ------
    GeminiServiceError
        If the API key is missing or the API call fails.
    """
    try:
        model = _get_model()
        response = model.generate_content(
            [_ANALYSIS_PROMPT, image],
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,  # low temperature for consistent output
            ),
        )
        # Gemini may block responses for safety – check first
        if not response.parts:
            raise GeminiServiceError(
                "Gemini returned an empty response. "
                "The image may have been blocked by safety filters."
            )
        return response.text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"Gemini API call failed: {exc}") from exc


def translate_json(raw_json: str, target_language: str) -> str:
    """Translate the values of the JSON response to a target language.
    
    Parameters
    ----------
    raw_json : str
        The JSON string to translate.
    target_language : str
        The language to translate to (e.g., 'Hindi', 'Spanish').
        
    Returns
    -------
    str
        The translated JSON string.
    """
    prompt = (
        f"You are a translator. Translate the string values in the following JSON into {target_language}. "
        "DO NOT change the JSON keys. DO NOT change boolean or numeric values. "
        "Return STRICTLY valid JSON only, with no markdown code blocks or explanations.\n\n"
        f"{raw_json}"
    )
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.1),
        )
        if not response.parts:
            return raw_json
        return response.text
    except Exception:
        return raw_json


def ask_followup(disease_name: str, context: dict, question: str) -> str:
    """Ask a follow-up question about the diagnosed disease.
    
    Parameters
    ----------
    disease_name : str
        The name of the detected disease.
    context : dict
        The parsed dictionary of the analysis to provide context.
    question : str
        The farmer's question.
        
    Returns
    -------
    str
        The AI's response.
    """
    prompt = (
        f"You are an agricultural expert helping a farmer. "
        f"They recently scanned a leaf and it was diagnosed with '{disease_name}'.\n"
        f"Here are the symptoms, treatment, and prevention details previously given:\n"
        f"Symptoms: {', '.join(context.get('symptoms', []))}\n"
        f"Treatment: {', '.join(context.get('treatment', []))}\n"
        f"Prevention: {', '.join(context.get('prevention', []))}\n\n"
        f"The farmer has a follow-up question:\n'{question}'\n\n"
        "Provide a clear, practical, and helpful answer in 2-3 short paragraphs. "
        "Speak directly to the farmer. Keep it simple and actionable."
    )
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.4),
        )
        if not response.parts:
            return "I'm sorry, I couldn't generate an answer right now. Please try again."
        return response.text
    except Exception as exc:
        return f"Error connecting to AI assistant: {exc}"


def generate_treatment_schedule(disease_name: str, duration_days: int = 7) -> str:
    """Generate a day-by-day treatment schedule for a given disease.
    
    Parameters
    ----------
    disease_name : str
        The name of the disease to treat.
    duration_days : int
        Number of days for the schedule (default 7).
        
    Returns
    -------
    str
        Markdown string containing the schedule.
    """
    prompt = (
        f"You are an agricultural expert. Create a {duration_days}-day treatment schedule "
        f"for a plant suffering from '{disease_name}'.\n"
        "Format the output strictly in clean Markdown as a day-by-day checklist or timeline. "
        "Keep the advice practical, specific, and actionable for a farmer. "
        "Include natural or chemical treatments as appropriate."
    )
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.3),
        )
        if not response.parts:
            return "Could not generate a treatment schedule."
        return response.text
    except Exception as exc:
        return f"Error connecting to AI assistant: {exc}"
