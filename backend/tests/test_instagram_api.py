"""
Instagram Graph API Client Tests

Unit tests for Instagram API client functionality
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from datetime import datetime

from app.integrations.instagram_api import (
    InstagramGraphAPI,
    RateLimiter,
    InstagramAPIError,
    RateLimitError,
    TokenExpiredError,
    PermissionError,
    InstagramUser,
    InstagramMedia,
    InstagramHashtag
)


# ========== Rate Limiter Tests ==========

def test_rate_limiter_allows_calls():
    """Test that rate limiter allows calls under the limit"""
    limiter = RateLimiter(max_calls=5, period=60)
    
    # First 5 calls should be allowed
    for i in range(5):
        assert limiter.is_allowed() == True
    
    # 6th call should be denied
    assert limiter.is_allowed() == False


def test_rate_limiter_remaining_calls():
    """Test remaining calls calculation"""
    limiter = RateLimiter(max_calls=10, period=60)
    
    assert limiter.get_remaining_calls() == 10
    
    # Make 3 calls
    for i in range(3):
        limiter.is_allowed()
    
    assert limiter.get_remaining_calls() == 7


def test_rate_limiter_time_until_reset():
    """Test time until next call is allowed"""
    limiter = RateLimiter(max_calls=2, period=60)
    
    # Under limit - no wait time
    assert limiter.time_until_next_call() == 0.0
    
    # Use up calls
    limiter.is_allowed()
    limiter.is_allowed()
    
    # Over limit - should have wait time
    wait_time = limiter.time_until_next_call()
    assert wait_time > 0


# ========== API Client Tests ==========

@pytest.mark.asyncio
async def test_instagram_api_initialization():
    """Test API client initialization"""
    client = InstagramGraphAPI(access_token="test_token")
    
    assert client.access_token == "test_token"
    assert client.rate_limiter is not None
    assert client.rate_limiter.max_calls == 200
    
    await client.close()


@pytest.mark.asyncio
async def test_build_url():
    """Test URL building"""
    client = InstagramGraphAPI()
    
    url = client._build_url("me")
    assert url == "https://graph.instagram.com/me"
    
    url = client._build_url("/me/media")
    assert url == "https://graph.instagram.com/me/media"
    
    await client.close()


@pytest.mark.asyncio
async def test_make_request_rate_limit():
    """Test rate limiting in requests"""
    client = InstagramGraphAPI()
    
    # Mock rate limiter to deny requests
    client.rate_limiter.is_allowed = Mock(return_value=False)
    client.rate_limiter.time_until_next_call = Mock(return_value=60.0)
    
    with pytest.raises(RateLimitError):
        await client._make_request("GET", "me")
    
    await client.close()


@pytest.mark.asyncio
async def test_handle_api_error_token_expired():
    """Test handling of expired token error"""
    client = InstagramGraphAPI()
    
    # Mock HTTP response with token expired error
    with patch.object(client.client, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": {
                "code": 190,
                "message": "Access token has expired",
                "type": "OAuthException"
            }
        }
        mock_get.return_value = mock_response
        
        client.rate_limiter.is_allowed = Mock(return_value=True)
        
        with pytest.raises(TokenExpiredError):
            await client._make_request("GET", "me")
    
    await client.close()


@pytest.mark.asyncio
async def test_handle_api_error_permission():
    """Test handling of permission error"""
    client = InstagramGraphAPI()
    
    # Mock HTTP response with permission error
    with patch.object(client.client, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "error": {
                "code": 200,
                "message": "Permission denied",
                "type": "PermissionError"
            }
        }
        mock_get.return_value = mock_response
        
        client.rate_limiter.is_allowed = Mock(return_value=True)
        
        with pytest.raises(PermissionError):
            await client._make_request("GET", "me")
    
    await client.close()


@pytest.mark.asyncio
async def test_get_user_profile():
    """Test getting user profile"""
    client = InstagramGraphAPI(access_token="test_token")
    
    # Mock successful API response
    with patch.object(client.client, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": "12345",
            "username": "test_user",
            "account_type": "BUSINESS",
            "media_count": 100
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client.rate_limiter.is_allowed = Mock(return_value=True)
        
        user = await client.get_user_profile("12345")
        
        assert isinstance(user, InstagramUser)
        assert user.id == "12345"
        assert user.username == "test_user"
        assert user.account_type == "BUSINESS"
        assert user.media_count == 100
    
    await client.close()


@pytest.mark.asyncio
async def test_get_user_media():
    """Test getting user media"""
    client = InstagramGraphAPI(access_token="test_token")
    
    # Mock successful API response
    with patch.object(client.client, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "media_1",
                    "caption": "Test post",
                    "media_type": "IMAGE",
                    "media_url": "https://example.com/image.jpg",
                    "permalink": "https://instagram.com/p/test",
                    "timestamp": "2024-01-15T10:00:00+0000",
                    "like_count": 100,
                    "comments_count": 10
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client.rate_limiter.is_allowed = Mock(return_value=True)
        
        media_list = await client.get_user_media("12345", limit=10)
        
        assert len(media_list) == 1
        assert isinstance(media_list[0], InstagramMedia)
        assert media_list[0].id == "media_1"
        assert media_list[0].caption == "Test post"
        assert media_list[0].like_count == 100
    
    await client.close()


@pytest.mark.asyncio
async def test_search_hashtag():
    """Test hashtag search"""
    client = InstagramGraphAPI(access_token="test_token")
    
    # Mock successful API response
    with patch.object(client.client, 'get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "hashtag_123",
                    "name": "kbeauty"
                }
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client.rate_limiter.is_allowed = Mock(return_value=True)
        
        hashtag = await client.search_hashtag("user_123", "kbeauty")
        
        assert hashtag is not None
        assert isinstance(hashtag, InstagramHashtag)
        assert hashtag.id == "hashtag_123"
        assert hashtag.name == "kbeauty"
    
    await client.close()


@pytest.mark.asyncio
async def test_get_rate_limit_status():
    """Test getting rate limit status"""
    client = InstagramGraphAPI()
    
    # Make some calls
    client.rate_limiter.is_allowed()
    client.rate_limiter.is_allowed()
    client.rate_limiter.is_allowed()
    
    status = client.get_rate_limit_status()
    
    assert "remaining_calls" in status
    assert "max_calls_per_hour" in status
    assert "time_until_reset" in status
    assert status["max_calls_per_hour"] == 200
    assert status["remaining_calls"] == 197  # 200 - 3 calls
    
    await client.close()


@pytest.mark.asyncio
async def test_context_manager():
    """Test using client as async context manager"""
    from app.integrations.instagram_api import InstagramAPIContext
    
    async with InstagramAPIContext("test_token") as client:
        assert isinstance(client, InstagramGraphAPI)
        assert client.access_token == "test_token"
    
    # Client should be closed after context


# ========== Pydantic Model Tests ==========

def test_instagram_user_model():
    """Test InstagramUser model"""
    user = InstagramUser(
        id="123",
        username="test_user",
        account_type="PERSONAL",
        media_count=50
    )
    
    assert user.id == "123"
    assert user.username == "test_user"
    assert user.account_type == "PERSONAL"
    assert user.media_count == 50


def test_instagram_media_model():
    """Test InstagramMedia model"""
    media = InstagramMedia(
        id="media_123",
        caption="Test caption",
        media_type="IMAGE",
        media_url="https://example.com/image.jpg",
        permalink="https://instagram.com/p/test",
        timestamp=datetime.now(),
        like_count=100,
        comments_count=10
    )
    
    assert media.id == "media_123"
    assert media.caption == "Test caption"
    assert media.media_type == "IMAGE"
    assert media.like_count == 100
    assert media.comments_count == 10


def test_instagram_hashtag_model():
    """Test InstagramHashtag model"""
    hashtag = InstagramHashtag(
        id="hashtag_123",
        name="kbeauty"
    )
    
    assert hashtag.id == "hashtag_123"
    assert hashtag.name == "kbeauty"


# ========== Integration Tests ==========

@pytest.mark.asyncio
@pytest.mark.integration
async def test_full_oauth_flow():
    """
    Integration test for full OAuth flow
    
    Note: This test requires real Instagram App credentials
    and should be run manually or in CI with proper setup
    """
    pytest.skip("Requires real Instagram App credentials")
    
    # This would test:
    # 1. Exchange code for short token
    # 2. Exchange short token for long token
    # 3. Use long token to fetch data
    # 4. Refresh long token


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
