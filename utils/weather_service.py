"""
Weather integration for optimal treatment timing suggestions.
Uses Open-Meteo free API (no API key required).
"""

import requests
from datetime import datetime, timedelta


def get_weather_forecast(lat: float, lon: float, days: int = 7) -> dict:
    """
    Fetch weather forecast for given coordinates.
    
    Parameters
    ----------
    lat : float
        Latitude
    lon : float
        Longitude
    days : int
        Number of days to forecast (1-10)
    
    Returns
    -------
    dict
        Weather forecast data with recommendations
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,windspeed_10m_max",
            "temperature_unit": "fahrenheit",
            "windspeed_unit": "mph",
            "precipitation_unit": "inch",
            "timezone": "auto",
            "forecast_days": min(days, 10)
        }
        
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}


def analyze_treatment_conditions(weather_data: dict) -> list:
    """
    Analyze weather forecast and suggest best treatment days.
    
    Parameters
    ----------
    weather_data : dict
        Weather forecast from Open-Meteo API
    
    Returns
    -------
    list
        Recommendations for treatment timing
    """
    recommendations = []
    
    try:
        daily = weather_data.get("daily", {})
        temps_max = daily.get("temperature_2m_max", [])
        temps_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        wind = daily.get("windspeed_10m_max", [])
        times = daily.get("time", [])
        
        for i, day in enumerate(times):
            temp_max = temps_max[i] if i < len(temps_max) else 0
            temp_min = temps_min[i] if i < len(temps_min) else 0
            rain = precip[i] if i < len(precip) else 0
            wind_speed = wind[i] if i < len(wind) else 0
            
            day_date = datetime.fromisoformat(day).strftime("%A, %b %d")
            
            # Determine if day is suitable for treatment
            score = 0
            reasons = []
            
            # Low wind is better for spray application
            if wind_speed < 10:
                score += 2
                reasons.append("✓ Low wind (good for spraying)")
            elif wind_speed < 15:
                score += 1
                reasons.append("⚠️ Moderate wind (acceptable)")
            else:
                reasons.append("✗ High wind (avoid spraying)")
            
            # No rain is crucial - treatment washes off
            if rain < 0.1:
                score += 2
                reasons.append("✓ No rain expected")
            else:
                reasons.append(f"✗ {rain}\" rain expected")
            
            # Moderate temperature (60-80°F is ideal)
            if 60 <= temp_max <= 80:
                score += 2
                reasons.append(f"✓ Ideal temps: {int(temp_min)}°F - {int(temp_max)}°F")
            elif 50 <= temp_max <= 90:
                score += 1
                reasons.append(f"⚠️ Acceptable temps: {int(temp_min)}°F - {int(temp_max)}°F")
            else:
                reasons.append(f"✗ Temperature {int(temp_max)}°F (too extreme)")
            
            # Apply early morning (cooler, lower wind)
            # Avoid late afternoon (heat stress)
            if i == 0:
                reasons.append("📅 Treat early morning for best results")
            
            recommendation = {
                "date": day_date,
                "score": score,
                "suitable": score >= 4,
                "temp_max": int(temp_max),
                "temp_min": int(temp_min),
                "rain": rain,
                "wind": wind_speed,
                "reasons": reasons
            }
            recommendations.append(recommendation)
        
        return sorted(recommendations, key=lambda x: x["score"], reverse=True)
    
    except Exception as e:
        return [{"error": f"Could not analyze weather: {str(e)}"}]


def get_disease_weather_risk(weather_data: dict) -> dict:
    """
    Assess disease risk based on current/forecast weather.
    Different diseases thrive in different conditions.
    """
    try:
        daily = weather_data.get("daily", {})
        temps_max = daily.get("temperature_2m_max", [])
        precip = daily.get("precipitation_sum", [])
        
        if not temps_max or not precip:
            return {"error": "Insufficient weather data"}
        
        # Use today's values for risk assessment
        today_temp = temps_max[0] if temps_max else 70
        today_rain = precip[0] if precip else 0
        
        risks = {}
        
        # Powdery mildew: warm (70-80°F), low humidity, calm
        if 65 < today_temp < 85 and today_rain < 0.3:
            risks["Powdery Mildew"] = "HIGH - Warm & dry = ideal conditions"
        
        # Early Blight/Late Blight: cool, wet (60-70°F with rain)
        if 55 < today_temp < 75 and today_rain > 0.3:
            risks["Early Blight"] = "HIGH - Cool & wet = ideal conditions"
            risks["Blight"] = "HIGH - Cool & wet = ideal conditions"
        
        # Septoria/Leaf Spot: moderate temps with humidity
        if 65 < today_temp < 80 and today_rain > 0.2:
            risks["Septoria Leaf Blotch"] = "MODERATE - Humid conditions present"
            risks["Leaf Spot"] = "MODERATE - Humid conditions present"
        
        # Rust: humidity & moderate temps
        if 60 < today_temp < 75 and today_rain > 0.2:
            risks["Rust"] = "MODERATE - Conditions favor rust"
        
        return risks if risks else {"status": "Low disease risk today"}
    
    except Exception as e:
        return {"error": str(e)}
