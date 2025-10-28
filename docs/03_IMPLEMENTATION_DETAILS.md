# K-Beauty Global Leap - 구현 상세 문서

## 📂 프로젝트 구조 / Project Structure

```
webapp/
├── backend/                          # FastAPI Backend
│   ├── app/
│   │   ├── api/                      # API Endpoints
│   │   │   ├── deps.py               # Dependency injection
│   │   │   └── endpoints/
│   │   │       ├── auth.py           # Authentication endpoints
│   │   │       ├── instagram.py      # Instagram integration
│   │   │       ├── ai_analysis.py    # AI analysis endpoints
│   │   │       └── data.py           # Data collection endpoints
│   │   ├── core/                     # Core configurations
│   │   │   ├── config.py             # Application settings
│   │   │   ├── security.py           # JWT, password hashing
│   │   │   └── database.py           # Database connection
│   │   ├── models/                   # SQLAlchemy Models
│   │   │   ├── user.py               # User model
│   │   │   ├── company.py            # Company model
│   │   │   ├── instagram.py          # Instagram data models
│   │   │   └── analysis.py           # Analysis results model
│   │   ├── schemas/                  # Pydantic Schemas
│   │   │   ├── user.py               # User DTOs
│   │   │   ├── auth.py               # Auth request/response
│   │   │   ├── instagram.py          # Instagram DTOs
│   │   │   └── ai_analysis.py        # AI analysis DTOs
│   │   ├── services/                 # Business Logic
│   │   │   ├── ai_analyzer.py        # Core AI service
│   │   │   ├── ai_analyzer_extended.py  # Extended AI features
│   │   │   ├── cache_service.py      # Redis caching
│   │   │   └── market_intelligence.py   # Market insights
│   │   ├── integrations/             # External API Clients
│   │   │   ├── instagram_api.py      # Instagram Graph API
│   │   │   ├── openai_client.py      # OpenAI GPT-4
│   │   │   └── anthropic_client.py   # Anthropic Claude
│   │   ├── utils/                    # Utilities
│   │   │   ├── mock_data.py          # Mock data for testing
│   │   │   └── helpers.py            # Helper functions
│   │   └── main.py                   # FastAPI application
│   ├── alembic/                      # Database Migrations
│   │   ├── versions/                 # Migration files
│   │   └── env.py                    # Alembic configuration
│   ├── tests/                        # Backend Tests
│   │   ├── unit/                     # Unit tests
│   │   ├── integration/              # Integration tests
│   │   └── conftest.py               # Pytest fixtures
│   ├── requirements.txt              # Python dependencies
│   └── Dockerfile                    # Backend container
│
├── frontend/                         # Next.js Frontend
│   ├── src/
│   │   ├── app/                      # Next.js App Router
│   │   │   ├── (auth)/               # Auth routes
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── analysis/             # Analysis dashboards
│   │   │   │   ├── sentiment/        # Sentiment analysis page
│   │   │   │   ├── trends/           # Trend prediction page
│   │   │   │   ├── quality/          # Content quality page
│   │   │   │   └── influencers/      # Influencer analysis page
│   │   │   ├── dashboard/            # Main dashboard
│   │   │   ├── layout.tsx            # Root layout
│   │   │   └── page.tsx              # Home page
│   │   ├── components/               # React Components
│   │   │   ├── ai/                   # AI-related components
│   │   │   │   ├── ScoreCard.tsx     # Score display component
│   │   │   │   ├── InsightCard.tsx   # Insight display component
│   │   │   │   └── TrendChart.tsx    # Chart component
│   │   │   ├── layout/               # Layout components
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── common/               # Shared components
│   │   │       ├── Button.tsx
│   │   │       ├── Input.tsx
│   │   │       └── Modal.tsx
│   │   ├── store/                    # Zustand State Management
│   │   │   ├── authStore.ts          # Authentication state
│   │   │   └── analysisStore.ts      # Analysis results state
│   │   ├── utils/                    # Frontend Utilities
│   │   │   ├── api.ts                # Base API client
│   │   │   ├── aiAnalysisApi.ts      # AI analysis API client
│   │   │   └── auth.ts               # Auth utilities
│   │   └── types/                    # TypeScript Types
│   │       ├── user.ts
│   │       ├── analysis.ts
│   │       └── instagram.ts
│   ├── public/                       # Static assets
│   ├── package.json                  # Node dependencies
│   └── next.config.js                # Next.js configuration
│
├── docs/                             # Documentation
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── 02_TECHNICAL_ARCHITECTURE.md
│   ├── 03_IMPLEMENTATION_DETAILS.md  # This file
│   ├── AI_ANALYSIS_SYSTEM.md
│   └── INSTAGRAM_API_INTEGRATION.md
│
├── docker-compose.yml                # Local development setup
├── .env.example                      # Environment variables template
└── README.md                         # Project overview
```

