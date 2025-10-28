# Instagram Graph API 연동 가이드

## 📋 개요

K-Beauty Global Leap 플랫폼은 Instagram Graph API를 사용하여 실시간 Instagram 데이터를 수집하고 분석합니다.

**API 버전**: Instagram Graph API v18.0  
**인증 방식**: OAuth 2.0  
**Rate Limiting**: 200 calls per hour (per user)

---

## 🏗️ 아키텍처

```
┌─────────────────────────────────────────────────────────────┐
│                    K-Beauty Platform                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────────┐      ┌────────────────────┐            │
│  │  InstagramAPI   │◄────►│ InstagramService   │            │
│  │  Client         │      │ (Business Logic)   │            │
│  └─────────────────┘      └────────────────────┘            │
│         │                           │                        │
│         │                           ▼                        │
│         │                  ┌────────────────┐               │
│         │                  │  PostgreSQL DB │               │
│         │                  └────────────────┘               │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│            Instagram Graph API (Facebook)                    │
├─────────────────────────────────────────────────────────────┤
│  • User Info                                                 │
│  • Media (Posts)                                             │
│  • Hashtag Search                                            │
│  • Insights                                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔐 OAuth 2.0 인증 플로우

### 1단계: 사용자 인증 요청

```
GET https://api.instagram.com/oauth/authorize
  ?client_id={app-id}
  &redirect_uri={redirect-uri}
  &scope=user_profile,user_media
  &response_type=code
```

### 2단계: 인증 코드 교환 (Access Token 획득)

```python
POST https://api.instagram.com/oauth/access_token
{
  "client_id": "{app-id}",
  "client_secret": "{app-secret}",
  "grant_type": "authorization_code",
  "redirect_uri": "{redirect-uri}",
  "code": "{code}"
}
```

### 3단계: 단기 토큰 → 장기 토큰 교환

```python
GET https://graph.instagram.com/access_token
  ?grant_type=ig_exchange_token
  &client_secret={app-secret}
  &access_token={short-lived-token}
```

**장기 토큰**: 60일 유효, 갱신 가능

---

## 🎯 지원 API 엔드포인트

### 1. 사용자 프로필 정보

```
GET /{user-id}?fields=id,username,account_type,media_count
```

**응답 예시**:
```json
{
  "id": "17841405309211844",
  "username": "k_beauty_insider",
  "account_type": "BUSINESS",
  "media_count": 324
}
```

### 2. 사용자 미디어 (Posts)

```
GET /{user-id}/media?fields=id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count
```

**응답 예시**:
```json
{
  "data": [
    {
      "id": "17895695668004550",
      "caption": "New K-Beauty trend! #kbeauty #skincare",
      "media_type": "IMAGE",
      "media_url": "https://...",
      "permalink": "https://www.instagram.com/p/...",
      "timestamp": "2024-01-15T10:30:00+0000",
      "like_count": 1523,
      "comments_count": 87
    }
  ]
}
```

### 3. 해시태그 검색

```
GET /ig_hashtag_search?user_id={user-id}&q={hashtag}
```

### 4. 해시태그 관련 미디어

```
GET /{hashtag-id}/top_media?user_id={user-id}&fields=id,caption,media_url,like_count
```

### 5. Insights (비즈니스 계정 전용)

```
GET /{media-id}/insights?metric=engagement,impressions,reach,saved
```

---

## ⚙️ 환경 변수 설정

```env
# Instagram Graph API Configuration
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/v1/instagram/callback
INSTAGRAM_API_VERSION=v18.0

# Feature Flags
USE_REAL_INSTAGRAM_API=false  # MVP에서는 false (Mock 데이터 사용)
```

---

## 🚦 Rate Limiting 전략

Instagram Graph API는 **시간당 200 호출** 제한이 있습니다.

### 구현 전략

1. **요청 캐싱**
   - Redis를 사용하여 API 응답 캐싱 (TTL: 15분)
   - 동일 요청 중복 방지

2. **Rate Limiter 구현**
   ```python
   class RateLimiter:
       def __init__(self, max_calls=200, period=3600):
           self.max_calls = max_calls
           self.period = period
           self.calls = []
       
       def is_allowed(self):
           now = time.time()
           # Remove old calls
           self.calls = [call for call in self.calls if call > now - self.period]
           
           if len(self.calls) < self.max_calls:
               self.calls.append(now)
               return True
           return False
   ```

3. **배치 수집**
   - 스케줄러를 사용하여 주기적으로 데이터 수집
   - 실시간 요청 최소화

4. **우선순위 큐**
   - 중요한 요청 우선 처리
   - 사용자 요청 > 백그라운드 수집

---

## 🛡️ 에러 처리

### API 에러 코드

| 코드 | 설명 | 처리 방법 |
|------|------|-----------|
| 190 | Access token expired | 토큰 갱신 |
| 200 | Permission denied | 권한 재요청 |
| 4 | Rate limit exceeded | 대기 후 재시도 |
| 100 | Invalid parameter | 파라미터 검증 |

### 에러 처리 전략

```python
class InstagramAPIError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

