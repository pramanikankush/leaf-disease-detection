"""
Centralized configuration and API key management.
"""

import os
from typing import Optional

try:
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # Fallback to environment variables only if dotenv is unavailable.
    pass


class APIConfig:
    """Manage API keys and configuration across the application."""
    
    @staticmethod
    def get_gemini_api_key() -> str:
        """
        Retrieve Gemini API key from environment.
        
        Returns
        -------
        str
            The Gemini API key
            
        Raises
        ------
        RuntimeError
            If no API key is configured
        """
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        
        if not api_key:
            raise RuntimeError(
                "❌ GEMINI_API_KEY not configured. "
                "Set the environment variable before running the app."
            )
        
        return api_key
    
    @staticmethod
    def validate_gemini_api_key() -> tuple[bool, str]:
        """
        Validate Gemini API key exists and is valid format.
        
        Returns
        -------
        tuple[bool, str]
            (is_valid, message)
        """
        try:
            api_key = APIConfig.get_gemini_api_key()
            
            # Basic validation - check if key exists and has minimum length
            if not api_key or len(api_key) < 10:
                return False, "❌ API key too short or empty"
            
            # Check if it looks like a valid key format
            if api_key.startswith("AQ.") or api_key.startswith("sk-"):
                return True, "✅ API key validated"
            
            return True, "⚠️ API key format unusual but accepted"
        
        except RuntimeError as e:
            return False, str(e)
        except Exception as e:
            return False, f"❌ API validation error: {str(e)}"
    
    @staticmethod
    def get_all_config() -> dict:
        """Get all configuration details."""
        is_valid, msg = APIConfig.validate_gemini_api_key()
        
        api_key = os.environ.get("GEMINI_API_KEY", "").strip()
        masked_key = (api_key[:10] + "***") if api_key else "(not set)"

        return {
            "gemini_api_key": masked_key,
            "gemini_valid": is_valid,
            "gemini_message": msg,
            "environment": "production" if api_key else "development"
        }


def check_api_configuration():
    """Check if all required APIs are configured. Use in Streamlit startup."""
    import streamlit as st
    
    is_valid, msg = APIConfig.validate_gemini_api_key()
    
    if not is_valid:
        st.error(f"🔴 {msg}")
        st.info("""
        **Setup Required:**
        
        1. **Set Environment Variable** (Recommended):
           ```bash
           set GEMINI_API_KEY=your_api_key_here
           ```
        
          2. **Get API Key**:
           - Visit: https://aistudio.google.com/app/apikey
           - Create new API key
           - Copy and paste above
        """)
        return False
    
    return True
