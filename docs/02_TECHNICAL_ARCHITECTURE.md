# K-Beauty Global Leap - 기술 아키텍처 문서

## 📐 시스템 아키텍처 개요 / System Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js 14 (App Router) + TypeScript + Tailwind CSS    │   │
│  │  - Zustand (State Management)                            │   │
│  │  - React Query (Data Fetching)                           │   │
│  │  - Chart.js (Data Visualization)                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕ HTTPS/JSON
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  FastAPI (Python 3.11+)                                  │   │
│  │  - JWT Authentication                                    │   │
│  │  - Rate Limiting (slowapi)                               │   │
│  │  - CORS Middleware                                       │   │
│  │  - OpenAPI/Swagger Documentation                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                     SERVICE LAYER                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ AI Analysis  │  │  Instagram   │  │   Market     │          │
│  │   Service    │  │  API Client  │  │  Intelligence│          │
│  │              │  │              │  │   Service    │          │
│  │ - GPT-4      │  │ - OAuth 2.0  │  │ - Trends     │          │
│  │ - Claude     │  │ - Rate Limit │  │ - Insights   │          │
│  │ - Sentiment  │  │ - Media Fetch│  │ - Reports    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                    DATA/CACHE LAYER                              │
│  ┌──────────────┐                    ┌──────────────┐           │
│  │ PostgreSQL   │                    │    Redis     │           │
│  │   13+        │                    │   Cache      │           │
│  │              │                    │              │           │
│  │ - User Data  │                    │ - AI Results │           │
│  │ - Posts      │                    │ - Sessions   │           │
│  │ - Analytics  │                    │ - Rate Limits│           │
│  └──────────────┘                    └──────────────┘           │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  BACKGROUND JOBS LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Celery + Celery Beat (Redis Broker)                    │   │
│  │  - Scheduled Instagram Data Collection                   │   │
│  │  - Batch AI Analysis                                     │   │
│  │  - Report Generation                                     │   │
│  │  - Token Refresh                                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ Instagram  │  │  OpenAI    │  │ Anthropic  │                │
│  │ Graph API  │  │  GPT-4     │  │  Claude    │                │
│  │  v18.0     │  │            │  │            │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
User Request
    │
    ↓
┌─────────────────┐
│  Frontend UI    │
│  (Next.js)      │
└─────────────────┘
    │
    ↓ API Call (JWT)
┌─────────────────┐
│  FastAPI        │
│  Endpoint       │
└─────────────────┘
    │
    ↓
┌─────────────────┐      ┌─────────────────┐
│ Check Redis     │─────→│  Cache Hit?     │
│ Cache           │      │  Return Result  │
└─────────────────┘      └─────────────────┘
    │ Cache Miss
    ↓
┌─────────────────┐
│ Call Service    │
│ Layer           │
└─────────────────┘
    │
    ↓
┌─────────────────┐      ┌─────────────────┐
│ Instagram API   │      │  AI Service     │
│ or Database     │      │  (GPT-4/Claude) │
└─────────────────┘      └─────────────────┘
    │                            │
    └────────┬───────────────────┘
             ↓
    ┌─────────────────┐
    │  Process Data   │
    │  & Store Cache  │
    └─────────────────┘
             │
             ↓
    ┌─────────────────┐
    │ Save to         │
    │ PostgreSQL      │
    └─────────────────┘
             │
             ↓
    ┌─────────────────┐
    │ Return Response │
    │ to Frontend     │
    └─────────────────┘