async def handle_api_error(error):
    if error.code == 190:
        # Token expired - refresh token
        await refresh_access_token()
    elif error.code == 4:
        # Rate limit - wait and retry
        await asyncio.sleep(3600)
    elif error.code == 200:
        # Permission denied - fallback to mock data
        return await get_mock_data()
```

---

## 📊 데이터 수집 스케줄러

### Celery Beat 스케줄

```python
from celery import Celery
from celery.schedules import crontab

celery_app = Celery('k_beauty')

@celery_app.task
async def collect_trending_posts():
    """매 6시간마다 트렌딩 포스트 수집"""
    markets = ["germany", "france", "japan"]
    for market in markets:
        await instagram_service.collect_market_posts(market)

@celery_app.task
async def update_hashtag_trends():
    """매 12시간마다 해시태그 트렌드 업데이트"""
    hashtags = await get_tracked_hashtags()
    for hashtag in hashtags:
        await instagram_service.update_hashtag_metrics(hashtag)

# Celery Beat Schedule
celery_app.conf.beat_schedule = {
    'collect-posts-every-6-hours': {
        'task': 'collect_trending_posts',
        'schedule': crontab(hour='*/6'),
    },
    'update-hashtags-every-12-hours': {
        'task': 'update_hashtag_trends',
        'schedule': crontab(hour='*/12'),
    },
}
```

---

## 🔄 Mock 데이터 ↔ 실제 API 전환

### 설정 기반 전환

```python
# app/core/config.py
class Settings(BaseSettings):
    USE_REAL_INSTAGRAM_API: bool = False
    
    @property
    def instagram_data_source(self):
        return "real_api" if self.USE_REAL_INSTAGRAM_API else "mock_data"

# app/services/instagram_service.py
class InstagramService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        
        if self.settings.USE_REAL_INSTAGRAM_API:
            self.api_client = InstagramGraphAPI()
        else:
            self.api_client = None  # Use mock data
    
    async def search_posts(self, market: str, **kwargs):
        if self.api_client:
            # Fetch from real API
            return await self.api_client.search_posts(market, **kwargs)
        else:
            # Fetch from database (mock data)
            return await self._search_posts_from_db(market, **kwargs)
```

---

## 🧪 테스트 전략

### 1. Unit Tests (API Client)

```python
@pytest.mark.asyncio
async def test_instagram_api_get_user_profile():
    client = InstagramGraphAPI()
    user = await client.get_user_profile("test_user_id")
    assert user["username"] is not None
    assert user["media_count"] > 0
```

### 2. Integration Tests (Service Layer)

```python
@pytest.mark.asyncio
async def test_collect_posts_from_api():
    service = InstagramService(db)
    posts = await service.collect_market_posts("germany")
    assert len(posts) > 0
    assert posts[0].market == "germany"
```

### 3. Mock API Server (개발용)

```python
# tests/mock_instagram_api.py
from fastapi import FastAPI

mock_app = FastAPI()

@mock_app.get("/v18.0/{user_id}/media")
async def get_user_media(user_id: str):
    return {
        "data": [
            {
                "id": "123456789",
                "caption": "Test post",
                "like_count": 100
            }
        ]
    }
```

---

## 📈 모니터링 및 로깅

### 로깅 전략

```python
import logging

logger = logging.getLogger("instagram_api")

async def log_api_call(endpoint, params, response_time, status):
    logger.info(
        f"Instagram API Call",
        extra={
            "endpoint": endpoint,
            "params": params,
            "response_time_ms": response_time,
            "status": status,
            "rate_limit_remaining": response.headers.get("X-App-Usage")
        }
    )
```

### 메트릭 수집

- API 호출 횟수
- 응답 시간
- 에러율
- Rate limit 사용량
- 캐시 히트율

---

## 🚀 배포 전 체크리스트

- [ ] Instagram App 생성 및 승인
- [ ] OAuth 2.0 Redirect URI 설정
- [ ] 환경 변수 설정
- [ ] Rate limiter 테스트
- [ ] Error handling 테스트
- [ ] 토큰 갱신 로직 테스트
- [ ] 모니터링 대시보드 설정
- [ ] 백업 전략 수립 (API 장애 시 Mock 데이터 사용)

---

## 📚 참고 자료

- [Instagram Graph API 공식 문서](https://developers.facebook.com/docs/instagram-api)
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [Rate Limiting Best Practices](https://developers.facebook.com/docs/graph-api/overview/rate-limiting)
- [OAuth 2.0 Flow](https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow)

---

## 🎯 MVP vs Production

### MVP (현재)
- ✅ Mock 데이터 사용
- ✅ 150개 샘플 포스트
- ✅ 37개 해시태그
- ✅ 36명 인플루언서
- ✅ 3개 시장 (독일, 프랑스, 일본)

### Production (목표)
- 🔄 실시간 Instagram API 연동
- 🔄 자동 데이터 수집 스케줄러
- 🔄 Rate limiting 및 캐싱
- 🔄 토큰 관리 자동화
- 🔄 에러 복구 메커니즘
- 🔄 모니터링 및 알림

---

**작성일**: 2024-01-15  
**버전**: 1.0  
**작성자**: K-Beauty Global Leap Development Team