---

## 🔑 핵심 기능 구현 상세 / Feature Implementation Details

### 1. 인증 시스템 (Authentication System)

#### 구현 로직 (Implementation Logic)

**Flow Diagram**:
```
User Registration/Login
    │
    ↓
┌─────────────────────────┐
│  Frontend Form Submit   │
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  POST /api/v1/auth/*    │
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  Pydantic Validation    │  ← Email format, password strength
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  Password Hashing       │  ← bcrypt
│  (bcrypt + salt)        │
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  Save to PostgreSQL     │
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  Generate JWT Token     │  ← HS256, 1-hour expiry
└─────────────────────────┘
    │
    ↓
┌─────────────────────────┐
│  Return Token           │
│  Store in Frontend      │  ← localStorage + Zustand
└─────────────────────────┘
```

#### 핵심 코드 (Core Code)

**Backend: `/backend/app/core/security.py`**

```python
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = "your-secret-key-here"  # From environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: timedelta = None
) -> str:
    """
    JWT 액세스 토큰 생성
    
    Args:
        subject: 토큰의 주체 (일반적으로 user ID)
        expires_delta: 토큰 만료 시간 (기본값: 60분)
    
    Returns:
        str: 인코딩된 JWT 토큰
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # JWT payload
    to_encode = {
        "exp": expire,  # Expiration time
        "sub": str(subject),  # Subject (user ID)
        "iat": datetime.utcnow()  # Issued at
    }
    
    # Encode JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 해시된 비밀번호 비교
    
    Args:
        plain_password: 사용자가 입력한 평문 비밀번호
        hashed_password: 데이터베이스에 저장된 해시된 비밀번호
    
    Returns:
        bool: 비밀번호 일치 여부
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    비밀번호 해싱
    
    Args:
        password: 평문 비밀번호
    
    Returns:
        str: bcrypt로 해싱된 비밀번호
    """
    return pwd_context.hash(password)
```

**Backend: `/backend/app/api/endpoints/auth.py`**

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token, verify_password, get_password_hash
from app.models.user import User
from app.schemas.auth import UserCreate, Token

router = APIRouter()


