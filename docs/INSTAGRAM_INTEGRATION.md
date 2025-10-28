# Instagram API 통합 가이드

> K-Beauty Global Leap - Instagram 데이터 수집 전략

**작성일**: 2025.10.28  
**담당**: (주)뷰티인사이드랩

---

## 🎯 목표

K-Beauty 브랜드의 글로벌 시장 트렌드 분석을 위해 Instagram 데이터를 수집하고 분석합니다.

### 수집 대상 데이터:
- 📸 **게시물**: 이미지, 캡션, 해시태그, 위치
- 📊 **메트릭**: 좋아요, 댓글, 저장, 공유 수
- 👥 **인플루언서**: 팔로워, 참여율, 게시 빈도
- 🏷️ **해시태그**: 트렌딩 해시태그, 사용 빈도
- 🌍 **지역**: 타겟 마켓별 트렌드 차이

---

## 📋 Instagram API 옵션 비교

### 1. Instagram Graph API (공식, 추천)

**장점**:
- ✅ 공식 Meta API, 안정적이고 합법적
- ✅ 비즈니스 계정 인사이트 접근 가능
- ✅ 높은 Rate Limit (200 calls/hour/user)
- ✅ 공개 해시태그 검색 가능
- ✅ 사용자 멘션, 태그된 미디어 접근

**단점**:
- ❌ Facebook Business Manager 계정 필요
- ❌ 앱 리뷰 프로세스 필요 (시간 소요)
- ❌ 비즈니스 계정만 연동 가능

**사용 가능한 엔드포인트**:
```
GET /{ig-user-id}/media                    # 게시물 목록
GET /{ig-media-id}                          # 게시물 상세
GET /{ig-user-id}/insights                  # 인사이트
GET /ig_hashtag_search?q={hashtag}          # 해시태그 검색
GET /{ig-hashtag-id}/recent_media           # 해시태그 최근 게시물
```

**필요한 권한**:
- `instagram_basic`
- `instagram_manage_insights`
- `pages_read_engagement`

---

### 2. Instagram Basic Display API

**장점**:
- ✅ 개인 계정 사용 가능
- ✅ 빠른 설정 (앱 리뷰 불필요)
- ✅ 기본 미디어 데이터 접근

**단점**:
- ❌ 인사이트 데이터 없음 (좋아요, 댓글 수 제한적)
- ❌ 해시태그 검색 불가능
- ❌ 공개 데이터만 접근
- ❌ Rate Limit 낮음

**사용 케이스**:
- 개발 초기 프로토타입
- 자사 계정 데이터만 필요한 경우

---

### 3. 서드파티 API 서비스

**추천 서비스**:

#### Apify Instagram Scraper
- 💰 **가격**: $49/월 (10,000 results)
- ✅ 해시태그, 위치, 사용자 기반 검색
- ✅ 상세한 메트릭 데이터
- ✅ Rate Limit 관리 자동화
- ✅ 빠른 구현 가능

#### RapidAPI - Instagram API
- 💰 **가격**: $0-200/월 (사용량 기반)
- ✅ 공개 프로필, 게시물, 해시태그
- ✅ REST API 형식
- ✅ 문서화 잘됨

#### Phantombuster
- 💰 **가격**: $56/월
- ✅ 자동화된 스크래핑
- ✅ CSV 내보내기
- ❌ API 형식 아님 (수동 다운로드)

---

## 🚀 구현 전략 (단계적 접근)

### Phase 1: MVP (Week 1) - Mock 데이터
**목표**: 데모 가능한 프로토타입

```
✅ Mock 데이터 생성 (JSON fixtures)
✅ 데이터베이스 모델 설계
✅ API 엔드포인트 구현
✅ 프론트엔드 UI 연동
```

**장점**:
- 즉시 개발 시작 가능
- Instagram API 승인 대기 불필요
- 데이터 구조 검증 가능

---

### Phase 2: Pilot (Week 2-4) - 실제 데이터

**옵션 A: Instagram Graph API (공식, 추천)**
```
1. Facebook Developer 계정 생성
2. 앱 생성 및 Instagram Graph API 추가
3. 테스트 사용자 추가
4. Access Token 발급
5. 앱 리뷰 제출 (인스타그램 권한)
```