```

---

## 🛠️ 기술 스택 상세 / Technology Stack Details

### Frontend Stack

| Technology | Version | Purpose | Selection Rationale |
|-----------|---------|---------|---------------------|
| **Next.js** | 14.x (App Router) | React Framework | - Server-side rendering for SEO<br>- App Router for modern patterns<br>- Built-in API routes<br>- Excellent TypeScript support |
| **TypeScript** | 5.x | Type Safety | - Catch errors at compile time<br>- Better IDE support<br>- Self-documenting code<br>- Refactoring confidence |
| **Tailwind CSS** | 3.x | Styling | - Rapid UI development<br>- Consistent design system<br>- Small bundle size<br>- Responsive utilities |
| **Zustand** | 4.x | State Management | - Simple API vs Redux<br>- No boilerplate<br>- TypeScript-friendly<br>- Persist middleware built-in |
| **Chart.js** | 4.x | Data Visualization | - Beautiful charts out-of-box<br>- Responsive design<br>- Animation support<br>- Wide chart type support |
| **Axios** | 1.x | HTTP Client | - Interceptor support<br>- Request/response transformation<br>- Better error handling than fetch<br>- TypeScript types included |

### Backend Stack

| Technology | Version | Purpose | Selection Rationale |
|-----------|---------|---------|---------------------|
| **FastAPI** | 0.104+ | API Framework | - Async/await native support<br>- Auto OpenAPI documentation<br>- Best Python performance<br>- Pydantic validation built-in |
| **Python** | 3.11+ | Language | - Latest performance improvements<br>- Excellent AI/ML libraries<br>- Rich ecosystem<br>- Type hints support |
| **SQLAlchemy** | 2.x | ORM | - Industry standard Python ORM<br>- Async support (2.0+)<br>- Complex query builder<br>- Database agnostic |
| **Alembic** | 1.x | Migrations | - Official SQLAlchemy migrations<br>- Version control for schema<br>- Auto-generate from models<br>- Rollback support |
| **Pydantic** | 2.x | Validation | - Data validation at runtime<br>- Built into FastAPI<br>- Excellent error messages<br>- JSON schema generation |

### Database & Caching

| Technology | Version | Purpose | Selection Rationale |
|-----------|---------|---------|---------------------|
| **PostgreSQL** | 13+ | Primary Database | - ACID compliance<br>- JSON/JSONB support<br>- Full-text search<br>- Mature and reliable |
| **Redis** | 7.x | Cache & Session | - In-memory speed<br>- TTL support<br>- Pub/Sub for real-time<br>- Simple data structures |

### AI & External Services

| Service | Purpose | Selection Rationale |
|---------|---------|---------------------|
| **OpenAI GPT-4** | Sentiment Analysis, Content Evaluation | - Best-in-class language understanding<br>- Reliable API<br>- JSON mode for structured output |
| **Anthropic Claude** | Backup AI, Cultural Analysis | - Strong reasoning capabilities<br>- Longer context window<br>- Alternative when GPT-4 unavailable |
| **Instagram Graph API** | Social Data Collection | - Official Instagram API<br>- OAuth 2.0 security<br>- Media insights access |

### Background Jobs

| Technology | Version | Purpose | Selection Rationale |
|-----------|---------|---------|---------------------|
| **Celery** | 5.x | Task Queue | - Distributed task execution<br>- Retry mechanisms<br>- Python ecosystem standard<br>- Monitoring tools available |
| **Celery Beat** | 2.x | Scheduler | - Cron-like scheduling<br>- Dynamic schedule updates<br>- Built for Celery integration |
| **Redis** | 7.x | Message Broker | - Fast message passing<br>- Simple setup<br>- Used already for cache |

### Development & DevOps

| Technology | Purpose | Selection Rationale |
|-----------|---------|---------------------|
| **Docker** | Containerization | - Consistent environments<br>- Easy deployment<br>- Service isolation |
| **Docker Compose** | Local Development | - Multi-container orchestration<br>- Simple configuration<br>- Development parity |
| **pytest** | Testing | - Python standard<br>- Fixtures system<br>- Plugin ecosystem |
| **Jest** | Frontend Testing | - React ecosystem standard<br>- Snapshot testing<br>- Fast execution |

---

## 🗄️ 데이터베이스 스키마 / Database Schema

### Entity Relationship Diagram

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (PK)             │
│ email (UNIQUE)      │
│ hashed_password     │
│ full_name           │
│ company_id (FK)     │◄─────┐
│ instagram_user_id   │      │
│ instagram_token     │      │
│ instagram_token_exp │      │
│ is_active           │      │
│ is_superuser        │      │
│ created_at          │      │
│ updated_at          │      │
└─────────────────────┘      │
                              │
┌─────────────────────────────┼───────────────────────────────┐
│                             │                               │
│  ┌─────────────────────┐   │   ┌─────────────────────┐     │
│  │     companies       │   │   │  instagram_posts    │     │
│  ├─────────────────────┤   │   ├─────────────────────┤     │
│  │ id (PK)             │───┘   │ id (PK)             │     │
│  │ name                │       │ post_id (UNIQUE)    │     │
│  │ industry            │       │ user_id (FK)        │─────┤
│  │ target_markets      │       │ caption             │     │
│  │ subscription_tier   │       │ media_type          │     │
│  │ is_active           │       │ media_url           │     │
│  │ created_at          │       │ permalink           │     │
│  │ updated_at          │       │ timestamp           │     │
│  └─────────────────────┘       │ like_count          │     │
│                                │ comment_count       │     │
│                                │ engagement_rate     │     │
│                                │ hashtags            │     │
│                                │ raw_data            │     │
│                                │ collected_at        │     │
│                                └─────────────────────┘     │
│                                                             │
│  ┌─────────────────────┐       ┌─────────────────────┐     │
│  │ instagram_hashtags  │       │instagram_influencers│     │
│  ├─────────────────────┤       ├─────────────────────┤     │
│  │ id (PK)             │       │ id (PK)             │     │
│  │ hashtag (UNIQUE)    │       │ username (UNIQUE)   │     │
│  │ post_count          │       │ instagram_user_id   │     │
│  │ market              │       │ follower_count      │     │
│  │ trending_score      │       │ avg_engagement      │     │
│  │ last_updated        │       │ market              │     │
│  │ created_at          │       │ category            │     │
│  └─────────────────────┘       │ authenticity_score  │     │
│                                │ verified            │     │
│                                │ bio                 │     │
│                                │ raw_data            │     │
│                                │ last_updated        │     │
│                                │ created_at          │     │
│                                └─────────────────────┘     │
│                                                             │
│  ┌─────────────────────────────────────────────────┐       │
│  │           ai_analysis_results                   │       │
│  ├─────────────────────────────────────────────────┤       │
│  │ id (PK)                                         │       │
│  │ user_id (FK)                                    │───────┘
│  │ analysis_type (sentiment/trend/quality/etc.)    │
│  │ input_data (JSONB)                              │
│  │ result_data (JSONB)                             │
│  │ model_used (gpt-4/claude)                       │
│  │ tokens_used                                     │
│  │ cost_usd                                        │
│  │ created_at                                      │
│  └─────────────────────────────────────────────────┘
```

