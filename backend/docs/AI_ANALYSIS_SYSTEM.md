# AI 분석 시스템 아키텍처

## 📋 개요

K-Beauty Global Leap의 AI 분석 시스템은 GPT-4와 Claude를 활용하여 Instagram 콘텐츠, 트렌드, 인플루언서를 분석하고 K-Beauty 기업에게 실행 가능한 인사이트를 제공합니다.

**핵심 AI 엔진**: OpenAI GPT-4, Anthropic Claude 3  
**분석 도메인**: 감성 분석, 트렌드 예측, 콘텐츠 품질, 문화적 적합성

---

## 🏗️ 시스템 아키텍처

```
┌─────────────────────────────────────────────────────────────────┐
│                    K-Beauty Platform                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐      ┌─────────────────────┐             │
│  │  AI Analyzer     │◄────►│  Analysis Service   │             │
│  │  (GPT-4/Claude)  │      │  (Business Logic)   │             │
│  └──────────────────┘      └─────────────────────┘             │
│         │                            │                           │
│         │                            ▼                           │
│         │                   ┌──────────────────┐                │
│         │                   │  Analysis Model  │                │
│         │                   │   (PostgreSQL)   │                │
│         │                   └──────────────────┘                │
│         │                                                        │
│         ▼                                                        │
│  ┌──────────────────┐                                           │
│  │  Redis Cache     │  (Analysis Results Cache)                │
│  └──────────────────┘                                           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   External AI APIs                               │
├─────────────────────────────────────────────────────────────────┤
│  • OpenAI GPT-4 (Content Analysis, Sentiment)                   │
│  • Anthropic Claude 3 (Cultural Analysis, Reasoning)            │
│  • Hugging Face (Custom NLP Models)                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 AI 분석 기능

### 1. 감성 분석 (Sentiment Analysis)

**목적**: Instagram 포스트와 댓글의 감성을 분석하여 브랜드 반응 파악

**분석 항목**:
- **Overall Sentiment**: Positive (0.7-1.0), Neutral (0.3-0.7), Negative (0.0-0.3)
- **Emotion Classification**: Joy, Surprise, Trust, Fear, Sadness, Anger
- **Sentiment Intensity**: 감정의 강도 (0-100)
- **Key Phrases**: 감성을 나타내는 주요 문구 추출

**AI 모델**: GPT-4 (정확도 ~92%)

**프롬프트 예시**:
```
Analyze the sentiment of the following Instagram post caption and comments:

Caption: "{caption}"
Comments: [{comments}]

Provide:
1. Overall sentiment (positive/neutral/negative) with confidence score
2. Primary emotions detected
3. Sentiment intensity (0-100)
4. Key phrases that indicate sentiment
5. Cultural nuances (if any)

Return as JSON.
```

---

### 2. 트렌드 예측 (Trend Prediction)

**목적**: 해시태그와 콘텐츠 패턴을 분석하여 다음 트렌드 예측

**분석 항목**:
- **Trend Score**: 현재 트렌드 점수 (0-100)
- **Growth Trajectory**: Rising, Stable, Declining
- **Peak Prediction**: 트렌드 정점 예상 시점
- **Market Potential**: 시장 잠재력 평가
- **Recommended Actions**: 실행 가능한 조언

**AI 모델**: GPT-4 + Time Series Analysis

**분석 로직**:
```python
1. Historical Data: 최근 30일 해시태그 사용량
2. Engagement Trend: 참여도 변화 추이
3. Influencer Adoption: 인플루언서 채택률
4. Cross-market Analysis: 다른 시장과 비교
5. AI Prediction: GPT-4로 종합 예측
```

---

### 3. 콘텐츠 품질 평가 (Content Quality Scoring)

**목적**: 포스트의 마케팅 효과성을 평가

**평가 지표**:
- **Visual Appeal**: 0-100 (이미지/비디오 품질)
- **Caption Quality**: 0-100 (캡션 작성 품질)
- **Hashtag Relevance**: 0-100 (해시태그 적절성)
- **Engagement Potential**: 0-100 (참여 가능성)
- **Brand Alignment**: 0-100 (브랜드 일치성)

**Overall Score**: (각 지표의 가중 평균)

**AI 모델**: GPT-4 Vision (이미지 분석) + GPT-4 (텍스트 분석)

---

### 4. 인플루언서 진정성 분석 (Influencer Authenticity)

**목적**: 인플루언서의 신뢰도와 팔로워 품질 평가

**분석 항목**:
- **Authenticity Score**: 0-100 (진정성 점수)
- **Engagement Quality**: 진짜 참여 vs 봇/스팸
- **Content Consistency**: 콘텐츠 일관성
- **Audience Quality**: 팔로워 품질 (demographics, activity)
- **Partnership History**: 과거 협업 성과

**AI 모델**: Claude 3 (복잡한 추론)

**분석 방법**:
```
1. Engagement Pattern Analysis: 비정상적인 패턴 탐지
2. Comment Quality: 댓글의 진정성 분석
3. Follower Growth: 팔로워 증가 패턴
4. Content Authenticity: 콘텐츠 진정성
5. Cross-reference: 다른 플랫폼과 교차 검증
```

---

### 5. 시장별 문화적 적합성 분석 (Cultural Fit Analysis)

**목적**: 콘텐츠가 타겟 시장의 문화에 적합한지 평가

**분석 항목**:
- **Cultural Alignment**: 0-100 (문화적 일치도)
- **Taboo Detection**: 문화적 금기 탐지
- **Local Preferences**: 현지 선호도 매칭
- **Language Appropriateness**: 언어 사용 적절성
- **Visual Cultural Fit**: 이미지의 문화적 적합성

**AI 모델**: Claude 3 (문화적 뉘앙스 이해)

**시장별 문화 데이터베이스**:
```json
{
  "germany": {
    "values": ["efficiency", "quality", "sustainability"],
    "taboos": ["overly aggressive marketing", "false claims"],
    "preferences": ["natural ingredients", "clinical proof"]
  },
  "france": {
    "values": ["elegance", "sophistication", "tradition"],
    "taboos": ["loud advertising", "too much text"],
    "preferences": ["luxury", "artisanal", "sensory experience"]
  },
  "japan": {
    "values": ["harmony", "precision", "respect"],
    "taboos": ["direct confrontation", "showing off"],
    "preferences": ["cute packaging", "detailed info", "cleanliness"]
  }
}
```

---

## 🔧 기술 스택

### AI/ML Libraries
```python
# OpenAI
openai==1.3.7