**옵션 B: 서드파티 API (빠른 구현)**
```
1. Apify 계정 생성
2. Instagram Scraper Actor 사용
3. API 키 발급
4. 백엔드 통합
```

---

### Phase 3: SaaS (Week 5+) - 프로덕션

**하이브리드 접근**:
- 💼 **고객 비즈니스 계정**: Instagram Graph API (공식)
- 📊 **시장 트렌드 데이터**: Apify (서드파티)
- 🔍 **해시태그 분석**: 자체 크롤링 (제한적)

---

## 📊 데이터베이스 스키마

### InstagramPost (게시물)
```python
class InstagramPost(Base):
    __tablename__ = "instagram_posts"
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)  # Instagram post ID
    
    # Content
    caption = Column(Text, nullable=True)
    media_type = Column(String)  # IMAGE, VIDEO, CAROUSEL_ALBUM
    media_url = Column(String, nullable=True)
    permalink = Column(String, nullable=True)
    
    # Metadata
    username = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    location = Column(String, nullable=True)
    
    # Metrics
    like_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    save_count = Column(Integer, nullable=True)
    reach = Column(Integer, nullable=True)
    impressions = Column(Integer, nullable=True)
    
    # Analysis
    hashtags = Column(JSON, default=list)  # ["kbeauty", "skincare"]
    mentions = Column(JSON, default=list)  # ["@brand"]
    market = Column(String, index=True)  # "germany", "france"
    
    # Relationships
    analysis_id = Column(Integer, ForeignKey("analyses.id"), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### InstagramHashtag (해시태그 트렌드)
```python
class InstagramHashtag(Base):
    __tablename__ = "instagram_hashtags"
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    
    name = Column(String, index=True)  # "kbeauty"
    market = Column(String, index=True)  # "germany"
    
    # Metrics
    post_count = Column(Integer, default=0)
    avg_engagement = Column(Float, default=0.0)
    growth_rate = Column(Float, default=0.0)  # % change week-over-week
    
    # Trending
    is_trending = Column(Boolean, default=False)
    trend_score = Column(Float, default=0.0)
    
    # Timestamps
    tracked_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### InstagramInfluencer (인플루언서)
```python
class InstagramInfluencer(Base):
    __tablename__ = "instagram_influencers"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    
    # Profile
    full_name = Column(String, nullable=True)
    biography = Column(Text, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    
    # Metrics
    followers_count = Column(Integer, default=0)
    following_count = Column(Integer, default=0)
    media_count = Column(Integer, default=0)
    
    # Engagement
    avg_likes = Column(Float, default=0.0)
    avg_comments = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)  # (likes + comments) / followers
    
    # Category
    category = Column(String, index=True)  # "beauty", "skincare", "makeup"
    market = Column(String, index=True)
    
    # Quality Score
    authenticity_score = Column(Float, default=0.0)  # AI-based fake follower detection
    brand_affinity_score = Column(Float, default=0.0)  # K-Beauty relevance
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## 🔧 백엔드 서비스 구조

### Instagram Service
```python
# backend/app/services/instagram_service.py

class InstagramService:
    """Instagram 데이터 수집 및 분석 서비스"""
    
    async def search_hashtag_posts(
        self, 
        hashtag: str, 
        market: str, 
        limit: int = 50
    ) -> List[InstagramPost]:
        """해시태그로 게시물 검색"""
        pass
    
    async def get_trending_hashtags(
        self, 
        market: str, 
        category: str = "kbeauty"
    ) -> List[InstagramHashtag]:
        """트렌딩 해시태그 분석"""
        pass
    
    async def find_influencers(
        self, 
        market: str, 
        min_followers: int = 10000,
        max_followers: int = 500000
    ) -> List[InstagramInfluencer]:
        """마이크로 인플루언서 발굴"""
        pass
    
    async def analyze_engagement(
        self, 
        posts: List[InstagramPost]
    ) -> Dict:
        """참여율 분석"""
        pass