### Table Definitions

#### 1. **users** Table

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company_id INTEGER REFERENCES companies(id),
    
    -- Instagram OAuth Fields
    instagram_user_id VARCHAR(255) UNIQUE,
    instagram_access_token TEXT,
    instagram_token_expires_at TIMESTAMP,
    
    -- Status Fields
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_company ON users(company_id);
CREATE INDEX idx_users_instagram ON users(instagram_user_id);
```

**Purpose**: Store user accounts with Instagram OAuth integration

#### 2. **companies** Table

```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    industry VARCHAR(100),
    target_markets JSONB,  -- ["DE", "FR", "JP"]
    
    -- Subscription
    subscription_tier VARCHAR(50) DEFAULT 'free',
    subscription_expires_at TIMESTAMP,
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_companies_industry ON companies(industry);
```

**Purpose**: Store company/organization data for B2B features

#### 3. **instagram_posts** Table

```sql
CREATE TABLE instagram_posts (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    
    -- Content
    caption TEXT,
    media_type VARCHAR(50),  -- IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url TEXT,
    permalink TEXT,
    
    -- Metrics
    timestamp TIMESTAMP,
    like_count INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    engagement_rate FLOAT,
    
    -- Analysis
    hashtags TEXT[],
    raw_data JSONB,  -- Store full API response
    
    -- Timestamps
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_posts_user ON instagram_posts(user_id);
CREATE INDEX idx_posts_timestamp ON instagram_posts(timestamp DESC);
CREATE INDEX idx_posts_hashtags ON instagram_posts USING GIN(hashtags);
```

**Purpose**: Cache Instagram post data to reduce API calls

#### 4. **instagram_hashtags** Table

```sql
CREATE TABLE instagram_hashtags (
    id SERIAL PRIMARY KEY,
    hashtag VARCHAR(255) UNIQUE NOT NULL,
    post_count INTEGER DEFAULT 0,
    market VARCHAR(10),  -- DE, FR, JP, etc.
    trending_score FLOAT,
    
    -- Timestamps
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_hashtags_market ON instagram_hashtags(market);
CREATE INDEX idx_hashtags_trending ON instagram_hashtags(trending_score DESC);
```

**Purpose**: Track trending hashtags per market

#### 5. **instagram_influencers** Table

```sql
CREATE TABLE instagram_influencers (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    instagram_user_id VARCHAR(255) UNIQUE,
    
    -- Metrics
    follower_count INTEGER,
    avg_engagement_rate FLOAT,
    
    -- Classification
    market VARCHAR(10),
    category VARCHAR(100),  -- beauty, fashion, lifestyle
    authenticity_score FLOAT,  -- 0-100
    verified BOOLEAN DEFAULT FALSE,
    
    -- Profile
    bio TEXT,
    raw_data JSONB,
    
    -- Timestamps
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_influencers_market ON instagram_influencers(market);
CREATE INDEX idx_influencers_authenticity ON instagram_influencers(authenticity_score DESC);
```

**Purpose**: Track verified influencers for partnership opportunities

#### 6. **ai_analysis_results** Table

```sql
CREATE TABLE ai_analysis_results (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    
    -- Analysis Details
    analysis_type VARCHAR(50) NOT NULL,  -- sentiment, trend, quality, authenticity, cultural_fit, performance
    input_data JSONB NOT NULL,           -- Original request data
    result_data JSONB NOT NULL,          -- Analysis results
    
    -- AI Model Tracking
    model_used VARCHAR(50),              -- gpt-4, claude-3-opus
    tokens_used INTEGER,
    cost_usd DECIMAL(10, 4),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_analysis_user ON ai_analysis_results(user_id);
CREATE INDEX idx_analysis_type ON ai_analysis_results(analysis_type);
CREATE INDEX idx_analysis_created ON ai_analysis_results(created_at DESC);
```

**Purpose**: Log all AI analysis requests for auditing and cost tracking

---

## 🔌 API 엔드포인트 목록 / API Endpoints

### Base URL
```
Development: http://localhost:8000/api/v1
Production: https://api.kbeauty-leap.com/api/v1
```

### Authentication Endpoints

#### 1. User Registration
```http
POST /auth/register
Content-Type: application/json

Request:
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "Jane Doe",
  "company_name": "Beauty Corp"
}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "created_at": "2024-10-28T12:00:00Z"
}
```

#### 2. User Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

Request:
username=user@example.com&password=securepassword

Response: 200 OK
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### 3. Get Current User
```http
GET /auth/me
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "Jane Doe",
  "company_id": 1,
  "instagram_connected": true,
  "subscription_tier": "pro"
}
```

### Instagram Integration Endpoints

#### 4. Instagram OAuth URL
```http
GET /instagram/auth-url?redirect_uri=http://localhost:3000/callback

Response: 200 OK
{
  "auth_url": "https://api.instagram.com/oauth/authorize?client_id=...&redirect_uri=...&scope=user_profile,user_media&response_type=code"
}
```

#### 5. Instagram OAuth Callback
```http
POST /instagram/callback
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "code": "AQD...",
  "redirect_uri": "http://localhost:3000/callback"
}