@router.post("/register", response_model=Token)
def register(
    user_in: UserCreate,
    db: Session = Depends(get_db)
):
    """
    새로운 사용자 등록
    
    Process:
    1. 이메일 중복 체크
    2. 비밀번호 해싱
    3. 데이터베이스에 사용자 생성
    4. JWT 토큰 발급
    """
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # 2. Hash password
    hashed_password = get_password_hash(user_in.password)
    
    # 3. Create user
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # 4. Generate JWT token
    access_token = create_access_token(subject=db_user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
def login(
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    사용자 로그인
    
    Process:
    1. 이메일로 사용자 조회
    2. 비밀번호 검증
    3. JWT 토큰 발급
    """
    # 1. Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # 2. Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # 3. Generate JWT token
    access_token = create_access_token(subject=user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
```

**Frontend: `/frontend/src/store/authStore.ts`**

```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface User {
  id: number;
  email: string;
  full_name: string;
}

interface AuthState {
  // State
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  
  // Actions
  login: (token: string, user: User) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

/**
 * 인증 상태 관리 스토어
 * 
 * Features:
 * - JWT 토큰 저장
 * - 사용자 정보 관리
 * - localStorage 영구 저장 (persist middleware)
 * - 로그인/로그아웃 처리
 */
export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // Initial state
      user: null,
      token: null,
      isAuthenticated: false,
      
      // Login action
      login: (token: string, user: User) => {
        set({
          token,
          user,
          isAuthenticated: true
        });
      },
      
      // Logout action
      logout: () => {
        set({
          token: null,
          user: null,
          isAuthenticated: false
        });
        // Clear localStorage
        localStorage.removeItem('auth-storage');
      },
      
      // Update user action
      setUser: (user: User) => {
        set({ user });
      }
    }),
    {
      name: 'auth-storage', // localStorage key
      // Only persist token and user
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        isAuthenticated: state.isAuthenticated
      })
    }
  )
);
```

---

### 2. Instagram OAuth 통합 (Instagram OAuth Integration)

#### 구현 로직 (Implementation Logic)

**OAuth 2.0 Flow**:
```
Step 1: Authorization Request
┌─────────────────────────────────────────┐
│ Frontend: Get Authorization URL        │
│ GET /api/v1/instagram/auth-url          │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ Backend: Build Instagram OAuth URL      │
│ https://api.instagram.com/oauth/        │
│   authorize?client_id=...                │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ User: Redirected to Instagram           │
│ User authorizes app                      │
└─────────────────────────────────────────┘
    │
    ↓
Step 2: Authorization Code Callback
┌─────────────────────────────────────────┐
│ Instagram: Redirects to callback URL    │
│ http://localhost:3000/callback?code=... │
└─────────────────────────────────────────┘
    │
    ↓
Step 3: Token Exchange
┌─────────────────────────────────────────┐
│ Frontend: Send code to backend          │
│ POST /api/v1/instagram/callback          │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ Backend: Exchange code for token        │
│ POST to Instagram Graph API              │
│ - Short-lived token (1 hour)            │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ Backend: Exchange for long-lived token  │
│ GET to Instagram Graph API               │
│ - Long-lived token (60 days)            │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ Backend: Save token to database         │
│ UPDATE users SET instagram_access_token  │
└─────────────────────────────────────────┘
    │
    ↓
┌─────────────────────────────────────────┐
│ Return success to frontend              │
└─────────────────────────────────────────┘
```

#### 핵심 코드 (Core Code)

**Backend: `/backend/app/integrations/instagram_api.py`**

```python
import httpx
from datetime import datetime, timedelta
from typing import Optional, Dict
from app.core.config import settings

class InstagramGraphAPI:
    """
    Instagram Graph API 클라이언트
    
    Features:
    - OAuth 2.0 인증 플로우
    - 3단계 토큰 교환 (code → short-lived → long-lived)
    - Rate limiting (200 calls/hour)
    - 자동 토큰 갱신
    """
    
    def __init__(self):
        self.client_id = settings.INSTAGRAM_CLIENT_ID
        self.client_secret = settings.INSTAGRAM_CLIENT_SECRET
        self.base_url = "https://graph.instagram.com"
        self.oauth_url = "https://api.instagram.com/oauth"
        
        # Rate limiter
        self.rate_limiter = RateLimiter(max_calls=200, period=3600)
    
    
    def get_authorization_url(self, redirect_uri: str, state: str = None) -> str:
        """
        Step 1: Instagram OAuth 인증 URL 생성
        
        Args:
            redirect_uri: 콜백 URL (예: http://localhost:3000/callback)
            state: CSRF 방지용 랜덤 문자열 (옵션)
        
        Returns:
            str: Instagram 인증 페이지 URL
        """
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": "user_profile,user_media",  # 필요한 권한
            "response_type": "code"
        }
        
        if state:
            params["state"] = state
        
        # Build URL
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.oauth_url}/authorize?{query_string}"
    
    
    async def exchange_code_for_token(
        self, 
        code: str, 
        redirect_uri: str
    ) -> Dict:
        """
        Step 2: Authorization code를 short-lived token으로 교환
        
        Args:
            code: Instagram으로부터 받은 authorization code
            redirect_uri: 등록된 콜백 URL (Step 1과 동일해야 함)
        
        Returns:
            Dict: {
                "access_token": "short-lived-token",
                "user_id": "17841405793187218"
            }
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.oauth_url}/access_token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                    "code": code
                }
            )
            response.raise_for_status()
            return response.json()
    
    
    async def exchange_short_for_long_token(
        self, 
        short_lived_token: str
    ) -> Dict:
        """
        Step 3: Short-lived token을 long-lived token으로 교환
        
        Short-lived: 1시간 유효
        Long-lived: 60일 유효
        
        Args:
            short_lived_token: Step 2에서 받은 토큰
        
        Returns:
            Dict: {
                "access_token": "long-lived-token",
                "token_type": "bearer",
                "expires_in": 5183944  # 60 days in seconds
            }
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/access_token",
                params={
                    "grant_type": "ig_exchange_token",
                    "client_secret": self.client_secret,
                    "access_token": short_lived_token
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Calculate expiration datetime
            expires_at = datetime.utcnow() + timedelta(
                seconds=data["expires_in"]
            )
            data["expires_at"] = expires_at
            
            return data
    
    
    async def refresh_long_lived_token(
        self, 
        long_lived_token: str
    ) -> Dict:
        """
        Long-lived token 갱신 (만료 전 갱신 필요)
        
        Note: 만료 24시간 전에 갱신 권장
        
        Args:
            long_lived_token: 현재 long-lived token
        
        Returns:
            Dict: 새로운 long-lived token 정보
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/refresh_access_token",
                params={
                    "grant_type": "ig_refresh_token",
                    "access_token": long_lived_token
                }
            )
            response.raise_for_status()
            data = response.json()
            
            # Calculate new expiration
            expires_at = datetime.utcnow() + timedelta(
                seconds=data["expires_in"]
            )
            data["expires_at"] = expires_at
            
            return data
    
    
    async def get_user_profile(
        self, 
        user_id: str, 
        access_token: str,
        fields: list = None
    ) -> Dict:
        """
        Instagram 사용자 프로필 정보 조회
        
        Args:
            user_id: Instagram user ID
            access_token: Long-lived access token
            fields: 조회할 필드 리스트 (기본값: 기본 필드)
        
        Returns:
            Dict: 사용자 프로필 정보
        """
        # Check rate limit
        if not self.rate_limiter.is_allowed():
            raise RateLimitException(
                f"Rate limit exceeded. Wait {self.rate_limiter.get_wait_time()}s"
            )
        
        # Default fields
        if fields is None:
            fields = [
                "id", "username", "account_type", 
                "media_count", "followers_count", "follows_count"
            ]
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/{user_id}",
                params={
                    "fields": ",".join(fields),
                    "access_token": access_token
                }
            )
            response.raise_for_status()
            
            # Record API call
            self.rate_limiter.record_call()
            
            return response.json()


