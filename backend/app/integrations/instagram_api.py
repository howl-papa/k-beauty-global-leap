"""
Instagram Graph API Client

Handles all interactions with Instagram Graph API including:
- OAuth 2.0 authentication
- User profile and media fetching
- Hashtag search and insights
- Rate limiting and error handling
"""

import asyncio
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import httpx
from pydantic import BaseModel

from app.core.config import get_settings


# ========== Pydantic Models for API Responses ==========

class InstagramUser(BaseModel):
    """Instagram user profile data"""
    id: str
    username: str
    account_type: str
    media_count: int


class InstagramMedia(BaseModel):
    """Instagram media (post) data"""
    id: str
    caption: Optional[str] = None
    media_type: str  # IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url: str
    permalink: str
    timestamp: datetime
    like_count: Optional[int] = None
    comments_count: Optional[int] = None
    
    # Additional fields for insights
    impressions: Optional[int] = None
    reach: Optional[int] = None
    saved: Optional[int] = None
    engagement: Optional[int] = None


class InstagramHashtag(BaseModel):
    """Instagram hashtag data"""
    id: str
    name: str


class InstagramInsights(BaseModel):
    """Instagram insights data"""
    impressions: int
    reach: int
    engagement: int
    saved: int
    profile_views: int


# ========== Rate Limiter ==========

class RateLimiter:
    """
    Rate limiter for Instagram API calls
    
    Instagram limits: 200 calls per hour per user
    """
    
    def __init__(self, max_calls: int = 200, period: int = 3600):
        """
        Args:
            max_calls: Maximum number of calls allowed
            period: Time period in seconds (default: 3600 = 1 hour)
        """
        self.max_calls = max_calls
        self.period = period
        self.calls: List[float] = []
    
    def is_allowed(self) -> bool:
        """Check if a new API call is allowed"""
        now = time.time()
        
        # Remove calls outside the time window
        self.calls = [call_time for call_time in self.calls if call_time > now - self.period]
        
        # Check if we're under the limit
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        
        return False
    
    def time_until_next_call(self) -> float:
        """Get seconds until next call is allowed"""
        if len(self.calls) < self.max_calls:
            return 0.0
        
        now = time.time()
        oldest_call = min(self.calls)
        return max(0, self.period - (now - oldest_call))
    
    def get_remaining_calls(self) -> int:
        """Get number of remaining calls in current window"""
        now = time.time()
        self.calls = [call_time for call_time in self.calls if call_time > now - self.period]
        return max(0, self.max_calls - len(self.calls))


# ========== Custom Exceptions ==========

class InstagramAPIError(Exception):
    """Base exception for Instagram API errors"""
    def __init__(self, code: int, message: str, error_type: str = "APIError"):
        self.code = code
        self.message = message
        self.error_type = error_type
        super().__init__(f"Instagram API Error {code}: {message}")


class RateLimitError(InstagramAPIError):
    """Rate limit exceeded error"""
    def __init__(self):
        super().__init__(4, "Rate limit exceeded", "RateLimitError")


class TokenExpiredError(InstagramAPIError):
    """Access token expired error"""
    def __init__(self):
        super().__init__(190, "Access token expired", "OAuthException")


class PermissionError(InstagramAPIError):
    """Permission denied error"""
    def __init__(self, message: str = "Permission denied"):
        super().__init__(200, message, "PermissionError")


# ========== Instagram Graph API Client ==========