Response: 200 OK
{
  "instagram_user_id": "17841405793187218",
  "access_token_expires_at": "2024-12-28T12:00:00Z",
  "username": "beautyuser123"
}
```

#### 6. Get Instagram Profile
```http
GET /instagram/profile
Authorization: Bearer {access_token}

Response: 200 OK
{
  "id": "17841405793187218",
  "username": "beautyuser123",
  "account_type": "BUSINESS",
  "media_count": 150,
  "followers_count": 5000,
  "follows_count": 300
}
```

#### 7. Get Instagram Media
```http
GET /instagram/media?limit=25&fields=id,caption,media_type,timestamp,like_count
Authorization: Bearer {access_token}

Response: 200 OK
{
  "data": [
    {
      "id": "17895695668004550",
      "caption": "New K-Beauty launch! #kbeauty #skincare",
      "media_type": "IMAGE",
      "timestamp": "2024-10-20T10:30:00+0000",
      "like_count": 150,
      "comments_count": 20,
      "engagement_rate": 3.4
    }
  ],
  "paging": {
    "next": "https://..."
  }
}
```

### AI Analysis Endpoints

#### 8. Sentiment Analysis
```http
POST /ai/sentiment
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "market": "DE",
  "hashtags": ["#kbeauty", "#skincare"],
  "sample_size": 50,
  "time_range": "7d"
}

