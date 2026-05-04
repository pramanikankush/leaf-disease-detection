"""
Cache management service for Gemini API responses.
Reduces API calls and improves performance.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from pathlib import Path


class CacheManager:
    """Manage caching of Gemini API responses."""
    
    CACHE_DIR = Path("data/.cache")
    CACHE_EXPIRY_HOURS = 24
    
    def __init__(self):
        """Initialize cache directory."""
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_file(self, key: str) -> Path:
        """Get cache file path for a key."""
        sanitized_key = key.replace(" ", "_").replace("/", "_")
        return self.CACHE_DIR / f"{sanitized_key}.json"
    
    def get(self, key: str) -> Optional[str]:
        """Retrieve cached value if valid."""
        cache_file = self._get_cache_file(key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check expiry
            created = datetime.fromisoformat(data['created_at'])
            if datetime.now() - created > timedelta(hours=self.CACHE_EXPIRY_HOURS):
                cache_file.unlink()
                return None
            
            return data['value']
        except Exception:
            return None
    
    def set(self, key: str, value: str) -> None:
        """Cache a value."""
        cache_file = self._get_cache_file(key)
        
        try:
            data = {
                'created_at': datetime.now().isoformat(),
                'value': value
            }
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
        except Exception:
            pass  # Silently fail on cache write
    
    def clear(self, key: Optional[str] = None) -> None:
        """Clear specific cache or all cache."""
        if key:
            cache_file = self._get_cache_file(key)
            if cache_file.exists():
                cache_file.unlink()
        else:
            for cache_file in self.CACHE_DIR.glob("*.json"):
                cache_file.unlink()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_files = list(self.CACHE_DIR.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)
        
        return {
            "cached_items": len(cache_files),
            "total_size_mb": total_size / (1024 * 1024),
            "expiry_hours": self.CACHE_EXPIRY_HOURS
        }


# Global cache instance
_cache = CacheManager()


def get_cache() -> CacheManager:
    """Get global cache instance."""
    return _cache
