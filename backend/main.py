from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="K-Beauty Global Leap API",
    description="AI-Powered Localization Platform for K-Beauty SMEs - Empowering small businesses to compete globally",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Yongrak Park",
        "url": "https://yongrak.pro",
        "email": "contact@yongrak.pro",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://k-beauty-leap.com",
        "https://www.k-beauty-leap.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - Welcome message
    """
    return {
        "message": "Welcome to K-Beauty Global Leap API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers
    """
    return {
        "status": "healthy",
        "service": "k-beauty-global-leap-api",
        "version": "0.1.0",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/status")
async def api_status():
    """
    API status and available features
    """
    return {
        "api_version": "v1",
        "status": "operational",
        "features": {
            "market_intelligence": {
                "description": "Real-time local trend analysis and competitor monitoring",
                "status": "in_development"
            },
            "cultural_adaptation": {
                "description": "AI-powered transcreation and localization",
                "status": "in_development"
            },
            "partner_verification": {
                "description": "AI-based partner credibility assessment",
                "status": "planned"
            },
            "roi_optimization": {
                "description": "Real-time campaign performance tracking and optimization",
                "status": "planned"
            }
        },
        "supported_markets": [
            "United States",
            "Germany",
            "France",
            "Japan",
            "China"
        ]
    }


# Include API routers
from app.api import api_router

app.include_router(api_router, prefix="/api/v1")

# Future API route groups
# from app.api import market_intelligence, cultural_adaptation, partner_verification, roi_optimization
# app.include_router(market_intelligence.router, prefix="/api/v1/market-intelligence", tags=["Market Intelligence"])
# app.include_router(cultural_adaptation.router, prefix="/api/v1/cultural-adaptation", tags=["Cultural Adaptation"])
# app.include_router(partner_verification.router, prefix="/api/v1/partner-verification", tags=["Partner Verification"])
# app.include_router(roi_optimization.router, prefix="/api/v1/roi-optimization", tags=["ROI Optimization"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