Response: 200 OK
{
  "overall_sentiment": "positive",
  "sentiment_score": 78.5,
  "key_themes": ["glass skin", "hydration", "Korean routine"],
  "trending_topics": ["sheet masks", "serum layering"],
  "analysis_summary": "Strong positive sentiment...",
  "posts_analyzed": 50,
  "cached": false,
  "analyzed_at": "2024-10-28T12:00:00Z"
}
```

#### 9. Trend Analysis
```http
POST /ai/trends
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "market": "FR",
  "category": "skincare",
  "time_horizon": "30d"
}

Response: 200 OK
{
  "trending_products": [
    {
      "name": "Snail Mucin Essence",
      "trend_score": 92,
      "growth_rate": 45.2
    }
  ],
  "emerging_hashtags": ["#escargotbeauty", "#bave"],
  "predicted_peaks": ["2024-11-15", "2024-12-20"],
  "recommendations": ["Launch campaign before Black Friday..."],
  "confidence_score": 85
}
```

#### 10. Content Quality Evaluation
```http
POST /ai/quality
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "post_url": "https://instagram.com/p/ABC123",
  "detailed": true
}

Response: 200 OK
{
  "overall_score": 82,
  "visual_quality": 88,
  "caption_effectiveness": 75,
  "hashtag_relevance": 80,
  "improvements": [
    "Add call-to-action",
    "Use more specific hashtags"
  ],
  "estimated_reach": "5000-8000"
}
```

#### 11. Influencer Authenticity Check
```http
POST /ai/authenticity
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "username": "beautyinfluencer123",
  "check_followers": true
}

Response: 200 OK
{
  "authenticity_score": 87,
  "follower_quality": 92,
  "engagement_consistency": 85,
  "bot_percentage": 3.5,
  "red_flags": [],
  "recommendation": "Safe to collaborate",
  "verified_status": true
}
```

#### 12. Cultural Fit Analysis
```http
POST /ai/cultural-fit
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "content": "New whitening cream for perfect skin!",
  "target_market": "DE"
}

