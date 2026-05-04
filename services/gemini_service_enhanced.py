"""
Enhanced Gemini API integration for all application features.
Replaces all mock data with real-time AI responses.
"""

import json
from typing import Optional, List, Dict, Any
import google.generativeai as genai
from PIL import Image

from utils.config import APIConfig
from utils.cache_manager import get_cache


class GeminiServiceError(Exception):
    """Raised when Gemini API call fails."""


def _get_model() -> genai.GenerativeModel:
    """Get configured Gemini model."""
    try:
        api_key = APIConfig.get_gemini_api_key()
        genai.configure(api_key=api_key)
        return genai.GenerativeModel("gemini-2.5-flash")
    except RuntimeError as e:
        raise GeminiServiceError(str(e)) from e


def _parse_json_response(response_text: str) -> Dict[str, Any]:
    """Safely parse JSON from model response."""
    try:
        # Extract JSON from markdown code blocks if present
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_str = response_text[start:end].strip()
        else:
            json_str = response_text
        
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise GeminiServiceError(f"Invalid JSON response: {str(e)}") from e


# ============================================================================
# LEAF ANALYSIS (Keep original - do not modify)
# ============================================================================

def analyze_leaf(image: Image.Image) -> str:
    """Analyze plant leaf for diseases. [ORIGINAL - UNCHANGED]"""
    prompt = """You are a plant disease expert.
    
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
- No explanation outside JSON"""
    
    try:
        model = _get_model()
        response = model.generate_content(
            [prompt, image],
            generation_config=genai.types.GenerationConfig(temperature=0.2),
        )
        if not response.parts:
            raise GeminiServiceError("Empty response from Gemini")
        return response.text
    except GeminiServiceError:
        raise
    except Exception as exc:
        raise GeminiServiceError(f"API call failed: {exc}") from exc


# ============================================================================
# NEWS GENERATION (NEW - Replaces RSS feeds)
# ============================================================================

def generate_agriculture_news(count: int = 10, region: str = "Global") -> List[Dict[str, str]]:
    """Generate latest agriculture news using Gemini."""
    cache_key = f"news_{region}_{count}"
    
    # Check cache first
    cached = get_cache().get(cache_key)
    if cached:
        try:
            return json.loads(cached)
        except:
            pass
    
    prompt = f"""You are an agricultural news specialist. Generate {count} latest agricultural news items for the {region} region.
    
Respond STRICTLY in this JSON format (no markdown, no explanation):
{{
  "news": [
    {{
      "title": "Short, engaging headline",
      "summary": "2-3 sentence summary of the news",
    "link": "https://example.com/news-1",
      "category": "disease|weather|technology|market|policy"
    }}
  ]
}}

Requirements:
- Make news relevant to {region}
- Include mix of categories: plant diseases, weather alerts, farming tech, market prices, policy updates
- News should be current and practical for farmers
- Each summary should be actionable
- Generate realistic but varied content"""
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        
        data = _parse_json_response(response.text)
        news_items = data.get("news", [])
        
        # Cache the result
        get_cache().set(cache_key, json.dumps(news_items))
        
        return news_items
    except Exception as e:
        raise GeminiServiceError(f"News generation failed: {str(e)}") from e


# ============================================================================
# WEATHER ANALYSIS (NEW - Replaces Open-Meteo API)
# ============================================================================

def get_weather_recommendations(location: str = "your region") -> Dict[str, Any]:
    """Get weather-based farming recommendations using Gemini."""
    cache_key = f"weather_{location}"
    
    cached = get_cache().get(cache_key)
    if cached:
        try:
            return json.loads(cached)
        except:
            pass
    
    prompt = f"""You are an agricultural meteorologist providing weather-based recommendations for {location}.

Based on typical weather patterns and current season, provide recommendations in JSON:

{{
  "forecast_summary": "General weather pattern description",
  "treatment_optimal_days": ["Day 1", "Day 2", "Day 3"],
  "disease_risks": [
    {{"disease": "disease_name", "risk_level": "HIGH/MEDIUM/LOW", "reason": "why risk exists"}}
  ],
  "recommendations": [
    "Action 1",
    "Action 2"
  ],
  "best_time_to_treat": "specific time recommendation",
  "watering_schedule": "frequency and timing"
}}

Make recommendations practical for farmers."""
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.5)
        )
        
        data = _parse_json_response(response.text)
        get_cache().set(cache_key, json.dumps(data))
        return data
    except Exception as e:
        raise GeminiServiceError(f"Weather recommendations failed: {str(e)}") from e


# ============================================================================
# DISEASE INFORMATION (NEW - Replaces hardcoded database)
# ============================================================================