class RateLimiter:
    """
    API Rate Limiter
    
    Instagram API Limit: 200 calls per hour per user
    """
    
    def __init__(self, max_calls: int = 200, period: int = 3600):
        self.max_calls = max_calls
        self.period = period  # seconds
        self.calls = []  # List of call timestamps
    
    def is_allowed(self) -> bool:
        """현재 API 호출이 허용되는지 확인"""
        self._cleanup_old_calls()
        return len(self.calls) < self.max_calls
    
    def record_call(self):
        """API 호출 기록"""
        self.calls.append(datetime.utcnow())
    
    def get_remaining_calls(self) -> int:
        """남은 API 호출 횟수"""
        self._cleanup_old_calls()
        return self.max_calls - len(self.calls)
    
    def _cleanup_old_calls(self):
        """기간이 지난 호출 기록 제거"""
        cutoff = datetime.utcnow() - timedelta(seconds=self.period)
        self.calls = [call for call in self.calls if call > cutoff]
```

---

### 3. AI 감성 분석 (AI Sentiment Analysis)

#### 구현 로직 (Implementation Logic)

**Analysis Flow**:
```
User Request (market, hashtags, sample_size)
    │
    ↓
┌──────────────────────────────────────────┐
│ Check Redis Cache                        │
│ Key: sentiment:{market}:{hashtags}       │
└──────────────────────────────────────────┘
    │
    ├─ Cache Hit ──→ Return cached result
    │
    ↓ Cache Miss
┌──────────────────────────────────────────┐
│ Collect Instagram Posts                  │
│ - Search by hashtags                     │
│ - Filter by market                       │
│ - Get sample_size posts                  │
└──────────────────────────────────────────┘
    │
    ↓
┌──────────────────────────────────────────┐
│ Prepare AI Prompt                        │
│ - Posts captions                         │
│ - Comments                               │
│ - Engagement metrics                     │
└──────────────────────────────────────────┘
    │
    ↓
┌──────────────────────────────────────────┐
│ Call GPT-4 API                           │
│ - System prompt (market expert)          │
│ - User prompt (analysis request)         │
│ - Response format: JSON                  │
└──────────────────────────────────────────┘
    │
    ↓
┌──────────────────────────────────────────┐
│ Parse AI Response                        │
│ - Overall sentiment                      │
│ - Sentiment score (0-100)                │
│ - Key themes                             │
│ - Trending topics                        │
└──────────────────────────────────────────┘
    │
    ↓
┌──────────────────────────────────────────┐
│ Cache Result (24 hours TTL)              │
│ Save to PostgreSQL for audit            │
└──────────────────────────────────────────┘
    │
    ↓
Return Result to Frontend
```

#### 핵심 코드 (Core Code)

**Backend: `/backend/app/services/ai_analyzer.py`**

```python
import json
from typing import Dict, List
import openai
from app.core.config import settings
from app.services.cache_service import CacheService