Response: 200 OK
{
  "cultural_fit_score": 35,
  "sensitivity_issues": [
    "'Whitening' term problematic in German market",
    "Suggest 'brightening' or 'even tone' instead"
  ],
  "localization_tips": [
    "Emphasize natural ingredients",
    "Focus on skin health vs. color change"
  ],
  "revised_content": "New brightening serum for radiant, healthy skin!",
  "approval_status": "needs_revision"
}
```

#### 13. Performance Prediction
```http
POST /ai/predict-performance
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "post_draft": {
    "caption": "Introducing our new serum! #kbeauty #skincare",
    "media_type": "IMAGE",
    "hashtags": ["#kbeauty", "#skincare"],
    "posting_time": "2024-11-01T18:00:00Z"
  },
  "market": "JP"
}

Response: 200 OK
{
  "predicted_likes": 850,
  "predicted_comments": 45,
  "predicted_engagement_rate": 4.2,
  "confidence_interval": [750, 950],
  "optimization_tips": [
    "Post at 19:00 JST for better reach",
    "Add #美容 hashtag for Japanese audience"
  ],
  "predicted_reach": 25000
}
```

#### 14. Market Entry Recommendation
```http
GET /ai/market-entry/DE
Authorization: Bearer {access_token}

Response: 200 OK
{
  "market": "DE",
  "entry_readiness_score": 78,
  "competitive_landscape": {
    "intensity": "high",
    "top_players": ["Brand A", "Brand B"]
  },
  "target_demographics": {
    "age_range": "25-40",
    "interests": ["natural skincare", "sustainability"]
  },
  "recommended_channels": [
    {
      "platform": "Instagram",
      "priority": "high",
      "influencer_count": 1250
    }
  ],
  "estimated_budget": {
    "min": 5000,
    "max": 15000,
    "currency": "EUR"
  },
  "timeline": "3-6 months",
  "key_success_factors": [
    "Sustainability messaging",
    "Clinical test results",
    "German language content"
  ]
}
```

#### 15. Batch Analysis
```http
POST /ai/batch-analyze
Authorization: Bearer {access_token}
Content-Type: application/json

Request:
{
  "analysis_types": ["sentiment", "quality"],
  "posts": [
    {"url": "https://instagram.com/p/ABC123"},
    {"url": "https://instagram.com/p/DEF456"}
  ],
  "market": "FR"
}

Response: 200 OK
{
  "results": [
    {
      "post_url": "https://instagram.com/p/ABC123",
      "sentiment": {...},
      "quality": {...}
    }
  ],
  "summary": {
    "total_posts": 2,
    "avg_sentiment_score": 75,
    "avg_quality_score": 80
  },
  "processing_time": 12.5
}
```

### Data Collection Endpoints

#### 16. Search Hashtag Posts
```http
GET /data/hashtag/kbeauty?market=DE&limit=50
Authorization: Bearer {access_token}

Response: 200 OK
{
  "hashtag": "kbeauty",
  "market": "DE",
  "posts_found": 50,
  "posts": [...],
  "trending_score": 85,
  "last_updated": "2024-10-28T12:00:00Z"
}
```

#### 17. Get Market Insights
```http
GET /data/market-insights/JP?category=skincare
Authorization: Bearer {access_token}

Response: 200 OK
{
  "market": "JP",
  "category": "skincare",
  "total_posts": 15000,
  "avg_engagement": 3.8,
  "top_hashtags": ["#美容", "#スキンケア"],
  "top_influencers": [...],
  "market_size_score": 92
}
```

### Admin Endpoints

#### 18. Get System Stats
```http
GET /admin/stats
Authorization: Bearer {admin_access_token}

Response: 200 OK
{
  "total_users": 150,
  "active_users_30d": 120,
  "total_analyses": 5000,
  "ai_cost_total": 350.50,
  "cache_hit_rate": 72.5,
  "instagram_api_calls": 1500,
  "api_rate_limit_remaining": 185
}
```

---

## 🔐 인증 및 보안 / Authentication & Security

### JWT Authentication
- **Token Type**: Bearer Token
- **Algorithm**: HS256
- **Expiration**: 1 hour (access token)
- **Refresh**: Not implemented in MVP (manual re-login)

### API Rate Limiting
```python
# Per User Limits
- Free Tier: 100 requests/day
- Basic Tier: 1,000 requests/day
- Pro Tier: 10,000 requests/day
- Enterprise: Custom limits