# Anthropic
anthropic==0.7.7

# LangChain (Orchestration)
langchain==0.0.350
langchain-openai==0.0.2
langchain-anthropic==0.0.1

# Caching & Embeddings
sentence-transformers==2.2.2
faiss-cpu==1.7.4
```

### Analysis Models
```python
# Sentiment Analysis
- GPT-4-turbo (primary)
- GPT-3.5-turbo (fallback)

# Content Analysis
- GPT-4-vision-preview (image analysis)
- Claude-3-opus (complex reasoning)
- Claude-3-sonnet (cost-effective)

# Embeddings
- text-embedding-3-large (OpenAI)
- all-MiniLM-L6-v2 (Sentence Transformers)
```

---

## 📊 Analysis Database Schema

### Analysis Model

```python
class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Analysis Type
    analysis_type = Column(String)  # sentiment, trend, quality, authenticity, cultural
    
    # Target
    target_type = Column(String)  # post, hashtag, influencer
    target_id = Column(Integer)
    
    # Results (JSON)
    results = Column(JSON)
    
    # Scores
    overall_score = Column(Float)
    confidence = Column(Float)
    
    # Metadata
    model_used = Column(String)  # gpt-4, claude-3-opus
    tokens_used = Column(Integer)
    processing_time = Column(Float)
    
    # Timestamps
    created_at = Column(DateTime)
    expires_at = Column(DateTime)  # Cache expiration