def get_disease_info(disease_name: str) -> Dict[str, Any]:
    """Get comprehensive disease information from Gemini."""
    cache_key = f"disease_info_{disease_name}"
    
    cached = get_cache().get(cache_key)
    if cached:
        try:
            return json.loads(cached)
        except:
            pass
    
    prompt = f"""You are a plant pathology expert. Provide comprehensive information about '{disease_name}'.

Response STRICTLY in JSON:
{{
  "disease_name": "{disease_name}",
  "description": "What the disease is",
  "severity": "LOW/MEDIUM/HIGH/CRITICAL",
  "affected_crops": ["crop1", "crop2"],
  "symptoms": ["symptom1", "symptom2"],
  "causes": ["cause1", "cause2"],
  "prevention": ["step1", "step2"],
  "treatment": ["treatment1", "treatment2"],
  "resistant_varieties": ["variety1", "variety2"],
  "season_alert": "When it's most problematic",
  "management_practices": ["practice1", "practice2"]
}}"""
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.3)
        )
        
        data = _parse_json_response(response.text)
        get_cache().set(cache_key, json.dumps(data))
        return data
    except Exception as e:
        raise GeminiServiceError(f"Disease info retrieval failed: {str(e)}") from e


# ============================================================================
# DISEASE COMPARISON (NEW - Fully AI-driven)
# ============================================================================

def compare_diseases(disease_names: List[str]) -> Dict[str, Any]:
    """Compare multiple diseases using Gemini."""
    cache_key = f"compare_{'_'.join(disease_names)}"
    
    cached = get_cache().get(cache_key)
    if cached:
        try:
            return json.loads(cached)
        except:
            pass
    
    diseases_str = ", ".join(disease_names)
    prompt = f"""You are a plant pathology expert. Compare these diseases: {diseases_str}

Provide comparison in JSON:
{{
  "comparison": {{
    "disease_name": {{
      "key_differences": ["diff1", "diff2"],
      "treatment_similarities": ["sim1", "sim2"],
      "prevention_overlap": ["overlap1"]
    }}
  }},
  "overall_comparison": "Summary of how these diseases differ",
  "which_is_more_severe": "Analysis of severity",
  "combined_management": "How to manage if both are present"
}}"""
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.4)
        )
        
        data = _parse_json_response(response.text)
        get_cache().set(cache_key, json.dumps(data))
        return data
    except Exception as e:
        raise GeminiServiceError(f"Disease comparison failed: {str(e)}") from e


# ============================================================================
# TREATMENT SCHEDULE (ENHANCED - Fully AI-driven)
# ============================================================================

def generate_treatment_schedule(disease_name: str, duration_days: int = 7, severity: str = "moderate") -> str:
    """Generate detailed day-by-day treatment schedule."""
    cache_key = f"treatment_{disease_name}_{duration_days}_{severity}"
    
    cached = get_cache().get(cache_key)
    if cached:
        return cached
    
    prompt = f"""You are an agricultural expert. Create a {duration_days}-day detailed treatment schedule for '{disease_name}' (severity: {severity}).

Format as clean Markdown with:
- Day-by-day checklist
- Specific actions and timings
- Natural and chemical options
- Monitoring checkpoints
- Success indicators

Be practical and actionable for farmers."""
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.4)
        )
        
        schedule = response.text
        get_cache().set(cache_key, schedule)
        return schedule
    except Exception as e:
        raise GeminiServiceError(f"Treatment schedule generation failed: {str(e)}") from e


# ============================================================================
# TRANSLATION (Keep original)
# ============================================================================

def translate_json(raw_json: str, target_language: str) -> str:
    """Translate JSON values to target language."""
    prompt = (
        f"Translate JSON string values to {target_language}. "
        "Keep keys, structure, and JSON format intact. "
        f"Return STRICTLY valid JSON:\n\n{raw_json}"
    )
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.1),
        )
        return response.text if response.parts else raw_json
    except Exception:
        return raw_json


# ============================================================================
# FOLLOW-UP QUESTIONS (Keep original)
# ============================================================================

def ask_followup(disease_name: str, context: dict, question: str) -> str:
    """Answer follow-up questions about disease."""
    prompt = (
        f"Agricultural expert helping farmer with '{disease_name}'.\n"
        f"Symptoms: {', '.join(context.get('symptoms', []))}\n"
        f"Treatment: {', '.join(context.get('treatment', []))}\n"
        f"Question: {question}\n\n"
        "Provide clear, practical answer in 2-3 paragraphs."
    )
    
    try:
        model = _get_model()
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.4),
        )
        return response.text if response.parts else "I couldn't generate an answer. Please try again."
    except Exception as exc:
        return f"Error: {exc}"


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

def clear_cache(key: Optional[str] = None) -> None:
    """Clear cache for specific key or all."""
    get_cache().clear(key)


def get_cache_stats() -> Dict[str, Any]:
    """Get cache statistics."""
    return get_cache().get_stats()