# Global Limits
- 1000 requests/minute per IP
```

### Instagram API Rate Limiting
- **Rate Limit**: 200 calls per hour per user
- **Strategy**: Queue-based with retry logic
- **Monitoring**: Real-time tracking of remaining calls

### Security Best Practices
1. **Password Hashing**: bcrypt with salt
2. **SQL Injection Prevention**: SQLAlchemy ORM parameterized queries
3. **CORS**: Configured whitelist for frontend domain
4. **HTTPS Only**: Enforced in production
5. **Sensitive Data**: Environment variables (never in code)
6. **Token Storage**: Encrypted in database

---

## 📊 성능 최적화 / Performance Optimization

### Caching Strategy

| Data Type | Cache Location | TTL | Rationale |
|-----------|---------------|-----|-----------|
| Sentiment Analysis | Redis | 24 hours | Market sentiment changes slowly |
| Content Quality | Redis | 24 hours | Post quality is stable |
| Influencer Auth | Redis | 7 days | Follower metrics change weekly |
| Cultural Fit | Redis | 7 days | Cultural rules are stable |
| Instagram Posts | PostgreSQL | 30 days | Reduce API calls |
| Hashtag Trends | Redis | 1 hour | Trends update frequently |

### Database Optimization
- **Indexes**: Created on frequently queried columns
- **Connection Pooling**: Max 20 connections
- **Query Optimization**: Eager loading for relationships
- **JSONB**: For flexible schema (raw API responses)

### API Optimization
- **Async/Await**: All I/O operations are async
- **Batch Processing**: Group similar requests
- **Lazy Loading**: Load data only when needed
- **Pagination**: Default 25 items, max 100

---

## 🔄 배포 아키텍처 / Deployment Architecture

### Development Environment
```yaml
Frontend: Next.js dev server (localhost:3000)
Backend: FastAPI with uvicorn (localhost:8000)
Database: PostgreSQL in Docker (localhost:5432)
Cache: Redis in Docker (localhost:6379)
Background Jobs: Celery worker + beat
```

### Production Environment (Planned)
```yaml
Frontend: Vercel / Cloudflare Pages
Backend: AWS ECS / Google Cloud Run
Database: AWS RDS PostgreSQL / Google Cloud SQL
Cache: AWS ElastiCache Redis / Google Cloud Memorystore
Background Jobs: AWS ECS (Celery) / Google Cloud Tasks
CDN: Cloudflare
Monitoring: Datadog / New Relic
```

---

## 📈 확장성 고려사항 / Scalability Considerations

### Horizontal Scaling
- **Stateless API**: Each request is independent
- **Load Balancer**: NGINX / AWS ALB ready
- **Session Storage**: Redis (shared across instances)
- **Background Workers**: Can add more Celery workers

### Vertical Scaling
- **Database**: Read replicas for heavy read operations
- **Cache**: Redis cluster for larger datasets
- **API**: Increase worker count per instance

### Future Improvements
1. **Message Queue**: RabbitMQ for better job distribution
2. **Microservices**: Split into AI service, data service, API gateway
3. **CDN**: Static asset delivery via CDN
4. **GraphQL**: For flexible data fetching
5. **WebSockets**: Real-time analysis updates

---

## 🧪 테스트 전략 / Testing Strategy

### Backend Testing
```python
# Unit Tests
pytest tests/unit/  # 80%+ coverage target

# Integration Tests
pytest tests/integration/  # API endpoint tests

# Load Tests
locust -f tests/load/locustfile.py
```

### Frontend Testing
```bash
# Component Tests
npm run test  # Jest + React Testing Library

# E2E Tests
npm run test:e2e  # Playwright (planned)
```

---

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

**Document Version**: 1.0.0  
**Last Updated**: 2024-10-28  
**Maintained By**: Development Team