```

### Sample Analysis Result

```json
{
  "analysis_id": 123,
  "analysis_type": "sentiment",
  "target": {
    "type": "post",
    "id": 456,
    "caption": "Loving this new K-Beauty serum! 🌸"
  },
  "results": {
    "sentiment": {
      "overall": "positive",
      "score": 0.92,
      "emotions": {
        "joy": 0.85,
        "trust": 0.70,
        "surprise": 0.40
      },
      "intensity": 87,
      "key_phrases": ["loving", "new", "serum"]
    },
    "cultural_notes": "Emoji usage appropriate for Western markets"
  },
  "confidence": 0.94,
  "model_used": "gpt-4-turbo",
  "tokens_used": 234,
  "processing_time": 1.23,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## ⚙️ AI Analyzer Implementation

### Core Analyzer Class

```python
class AIAnalyzer:
    """
    Core AI analysis engine using GPT-4 and Claude
    """
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.cache = Redis.from_url(settings.REDIS_URL)
    
    async def analyze_sentiment(self, text: str, context: dict) -> dict:
        """Analyze sentiment using GPT-4"""
        pass
    
    async def predict_trend(self, hashtag_data: dict) -> dict:
        """Predict trend trajectory"""
        pass
    
    async def evaluate_content_quality(self, post: dict) -> dict:
        """Evaluate content quality"""
        pass
    
    async def analyze_authenticity(self, influencer: dict) -> dict:
        """Analyze influencer authenticity"""
        pass
    
    async def analyze_cultural_fit(self, content: dict, market: str) -> dict:
        """Analyze cultural appropriateness"""
        pass
```

---

## 🚀 API Endpoints

### POST /api/v1/analysis/sentiment
Analyze sentiment of a post or comment

**Request**:
```json
{
  "target_type": "post",
  "target_id": 123,
  "include_comments": true
}
```

**Response**:
```json
{
  "analysis_id": 456,
  "sentiment": {
    "overall": "positive",
    "score": 0.92,
    "emotions": {...},
    "intensity": 87
  },
  "confidence": 0.94
}
```

### POST /api/v1/analysis/trend
Predict trend for a hashtag

**Request**:
```json
{
  "hashtag": "kbeauty",
  "market": "germany",
  "prediction_window": 30
}
```

### POST /api/v1/analysis/quality
Evaluate content quality

### POST /api/v1/analysis/authenticity
Analyze influencer authenticity

### POST /api/v1/analysis/cultural-fit
Analyze cultural appropriateness

### GET /api/v1/analysis/{analysis_id}
Get analysis results

---

## 💰 Cost Optimization

### Token Usage Optimization

| Analysis Type | Avg Tokens | Cost (GPT-4) | Cache TTL |
|--------------|-----------|--------------|-----------|
| Sentiment | 500 | $0.015 | 24 hours |
| Trend | 1000 | $0.030 | 12 hours |
| Quality | 800 | $0.024 | 24 hours |
| Authenticity | 1500 | $0.045 | 7 days |
| Cultural Fit | 1200 | $0.036 | 7 days |

**Budget per User**: $5/month → ~150 analyses

### Caching Strategy

```python
# Cache analysis results
cache_key = f"analysis:{type}:{target_id}"
cache_ttl = {
    "sentiment": 86400,  # 24 hours
    "trend": 43200,      # 12 hours
    "quality": 86400,
    "authenticity": 604800,  # 7 days
    "cultural": 604800
}
```

### Model Selection

```python
# Use cheaper models for simple tasks
if complexity == "simple":
    model = "gpt-3.5-turbo"  # $0.001/1K tokens
elif complexity == "medium":
    model = "gpt-4-turbo"    # $0.01/1K tokens
else:
    model = "claude-3-opus"  # $0.015/1K tokens
```

---

## 📈 Performance Metrics

### Target KPIs

- **Accuracy**: >90% (sentiment, quality)
- **Response Time**: <3 seconds (cached), <10 seconds (new)
- **Throughput**: 100 analyses/minute
- **Cache Hit Rate**: >70%
- **Cost per Analysis**: <$0.05

### Monitoring

```python
# Metrics to track
- Analysis request volume
- Model usage distribution
- Token consumption
- Cache hit/miss ratio
- Average response time
- Error rate by model
- User satisfaction (feedback)
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
def test_sentiment_analysis():
    analyzer = AIAnalyzer()
    result = analyzer.analyze_sentiment("I love this product!", {})
    assert result["sentiment"]["overall"] == "positive"
    assert result["sentiment"]["score"] > 0.7
```

### Integration Tests
```python
@pytest.mark.asyncio
async def test_full_analysis_workflow():
    # Create post
    post = create_test_post()
    
    # Analyze
    analysis = await analysis_service.analyze_post(post.id)
    
    # Verify
    assert analysis.overall_score > 0
    assert analysis.results is not None
```

### A/B Testing
- Test different prompts
- Compare GPT-4 vs Claude performance
- Optimize for cost vs accuracy

---

## 🔒 Security & Privacy

### Data Privacy
- Anonymize user data before sending to AI APIs
- No PII in analysis requests
- Secure API key management
- Audit logging for all AI requests

### Rate Limiting
```python
# Per-user rate limits
max_analyses_per_hour = 50
max_analyses_per_day = 200
```

---

## 📚 Best Practices

### Prompt Engineering

1. **Clear Instructions**: Be specific about output format
2. **Context Provision**: Include relevant market/cultural context
3. **Few-shot Examples**: Provide examples for better results
4. **Output Validation**: Always validate AI responses
5. **Fallback Handling**: Have fallback for API failures

### Error Handling

```python
try:
    result = await openai_client.chat.completions.create(...)
except OpenAIError as e:
    # Fallback to cached result or simpler model
    logger.error(f"OpenAI error: {e}")
    return fallback_analysis()
```

---

## 🚀 Roadmap

### Phase 1 (Current - Week 2)
- ✅ Sentiment Analysis
- ✅ Trend Prediction
- ✅ Content Quality
- ✅ Basic Caching

### Phase 2 (Week 3-4)
- Custom Fine-tuned Models
- Multi-language Support
- Advanced Cultural Analysis
- Real-time Analysis

### Phase 3 (Month 2)
- Predictive Analytics Dashboard
- Automated Recommendations
- Competitor Analysis
- ROI Prediction

---

**작성일**: 2024-01-15  
**버전**: 1.0  
**작성자**: K-Beauty Global Leap Development Team