class AIAnalyzer:
    """
    AI 기반 소셜 미디어 분석 서비스
    
    Features:
    - GPT-4 감성 분석
    - 트렌드 예측
    - 콘텐츠 품질 평가
    - Redis 캐싱 (비용 최적화)
    """
    
    def __init__(self):
        self.client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.cache = CacheService()
        self.model = "gpt-4-turbo-preview"
    
    
    async def analyze_sentiment(
        self,
        market: str,
        posts: List[Dict],
        detailed: bool = True
    ) -> Dict:
        """
        Instagram 게시물 감성 분석
        
        Args:
            market: 타겟 시장 (DE, FR, JP 등)
            posts: 분석할 게시물 리스트
            detailed: 상세 분석 여부
        
        Returns:
            Dict: {
                "overall_sentiment": "positive" | "neutral" | "negative",
                "sentiment_score": 0-100,
                "key_themes": ["theme1", "theme2"],
                "trending_topics": ["topic1", "topic2"],
                "analysis_summary": "..."
            }
        """
        # 1. Generate cache key
        cache_key = f"sentiment:{market}:{len(posts)}"
        
        # 2. Check cache
        cached = await self.cache.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # 3. Prepare prompt
        system_prompt = self._get_sentiment_system_prompt(market)
        user_prompt = self._prepare_sentiment_user_prompt(posts, detailed)
        
        # 4. Call GPT-4
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},  # JSON mode
            temperature=0.3  # Lower temp for consistent analysis
        )
        
        # 5. Parse response
        result = json.loads(response.choices[0].message.content)
        
        # 6. Add metadata
        result["posts_analyzed"] = len(posts)
        result["market"] = market
        result["model_used"] = self.model
        result["tokens_used"] = response.usage.total_tokens
        result["cached"] = False
        
        # 7. Cache result (24 hours)
        await self.cache.set(
            cache_key, 
            json.dumps(result), 
            ttl=86400  # 24 hours
        )
        
        return result
    
    
    def _get_sentiment_system_prompt(self, market: str) -> str:
        """
        시장별 감성 분석 시스템 프롬프트
        
        Purpose: GPT-4에게 역할과 맥락 제공
        """
        market_context = {
            "DE": "German beauty market expert with deep understanding of "
                  "German consumer preferences, cultural nuances, and "
                  "beauty trends in Deutschland.",
            "FR": "French beauty market expert familiar with French "
                  "elegance, skincare philosophy, and Parisian beauty standards.",
            "JP": "Japanese beauty market expert with knowledge of "
                  "J-beauty trends, kawaii culture, and Japanese "
                  "skincare rituals."
        }
        
        context = market_context.get(
            market, 
            f"Beauty market expert for {market}"
        )
        
        return f"""You are a {context}

Your task is to analyze Instagram posts related to K-Beauty products 
and provide sentiment analysis.

Consider:
1. Overall sentiment (positive, neutral, negative)
2. Sentiment intensity (0-100 score)
3. Key themes mentioned in posts
4. Trending topics and hashtags
5. Cultural context of the market

Provide your analysis in JSON format with the following structure:
{{
    "overall_sentiment": "positive" | "neutral" | "negative",
    "sentiment_score": 0-100,
    "key_themes": ["theme1", "theme2", ...],
    "trending_topics": ["topic1", "topic2", ...],
    "analysis_summary": "2-3 sentence summary"
}}
"""
    
    
    def _prepare_sentiment_user_prompt(
        self, 
        posts: List[Dict],
        detailed: bool
    ) -> str:
        """
        사용자 프롬프트 준비 (분석할 데이터 포함)
        """
        # Extract captions from posts
        captions = [post.get("caption", "") for post in posts]
        
        # Prepare post summaries
        post_summaries = []
        for i, post in enumerate(posts[:20], 1):  # Limit to 20 for token efficiency
            summary = f"{i}. "
            summary += f"Caption: {post.get('caption', 'No caption')[:200]}... "
            summary += f"Likes: {post.get('like_count', 0)}, "
            summary += f"Comments: {post.get('comments_count', 0)}"
            post_summaries.append(summary)
        
        prompt = f"""Analyze the sentiment of these {len(posts)} Instagram posts 
about K-Beauty products:

{chr(10).join(post_summaries)}

Please provide:
1. Overall sentiment trend
2. Numerical sentiment score (0=very negative, 100=very positive)
3. Top 5 key themes discussed
4. Top 5 trending topics
5. Brief analysis summary

Focus on authenticity, engagement quality, and cultural fit.
"""
        
        return prompt
```

**Frontend: `/frontend/src/app/analysis/sentiment/page.tsx`**

```typescript
'use client';

import { useState } from 'react';
import { aiAnalysisApi } from '@/utils/aiAnalysisApi';
import ScoreCard from '@/components/ai/ScoreCard';
import InsightCard from '@/components/ai/InsightCard';

/**
 * 감성 분석 대시보드 페이지
 * 
 * Features:
 * - 시장 선택 (DE, FR, JP)
 * - 해시태그 필터링
 * - 샘플 크기 조정
 * - 실시간 분석 결과 표시
 */