class InstagramGraphAPI:
    """
    Instagram Graph API Client
    
    Handles authentication, API requests, rate limiting, and error handling
    for Instagram Graph API v18.0
    """
    
    BASE_URL = "https://graph.instagram.com"
    API_VERSION = "v18.0"
    
    def __init__(self, access_token: Optional[str] = None):
        """
        Initialize Instagram API client
        
        Args:
            access_token: Instagram access token (if None, uses config)
        """
        self.settings = get_settings()
        self.access_token = access_token or getattr(self.settings, "INSTAGRAM_ACCESS_TOKEN", None)
        self.rate_limiter = RateLimiter(max_calls=200, period=3600)
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
    
    def _build_url(self, endpoint: str) -> str:
        """Build full API URL"""
        # Remove leading slash if present
        endpoint = endpoint.lstrip("/")
        return f"{self.BASE_URL}/{endpoint}"
    
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None
    ) -> Dict:
        """
        Make HTTP request to Instagram API with rate limiting and error handling
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint
            params: Query parameters
            data: Request body data
            
        Returns:
            API response as dictionary
            
        Raises:
            RateLimitError: If rate limit exceeded
            TokenExpiredError: If access token expired
            InstagramAPIError: For other API errors
        """
        # Check rate limit
        if not self.rate_limiter.is_allowed():
            wait_time = self.rate_limiter.time_until_next_call()
            raise RateLimitError()
        
        # Add access token to params
        if params is None:
            params = {}
        if self.access_token:
            params["access_token"] = self.access_token
        
        # Build URL
        url = self._build_url(endpoint)
        
        # Make request
        try:
            if method.upper() == "GET":
                response = await self.client.get(url, params=params)
            elif method.upper() == "POST":
                response = await self.client.post(url, params=params, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            # Parse response
            response.raise_for_status()
            result = response.json()
            
            # Check for API errors in response
            if "error" in result:
                error = result["error"]
                code = error.get("code", 0)
                message = error.get("message", "Unknown error")
                error_type = error.get("type", "APIError")
                
                # Handle specific errors
                if code == 190:
                    raise TokenExpiredError()
                elif code == 4:
                    raise RateLimitError()
                elif code == 200:
                    raise PermissionError(message)
                else:
                    raise InstagramAPIError(code, message, error_type)
            
            return result
            
        except httpx.HTTPStatusError as e:
            # Handle HTTP errors
            try:
                error_data = e.response.json()
                error = error_data.get("error", {})
                code = error.get("code", e.response.status_code)
                message = error.get("message", str(e))
                raise InstagramAPIError(code, message)
            except:
                raise InstagramAPIError(e.response.status_code, str(e))
        
        except httpx.RequestError as e:
            raise InstagramAPIError(0, f"Request failed: {str(e)}")
    
    # ========== Authentication ==========
    
    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict:
        """
        Exchange authorization code for short-lived access token
        
        Args:
            code: Authorization code from OAuth flow
            redirect_uri: Redirect URI used in authorization
            
        Returns:
            Dictionary with access_token and user_id
        """
        data = {
            "client_id": self.settings.INSTAGRAM_APP_ID,
            "client_secret": self.settings.INSTAGRAM_APP_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code
        }
        
        response = await self.client.post(
            "https://api.instagram.com/oauth/access_token",
            data=data
        )
        response.raise_for_status()
        return response.json()
    
    async def exchange_short_for_long_token(self, short_token: str) -> Dict:
        """
        Exchange short-lived token (1 hour) for long-lived token (60 days)
        
        Args:
            short_token: Short-lived access token
            
        Returns:
            Dictionary with access_token, token_type, expires_in
        """
        params = {
            "grant_type": "ig_exchange_token",
            "client_secret": self.settings.INSTAGRAM_APP_SECRET,
            "access_token": short_token
        }
        
        result = await self._make_request("GET", "access_token", params=params)
        return result
    
    async def refresh_long_lived_token(self, long_token: str) -> Dict:
        """
        Refresh long-lived token (extends expiration by 60 days)
        
        Args:
            long_token: Current long-lived access token
            
        Returns:
            Dictionary with new access_token and expires_in
        """
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": long_token
        }
        
        result = await self._make_request("GET", "refresh_access_token", params=params)
        return result
    
    # ========== User Operations ==========
    
    async def get_user_profile(
        self,
        user_id: str,
        fields: Optional[List[str]] = None
    ) -> InstagramUser:
        """
        Get user profile information
        
        Args:
            user_id: Instagram user ID
            fields: List of fields to retrieve (default: id, username, account_type, media_count)
            
        Returns:
            InstagramUser object
        """
        if fields is None:
            fields = ["id", "username", "account_type", "media_count"]
        
        params = {"fields": ",".join(fields)}
        result = await self._make_request("GET", f"{user_id}", params=params)
        
        return InstagramUser(**result)
    
    async def get_user_media(
        self,
        user_id: str,
        limit: int = 25,
        fields: Optional[List[str]] = None
    ) -> List[InstagramMedia]:
        """
        Get user's media (posts)
        
        Args:
            user_id: Instagram user ID
            limit: Maximum number of media items to retrieve
            fields: List of fields to retrieve
            
        Returns:
            List of InstagramMedia objects
        """
        if fields is None:
            fields = [
                "id", "caption", "media_type", "media_url", "permalink",
                "timestamp", "like_count", "comments_count"
            ]
        
        params = {
            "fields": ",".join(fields),
            "limit": limit
        }
        
        result = await self._make_request("GET", f"{user_id}/media", params=params)
        
        media_list = []
        for item in result.get("data", []):
            # Parse timestamp
            if "timestamp" in item:
                item["timestamp"] = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            media_list.append(InstagramMedia(**item))
        
        return media_list
    
    # ========== Media Operations ==========
    
    async def get_media_details(
        self,
        media_id: str,
        fields: Optional[List[str]] = None
    ) -> InstagramMedia:
        """
        Get detailed information about a specific media item
        
        Args:
            media_id: Instagram media ID
            fields: List of fields to retrieve
            
        Returns:
            InstagramMedia object
        """
        if fields is None:
            fields = [
                "id", "caption", "media_type", "media_url", "permalink",
                "timestamp", "like_count", "comments_count"
            ]
        
        params = {"fields": ",".join(fields)}
        result = await self._make_request("GET", f"{media_id}", params=params)
        
        # Parse timestamp
        if "timestamp" in result:
            result["timestamp"] = datetime.fromisoformat(result["timestamp"].replace("Z", "+00:00"))
        
        return InstagramMedia(**result)
    
    async def get_media_insights(
        self,
        media_id: str,
        metrics: Optional[List[str]] = None
    ) -> Dict:
        """
        Get insights for a media item (Business accounts only)
        
        Args:
            media_id: Instagram media ID
            metrics: List of metrics to retrieve (engagement, impressions, reach, saved)
            
        Returns:
            Dictionary with insights data
        """
        if metrics is None:
            metrics = ["engagement", "impressions", "reach", "saved"]
        
        params = {"metric": ",".join(metrics)}
        result = await self._make_request("GET", f"{media_id}/insights", params=params)
        
        # Parse insights data
        insights = {}
        for item in result.get("data", []):
            metric_name = item.get("name")
            metric_value = item.get("values", [{}])[0].get("value", 0)
            insights[metric_name] = metric_value
        
        return insights
    
    # ========== Hashtag Operations ==========
    
    async def search_hashtag(self, user_id: str, hashtag: str) -> Optional[InstagramHashtag]:
        """
        Search for a hashtag
        
        Args:
            user_id: Instagram user ID (required for hashtag search)
            hashtag: Hashtag name (without #)
            
        Returns:
            InstagramHashtag object or None if not found
        """
        params = {
            "user_id": user_id,
            "q": hashtag
        }
        
        result = await self._make_request("GET", "ig_hashtag_search", params=params)
        
        data = result.get("data", [])
        if data:
            return InstagramHashtag(**data[0])
        return None
    
    async def get_hashtag_top_media(
        self,
        hashtag_id: str,
        user_id: str,
        limit: int = 25,
        fields: Optional[List[str]] = None
    ) -> List[InstagramMedia]:
        """
        Get top media for a hashtag
        
        Args:
            hashtag_id: Instagram hashtag ID
            user_id: Instagram user ID (required)
            limit: Maximum number of media items
            fields: List of fields to retrieve
            
        Returns:
            List of InstagramMedia objects
        """
        if fields is None:
            fields = ["id", "caption", "media_url", "like_count", "comments_count", "timestamp"]
        
        params = {
            "user_id": user_id,
            "fields": ",".join(fields),
            "limit": limit
        }
        
        result = await self._make_request("GET", f"{hashtag_id}/top_media", params=params)
        
        media_list = []
        for item in result.get("data", []):
            if "timestamp" in item:
                item["timestamp"] = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            media_list.append(InstagramMedia(**item))
        
        return media_list
    
    async def get_hashtag_recent_media(
        self,
        hashtag_id: str,
        user_id: str,
        limit: int = 25,
        fields: Optional[List[str]] = None
    ) -> List[InstagramMedia]:
        """
        Get recent media for a hashtag
        
        Args:
            hashtag_id: Instagram hashtag ID
            user_id: Instagram user ID (required)
            limit: Maximum number of media items
            fields: List of fields to retrieve
            
        Returns:
            List of InstagramMedia objects
        """
        if fields is None:
            fields = ["id", "caption", "media_url", "like_count", "comments_count", "timestamp"]
        
        params = {
            "user_id": user_id,
            "fields": ",".join(fields),
            "limit": limit
        }
        
        result = await self._make_request("GET", f"{hashtag_id}/recent_media", params=params)
        
        media_list = []
        for item in result.get("data", []):
            if "timestamp" in item:
                item["timestamp"] = datetime.fromisoformat(item["timestamp"].replace("Z", "+00:00"))
            media_list.append(InstagramMedia(**item))
        
        return media_list
    
    # ========== Utility Methods ==========
    
    def get_rate_limit_status(self) -> Dict:
        """
        Get current rate limit status
        
        Returns:
            Dictionary with remaining calls and time info
        """
        return {
            "remaining_calls": self.rate_limiter.get_remaining_calls(),
            "max_calls_per_hour": self.rate_limiter.max_calls,
            "time_until_reset": self.rate_limiter.time_until_next_call()
        }


# ========== Context Manager Support ==========

class InstagramAPIContext:
    """Context manager for Instagram API client"""
    
    def __init__(self, access_token: Optional[str] = None):
        self.access_token = access_token
        self.client: Optional[InstagramGraphAPI] = None
    
    async def __aenter__(self) -> InstagramGraphAPI:
        self.client = InstagramGraphAPI(self.access_token)
        return self.client
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.close()


# ========== Factory Function ==========

def create_instagram_client(access_token: Optional[str] = None) -> InstagramGraphAPI:
    """
    Factory function to create Instagram API client
    
    Args:
        access_token: Instagram access token (optional)
        
    Returns:
        InstagramGraphAPI instance
    """
    return InstagramGraphAPI(access_token)
