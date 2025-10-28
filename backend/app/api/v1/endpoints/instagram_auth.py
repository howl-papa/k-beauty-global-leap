"""
Instagram OAuth 2.0 Authentication Endpoints

Handles Instagram login flow and token management
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict
from datetime import datetime, timedelta

from app.core.database import get_db
from app.core.config import get_settings
from app.integrations.instagram_api import InstagramGraphAPI, InstagramAPIError
from app.models.user import User
from app.api.v1.endpoints.auth import get_current_user


router = APIRouter()
settings = get_settings()


@router.get("/login")
async def instagram_login():
    """
    Redirect user to Instagram authorization page
    
    Step 1 of OAuth 2.0 flow
    """
    if not settings.INSTAGRAM_APP_ID:
        raise HTTPException(
            status_code=503,
            detail="Instagram API not configured. Please set INSTAGRAM_APP_ID in environment variables."
        )
    
    # Build authorization URL
    auth_url = (
        f"https://api.instagram.com/oauth/authorize"
        f"?client_id={settings.INSTAGRAM_APP_ID}"
        f"&redirect_uri={settings.INSTAGRAM_REDIRECT_URI}"
        f"&scope=user_profile,user_media"
        f"&response_type=code"
    )
    
    return RedirectResponse(url=auth_url)


@router.get("/callback")
async def instagram_callback(
    code: str = Query(..., description="Authorization code from Instagram"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Handle Instagram OAuth callback
    
    Step 2 of OAuth 2.0 flow: Exchange code for access token
    
    Args:
        code: Authorization code from Instagram
        current_user: Currently logged in user
        db: Database session
        
    Returns:
        Success message with token info
    """
    try:
        instagram_client = InstagramGraphAPI()
        
        # Step 1: Exchange code for short-lived token
        short_token_data = await instagram_client.exchange_code_for_token(
            code=code,
            redirect_uri=settings.INSTAGRAM_REDIRECT_URI
        )
        
        short_token = short_token_data["access_token"]
        instagram_user_id = short_token_data["user_id"]
        
        # Step 2: Exchange short-lived token for long-lived token (60 days)
        long_token_data = await instagram_client.exchange_short_for_long_token(short_token)
        
        long_token = long_token_data["access_token"]
        expires_in = long_token_data.get("expires_in", 5184000)  # Default 60 days
        
        # Calculate expiration date
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        # Store token in user record
        current_user.instagram_access_token = long_token
        current_user.instagram_user_id = instagram_user_id
        current_user.instagram_token_expires_at = expires_at
        
        db.commit()
        db.refresh(current_user)
        
        await instagram_client.close()
        
        return {
            "success": True,
            "message": "Instagram account connected successfully",
            "instagram_user_id": instagram_user_id,
            "token_expires_at": expires_at.isoformat(),
            "expires_in_days": expires_in // 86400
        }
        
    except InstagramAPIError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Instagram API error: {e.message}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect Instagram account: {str(e)}"
        )


@router.post("/refresh-token")
async def refresh_instagram_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Refresh Instagram long-lived access token
    
    Extends token expiration by 60 days
    
    Returns:
        New token info
    """
    if not current_user.instagram_access_token:
        raise HTTPException(
            status_code=400,
            detail="No Instagram account connected. Please connect your Instagram account first."
        )
    
    try:
        instagram_client = InstagramGraphAPI(current_user.instagram_access_token)
        
        # Refresh token
        new_token_data = await instagram_client.refresh_long_lived_token(
            current_user.instagram_access_token
        )
        
        new_token = new_token_data["access_token"]
        expires_in = new_token_data.get("expires_in", 5184000)  # Default 60 days
        
        # Calculate new expiration date
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        # Update user record
        current_user.instagram_access_token = new_token
        current_user.instagram_token_expires_at = expires_at
        
        db.commit()
        db.refresh(current_user)
        
        await instagram_client.close()
        
        return {
            "success": True,
            "message": "Instagram token refreshed successfully",
            "token_expires_at": expires_at.isoformat(),
            "expires_in_days": expires_in // 86400
        }
        
    except InstagramAPIError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to refresh token: {e.message}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to refresh Instagram token: {str(e)}"
        )


@router.delete("/disconnect")
async def disconnect_instagram(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Disconnect Instagram account from user profile
    
    Removes stored access token
    """
    if not current_user.instagram_access_token:
        raise HTTPException(
            status_code=400,
            detail="No Instagram account connected"
        )
    
    # Remove Instagram credentials
    current_user.instagram_access_token = None
    current_user.instagram_user_id = None
    current_user.instagram_token_expires_at = None
    
    db.commit()
    
    return {
        "success": True,
        "message": "Instagram account disconnected successfully"
    }


@router.get("/status")
async def instagram_connection_status(
    current_user: User = Depends(get_current_user)
):
    """
    Check Instagram connection status
    
    Returns:
        Connection status and token info
    """
    if not current_user.instagram_access_token:
        return {
            "connected": False,
            "message": "No Instagram account connected"
        }
    
    # Check if token is expired or expiring soon (within 7 days)
    now = datetime.utcnow()
    expires_at = current_user.instagram_token_expires_at
    
    if expires_at:
        days_until_expiry = (expires_at - now).days
        is_expired = expires_at < now
        needs_refresh = days_until_expiry < 7
    else:
        days_until_expiry = None
        is_expired = True
        needs_refresh = True
    
    return {
        "connected": True,
        "instagram_user_id": current_user.instagram_user_id,
        "token_expires_at": expires_at.isoformat() if expires_at else None,
        "days_until_expiry": days_until_expiry,
        "is_expired": is_expired,
        "needs_refresh": needs_refresh,
        "message": "Instagram account connected"
    }


@router.get("/rate-limit")
async def get_rate_limit_status(
    current_user: User = Depends(get_current_user)
):
    """
    Get current Instagram API rate limit status
    
    Returns:
        Rate limit information
    """
    if not current_user.instagram_access_token:
        raise HTTPException(
            status_code=400,
            detail="No Instagram account connected"
        )
    
    instagram_client = InstagramGraphAPI(current_user.instagram_access_token)
    rate_limit_info = instagram_client.get_rate_limit_status()
    await instagram_client.close()
    
    return {
        "success": True,
        "rate_limit": rate_limit_info
    }