export default function SentimentAnalysisPage() {
  // State management
  const [market, setMarket] = useState<'DE' | 'FR' | 'JP'>('DE');
  const [hashtags, setHashtags] = useState<string[]>(['#kbeauty']);
  const [sampleSize, setSampleSize] = useState(50);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  /**
   * 감성 분석 실행
   */
  const runAnalysis = async () => {
    setLoading(true);
    try {
      // Call API
      const analysisResult = await aiAnalysisApi.analyzeSentiment({
        market,
        hashtags,
        sample_size: sampleSize,
        time_range: '7d'
      });
      
      setResult(analysisResult);
    } catch (error) {
      console.error('Analysis failed:', error);
      alert('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <h1 className="text-3xl font-bold mb-8">
        Sentiment Analysis Dashboard
      </h1>

      {/* Controls */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Market Selection */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Target Market
            </label>
            <select
              value={market}
              onChange={(e) => setMarket(e.target.value as any)}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="DE">🇩🇪 Germany</option>
              <option value="FR">🇫🇷 France</option>
              <option value="JP">🇯🇵 Japan</option>
            </select>
          </div>

          {/* Hashtag Input */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Hashtags
            </label>
            <input
              type="text"
              value={hashtags.join(', ')}
              onChange={(e) => setHashtags(
                e.target.value.split(',').map(h => h.trim())
              )}
              placeholder="#kbeauty, #skincare"
              className="w-full px-4 py-2 border rounded-lg"
            />
          </div>

          {/* Sample Size */}
          <div>
            <label className="block text-sm font-medium mb-2">
              Sample Size: {sampleSize}
            </label>
            <input
              type="range"
              min="10"
              max="100"
              step="10"
              value={sampleSize}
              onChange={(e) => setSampleSize(Number(e.target.value))}
              className="w-full"
            />
          </div>
        </div>

        {/* Analyze Button */}
        <button
          onClick={runAnalysis}
          disabled={loading}
          className="mt-6 w-full bg-blue-600 text-white py-3 rounded-lg
                     hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {loading ? 'Analyzing...' : 'Run Analysis'}
        </button>
      </div>

      {/* Results */}
      {result && (
        <div className="space-y-6">
          {/* Sentiment Score */}
          <ScoreCard
            title="Overall Sentiment"
            score={result.sentiment_score}
            subtitle={result.overall_sentiment.toUpperCase()}
            type="circular"
            size="lg"
          />

          {/* Key Themes */}
          <InsightCard
            title="Key Themes"
            items={result.key_themes}
            icon="💡"
          />

          {/* Trending Topics */}
          <InsightCard
            title="Trending Topics"
            items={result.trending_topics}
            icon="📈"
          />

          {/* Analysis Summary */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4">
              Analysis Summary
            </h3>
            <p className="text-gray-700 leading-relaxed">
              {result.analysis_summary}
            </p>
          </div>

          {/* Metadata */}
          <div className="text-sm text-gray-500">
            Analyzed {result.posts_analyzed} posts • 
            {result.cached ? ' From cache' : ' Fresh analysis'} • 
            Generated at {new Date(result.analyzed_at).toLocaleString()}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

### 4. Redis 캐싱 시스템 (Redis Caching System)

#### 구현 로직 (Implementation Logic)

**Caching Strategy**:
```
Request → Check Cache → Cache Hit? → Return
                ↓
              Cache Miss
                ↓
         Compute Result
                ↓
         Store in Cache (with TTL)
                ↓
              Return
```

#### 핵심 코드 (Core Code)

**Backend: `/backend/app/services/cache_service.py`**

```python
import json
import redis.asyncio as redis
from typing import Optional, Any
from app.core.config import settings

class CacheService:
    """
    Redis 캐싱 서비스
    
    Features:
    - 비동기 Redis 클라이언트
    - TTL 기반 캐싱
    - JSON 직렬화/역직렬화
    - 비용 최적화 (AI API 호출 감소)
    
    Cache Strategy:
    - Sentiment Analysis: 24 hours (market sentiment changes slowly)
    - Content Quality: 24 hours (post quality is stable)
    - Influencer Authenticity: 7 days (metrics update weekly)
    - Cultural Fit: 7 days (cultural rules are stable)
    - Trend Analysis: 1 hour (trends change frequently)
    """
    
    def __init__(self):
        self.redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        
        # Default TTLs (seconds)
        self.default_ttls = {
            "sentiment": 86400,      # 24 hours
            "quality": 86400,        # 24 hours
            "authenticity": 604800,  # 7 days
            "cultural": 604800,      # 7 days
            "trend": 3600,           # 1 hour
            "performance": 3600      # 1 hour
        }
    
    
    async def get(self, key: str) -> Optional[str]:
        """
        캐시에서 값 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            Optional[str]: 캐시된 값 (없으면 None)
        """
        try:
            value = await self.redis_client.get(key)
            return value
        except Exception as e:
            # Log error but don't fail the request
            print(f"Cache get error: {e}")
            return None
    
    
    async def set(
        self, 
        key: str, 
        value: str, 
        ttl: int = None
    ) -> bool:
        """
        캐시에 값 저장
        
        Args:
            key: 캐시 키
            value: 저장할 값 (문자열 또는 JSON)
            ttl: Time-to-live (초 단위, None이면 영구 저장)
        
        Returns:
            bool: 성공 여부
        """
        try:
            if ttl:
                await self.redis_client.setex(key, ttl, value)
            else:
                await self.redis_client.set(key, value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    
    async def delete(self, key: str) -> bool:
        """
        캐시에서 값 삭제
        
        Args:
            key: 캐시 키
        
        Returns:
            bool: 성공 여부
        """
        try:
            await self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    
    async def get_json(self, key: str) -> Optional[dict]:
        """
        JSON 형식 캐시 조회
        
        Args:
            key: 캐시 키
        
        Returns:
            Optional[dict]: JSON 파싱된 결과
        """
        value = await self.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return None
        return None
    
    
    async def set_json(
        self, 
        key: str, 
        value: dict, 
        ttl: int = None
    ) -> bool:
        """
        JSON 형식으로 캐시 저장
        
        Args:
            key: 캐시 키
            value: 저장할 딕셔너리
            ttl: Time-to-live (초)
        
        Returns:
            bool: 성공 여부
        """
        try:
            json_str = json.dumps(value)
            return await self.set(key, json_str, ttl)
        except Exception as e:
            print(f"Cache set_json error: {e}")
            return False
    
    
    def get_ttl_for_analysis_type(self, analysis_type: str) -> int:
        """
        분석 타입별 적절한 TTL 반환
        
        Args:
            analysis_type: 분석 타입 (sentiment, quality, etc.)
        
        Returns:
            int: TTL (초)
        """
        return self.default_ttls.get(analysis_type, 3600)
    
    
    async def get_cache_stats(self) -> dict:
        """
        캐시 통계 조회
        
        Returns:
            dict: Redis 통계 정보
        """
        info = await self.redis_client.info()
        return {
            "total_keys": info.get("db0", {}).get("keys", 0),
            "memory_used": info.get("used_memory_human"),
            "hit_rate": self._calculate_hit_rate(info),
            "uptime_days": info.get("uptime_in_days")
        }
    
    
    def _calculate_hit_rate(self, info: dict) -> float:
        """
        캐시 히트율 계산
        
        Hit Rate = Hits / (Hits + Misses)
        """
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        if total == 0:
            return 0.0
        
        return round((hits / total) * 100, 2)
```

---

## 🧪 테스트 및 검증 / Testing & Validation

### Backend Unit Tests

**Example: `/backend/tests/unit/test_ai_analyzer.py`**

```python
import pytest
from app.services.ai_analyzer import AIAnalyzer

@pytest.mark.asyncio
async def test_sentiment_analysis():
    """감성 분석 기능 테스트"""
    analyzer = AIAnalyzer()
    
    # Mock posts
    posts = [
        {
            "caption": "Love this K-Beauty serum! #kbeauty",
            "like_count": 100,
            "comments_count": 10
        },
        {
            "caption": "Amazing results with Korean skincare",
            "like_count": 150,
            "comments_count": 15
        }
    ]
    
    # Run analysis
    result = await analyzer.analyze_sentiment(
        market="DE",
        posts=posts,
        detailed=True
    )
    
    # Assertions
    assert "overall_sentiment" in result
    assert result["sentiment_score"] >= 0
    assert result["sentiment_score"] <= 100
    assert len(result["key_themes"]) > 0
    assert result["posts_analyzed"] == 2
```

### Frontend Component Tests

**Example: `/frontend/src/components/ai/ScoreCard.test.tsx`**

```typescript
import { render, screen } from '@testing-library/react';
import ScoreCard from './ScoreCard';

describe('ScoreCard Component', () => {
  it('renders score correctly', () => {
    render(
      <ScoreCard
        title="Test Score"
        score={85}
        subtitle="High Performance"
      />
    );
    
    expect(screen.getByText('Test Score')).toBeInTheDocument();
    expect(screen.getByText('85')).toBeInTheDocument();
    expect(screen.getByText('High Performance')).toBeInTheDocument();
  });
  
  it('applies correct color based on score', () => {
    const { container } = render(
      <ScoreCard title="Test" score={85} />
    );
    
    // Score 85 should be green (80+)
    const scoreElement = container.querySelector('[class*="green"]');
    expect(scoreElement).toBeInTheDocument();
  });
});
```

---

## 🔧 환경 설정 / Environment Configuration

### Backend Environment Variables

**File: `/backend/.env`**

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/kbeauty_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Secret
SECRET_KEY=your-super-secret-jwt-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Instagram API
INSTAGRAM_CLIENT_ID=your_instagram_app_id
INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret
INSTAGRAM_REDIRECT_URI=http://localhost:3000/callback

# OpenAI
OPENAI_API_KEY=sk-your-openai-api-key

# Anthropic
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key

# Application
APP_NAME=K-Beauty Global Leap
APP_VERSION=0.1.0
DEBUG=True

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]
```

### Frontend Environment Variables

**File: `/frontend/.env.local`**

```bash
# API Base URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Feature Flags
NEXT_PUBLIC_ENABLE_MOCK_DATA=true
NEXT_PUBLIC_ENABLE_ANALYTICS=false

# App Info
NEXT_PUBLIC_APP_NAME=K-Beauty Global Leap
NEXT_PUBLIC_APP_VERSION=0.1.0
```

---

## 📝 주요 파일 설명 / Key File Descriptions

### Backend Core Files

| File Path | Purpose | Key Functions |
|-----------|---------|--------------|
| `app/main.py` | FastAPI 애플리케이션 진입점 | `create_app()`, CORS, middleware |
| `app/core/config.py` | 환경 변수 및 설정 관리 | `Settings` class with Pydantic |
| `app/core/database.py` | 데이터베이스 연결 설정 | `get_db()`, session management |
| `app/api/deps.py` | 의존성 주입 (DI) | `get_current_user()`, `get_db()` |
| `app/services/ai_analyzer.py` | AI 분석 핵심 로직 | `analyze_sentiment()`, `predict_trends()` |
| `app/integrations/instagram_api.py` | Instagram API 클라이언트 | OAuth flow, data collection |

### Frontend Core Files

| File Path | Purpose | Key Features |
|-----------|---------|--------------|
| `src/app/layout.tsx` | 루트 레이아웃 | Provider 설정, 전역 스타일 |
| `src/utils/api.ts` | HTTP 클라이언트 베이스 | Axios instance, interceptors |
| `src/utils/aiAnalysisApi.ts` | AI 분석 API 클라이언트 | Type-safe API calls |
| `src/store/authStore.ts` | 인증 상태 관리 | JWT 저장, 로그인/로그아웃 |
| `src/components/ai/ScoreCard.tsx` | 점수 표시 컴포넌트 | Circular/bar progress |

---

## 🚀 개발 워크플로우 / Development Workflow

### 1. 로컬 개발 환경 시작

```bash
# 1. Clone repository
git clone https://github.com/yourorg/kbeauty-leap.git
cd kbeauty-leap

# 2. Start backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Edit with your keys
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload

# 3. Start frontend (new terminal)
cd frontend
npm install
cp .env.example .env.local  # Edit if needed
npm run dev

# 4. Start Redis (new terminal)
docker run -d -p 6379:6379 redis:7-alpine

# 5. Start PostgreSQL (new terminal)
docker run -d -p 5432:5432 \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=kbeauty_db \
  postgres:13
```

### 2. 새로운 기능 개발

```bash
# 1. Create feature branch
git checkout -b feature/new-analysis-type

# 2. Backend: Add new endpoint
# Edit: backend/app/api/endpoints/ai_analysis.py

# 3. Backend: Add service logic
# Edit: backend/app/services/ai_analyzer_extended.py

# 4. Frontend: Add API client method
# Edit: frontend/src/utils/aiAnalysisApi.ts

# 5. Frontend: Create UI page
# Create: frontend/src/app/analysis/new-type/page.tsx

# 6. Test locally
# Run tests, verify functionality

# 7. Commit and push
git add .
git commit -m "feat: Add new analysis type"
git push origin feature/new-analysis-type

# 8. Create Pull Request
# Open PR on GitHub
```

### 3. 데이터베이스 마이그레이션

```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Add new_column to users"

# Review generated migration
cat alembic/versions/XXXX_add_new_column_to_users.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

---

## 📊 성능 모니터링 / Performance Monitoring

### Key Metrics to Track

1. **API Response Time**
   - Target: < 200ms for cached requests
   - Target: < 2s for AI analysis requests

2. **Cache Hit Rate**
   - Target: > 70% for cost optimization
   - Monitor via Redis INFO command

3. **Database Query Time**
   - Target: < 50ms for simple queries
   - Use `EXPLAIN ANALYZE` for optimization

4. **AI API Costs**
   - Track tokens used per analysis
   - Daily cost monitoring

5. **Instagram API Rate Limit**
   - Current usage: X / 200 calls per hour
   - Alert when < 20% remaining

---

## 🔒 보안 체크리스트 / Security Checklist

- ✅ Passwords hashed with bcrypt
- ✅ JWT tokens with expiration
- ✅ SQL injection prevented (ORM parameterized queries)
- ✅ CORS properly configured
- ✅ Environment variables for secrets
- ✅ HTTPS enforced in production
- ✅ Rate limiting enabled
- ✅ Input validation with Pydantic
- ✅ Instagram tokens encrypted in database
- ✅ No sensitive data in logs

---

## 📚 참고 자료 / Additional Resources

### Documentation
- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Next.js App Router Docs](https://nextjs.org/docs)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

### Related Documents
- `docs/AI_ANALYSIS_SYSTEM.md` - Detailed AI system architecture
- `docs/INSTAGRAM_API_INTEGRATION.md` - Instagram integration guide
- `README.md` - Project setup and quick start

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-10-28  
**Maintained By**: Development Team

---

## 📝 변경 이력 / Change Log

### v0.1.0 (2024-10-28)
- ✅ Initial documentation created
- ✅ All major features documented
- ✅ Code examples added with Korean/English comments
- ✅ Architecture diagrams included
- ✅ Development workflow documented