```

---

## 📝 MVP 구현 계획 (Day 5-6)

### ✅ Day 5: 데이터 모델 및 Mock 데이터

**오전 (2-3시간)**:
1. ✅ Instagram 데이터 모델 생성 (Post, Hashtag, Influencer)
2. ✅ Alembic 마이그레이션 생성
3. ✅ 데이터베이스 마이그레이션 실행

**오후 (2-3시간)**:
4. ✅ Mock 데이터 생성 스크립트
   - 독일, 프랑스, 일본 시장별 K-Beauty 게시물
   - 트렌딩 해시태그 (50개)
   - 마이크로 인플루언서 (20명)

---

### ✅ Day 6: 서비스 및 API 구현

**오전 (2-3시간)**:
1. ✅ Instagram Service 구현
   - `search_posts()`: 해시태그/위치 기반 검색
   - `get_trending_hashtags()`: 트렌드 분석
   - `find_influencers()`: 인플루언서 발굴

**오후 (2-3시간)**:
2. ✅ API 엔드포인트 구현
   - `GET /api/v1/instagram/posts?hashtag=kbeauty&market=germany`
   - `GET /api/v1/instagram/hashtags/trending?market=germany`
   - `GET /api/v1/instagram/influencers?market=germany`

3. ✅ API 문서 업데이트 (FastAPI 자동 문서)

---

## 🧪 테스트 시나리오

### 1. 해시태그 트렌드 분석
```bash
# 독일 시장 #kbeauty 트렌드
GET /api/v1/instagram/posts?hashtag=kbeauty&market=germany&limit=50

# 예상 응답
{
  "total": 50,
  "market": "germany",
  "hashtag": "kbeauty",
  "posts": [
    {
      "external_id": "instagram_123",
      "caption": "My new K-Beauty routine! 🇰🇷✨ #kbeauty #skincare",
      "like_count": 1523,
      "comment_count": 87,
      "hashtags": ["kbeauty", "skincare", "koreanbeauty"],
      "timestamp": "2025-10-25T14:30:00Z"
    }
  ],
  "insights": {
    "avg_engagement": 4.2,
    "top_hashtags": ["kbeauty", "skincare", "glowingskin"],
    "peak_posting_time": "18:00-21:00"
  }
}
```

### 2. 인플루언서 발굴
```bash
GET /api/v1/instagram/influencers?market=germany&min_followers=10000&max_followers=100000

# 예상 응답
{
  "total": 15,
  "influencers": [
    {
      "username": "beautyblogger_de",
      "followers_count": 45000,
      "engagement_rate": 5.8,
      "authenticity_score": 92,
      "category": "beauty"
    }
  ]
}
```

---

## 🔐 보안 고려사항

### Rate Limiting
- Instagram API: 200 calls/hour (공식)
- 자체 API: 100 calls/hour/user (Redis 기반)

### 데이터 저장
- 개인정보 최소 수집 (GDPR 준수)
- 공개 데이터만 저장
- 사용자 동의 필요 시 명시

### API 키 관리
- 환경 변수로 관리
- 프론트엔드 노출 금지
- 정기적 갱신

---

## 📈 성능 최적화

### 캐싱 전략
```python
# Redis 캐싱
# 해시태그 트렌드: 1시간
# 게시물 데이터: 6시간
# 인플루언서 프로필: 24시간
```

### 배치 처리
```python
# Celery 비동기 작업
# 1. 트렌드 해시태그 업데이트 (매 6시간)
# 2. 인플루언서 메트릭 업데이트 (매일)
# 3. 게시물 수집 (사용자 요청 시)
```

---

## 🎯 다음 단계 (Week 2+)

### Instagram Graph API 연동
1. Facebook Developer 계정 생성
2. 앱 생성 및 설정
3. Test Users 추가
4. 앱 리뷰 제출
5. Production 토큰 발급

### 고급 분석 기능
1. AI 기반 이미지 분석 (제품 인식)
2. 감성 분석 (댓글, 캡션)
3. 트렌드 예측 (시계열 분석)
4. 경쟁사 벤치마킹

---

## 📚 참고 자료

- [Instagram Graph API 문서](https://developers.facebook.com/docs/instagram-api)
- [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api)
- [Apify Instagram Scraper](https://apify.com/apify/instagram-scraper)
- [GDPR 가이드](https://gdpr.eu/)

---

**작성자**: (주)뷰티인사이드랩  
**버전**: 1.0  
**최종 업데이트**: 2025.10.28
