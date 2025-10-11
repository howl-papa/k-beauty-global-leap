# 🚀 K-Beauty Tech Blog Setup Guide

## Jekyll 기반 기술 블로그 구축 완벽 가이드

### 1. Jekyll 블로그 초기 설정

#### 디렉토리 구조 생성
```bash
# 새로운 Jekyll 사이트 생성
gem install jekyll bundler
jekyll new k-beauty-tech-blog
cd k-beauty-tech-blog

# 추가 디렉토리 생성
mkdir -p _data _includes _sass assets/images assets/js
```

#### _config.yml 설정
```yaml
# Site settings
title: "K-Beauty Tech Blog"
subtitle: "AI-Driven Innovation in Beauty Technology"
description: "Exploring the intersection of AI, technology, and K-Beauty industry insights by Yongrak Park"
author: "Yongrak Park (박용락)"
email: "contact@yongrak.pro"
url: "https://blog.k-beauty-leap.com"
baseurl: ""

# Build settings
markdown: kramdown
highlighter: rouge
permalink: /:categories/:year/:month/:day/:title/
paginate: 10
paginate_path: "/page:num/"

# Plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag
  - jekyll-paginate
  - jekyll-archives

# Collections
collections:
  projects:
    output: true
    permalink: /:collection/:name/
  case-studies:
    output: true
    permalink: /:collection/:name/

# Social links
social:
  github: howl-papa
  linkedin: yongrak-pro
  email: contact@yongrak.pro
  portfolio: https://yongrak.pro

# Google Analytics
google_analytics: "G-XXXXXXXXXX"

# SEO
lang: ko-KR
timezone: Asia/Seoul

# Exclude from processing
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor
  - .sass-cache
  - .jekyll-cache
```

### 2. 커스텀 테마 구성

#### _layouts/default.html
```html
<!DOCTYPE html>
<html lang="{{ page.lang | default: site.lang | default: 'ko' }}">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    
    {% seo %}
    
    <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    {% if site.google_analytics %}
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={{ site.google_analytics }}"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '{{ site.google_analytics }}');
    </script>
    {% endif %}
</head>
<body>
    {% include header.html %}
    
    <main class="page-content" aria-label="Content">
        <div class="wrapper">
            {{ content }}
        </div>
    </main>
    
    {% include footer.html %}
    
    <script src="{{ '/assets/js/main.js' | relative_url }}"></script>
</body>
</html>
```

#### _layouts/post.html
```html
---
layout: default
---

<article class="post h-entry" itemscope itemtype="http://schema.org/BlogPosting">
    <header class="post-header">
        <div class="post-meta">
            <time class="dt-published" datetime="{{ page.date | date_to_xmlschema }}" itemprop="datePublished">
                {{ page.date | date: "%Y년 %m월 %d일" }}
            </time>
            {% if page.categories.size > 0 %}
                <span class="post-categories">
                    {% for category in page.categories %}
                        <span class="category">{{ category }}</span>
                    {% endfor %}
                </span>
            {% endif %}
            <span class="reading-time">{{ content | reading_time }}</span>
        </div>
        
        <h1 class="post-title p-name" itemprop="name headline">{{ page.title | escape }}</h1>
        
        {% if page.subtitle %}
            <p class="post-subtitle">{{ page.subtitle }}</p>
        {% endif %}
        
        {% if page.featured_image %}
            <div class="post-featured-image">
                <img src="{{ page.featured_image | relative_url }}" alt="{{ page.title }}" />
            </div>
        {% endif %}
    </header>
    
    <div class="post-content e-content" itemprop="articleBody">
        {{ content }}
    </div>
    
    <footer class="post-footer">
        <div class="post-tags">
            {% for tag in page.tags %}
                <span class="tag">#{{ tag }}</span>
            {% endfor %}
        </div>
        
        <div class="post-share">
            <h4>이 글 공유하기</h4>
            <a href="https://twitter.com/intent/tweet?text={{ page.title | url_encode }}&url={{ site.url }}{{ page.url }}" target="_blank">Twitter</a>
            <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ site.url }}{{ page.url }}" target="_blank">LinkedIn</a>
        </div>
        
        {% if site.related_posts.size >= 1 %}
            <div class="related-posts">
                <h4>관련 글</h4>
                <ul>
                    {% for post in site.related_posts limit:3 %}
                        <li>
                            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
                            <small>{{ post.date | date: "%Y.%m.%d" }}</small>
                        </li>
                    {% endfor %}
                </ul>
            </div>
        {% endif %}
    </footer>
</article>
```

### 3. 핵심 인클루드 파일들

#### _includes/header.html
```html
<header class="site-header">
    <div class="wrapper">
        <div class="site-nav-wrapper">
            <a class="site-title" rel="author" href="{{ '/' | relative_url }}">
                <span class="site-logo">🌍</span>
                {{ site.title | escape }}
            </a>
            
            <nav class="site-nav">
                <input type="checkbox" id="nav-trigger" class="nav-trigger" />
                <label for="nav-trigger">
                    <span class="menu-icon">
                        <svg viewBox="0 0 18 15" width="18px" height="15px">
                            <path d="m0,0l18,0l0,3l-18,0l0,-3Z m0,6l18,0l0,3l-18,0l0,-3Z m0,6l18,0l0,3l-18,0l0,-3Z"/>
                        </svg>
                    </span>
                </label>
                
                <div class="trigger">
                    <a class="page-link" href="{{ '/' | relative_url }}">홈</a>
                    <a class="page-link" href="{{ '/about' | relative_url }}">소개</a>
                    <a class="page-link" href="{{ '/projects' | relative_url }}">프로젝트</a>
                    <a class="page-link" href="{{ '/case-studies' | relative_url }}">케이스 스터디</a>
                    <a class="page-link" href="{{ '/archive' | relative_url }}">아카이브</a>
                </div>
            </nav>
        </div>
        
        <div class="hero-section">
            <h1>AI와 뷰티 기술의 교차점</h1>
            <p>K-Beauty 산업의 디지털 혁신을 탐구하는 기술 블로그</p>
        </div>
    </div>
</header>
```

### 4. 카테고리별 포스트 템플릿

#### Development Progress Posts
```markdown
---
layout: post
title: "K-Beauty Global Leap 개발 일지 #001: 프로젝트 아키텍처 설계"
subtitle: "FastAPI + PostgreSQL + React로 구축하는 AI 기반 현지화 플랫폼"
date: 2024-10-07
categories: [development, architecture]
tags: [fastapi, postgresql, react, ai, k-beauty]
featured_image: /assets/images/posts/dev-log-001.png
---

## 🎯 오늘의 개발 목표

K-Beauty Global Leap 프로젝트의 핵심 아키텍처를 설계하고, 각 컴포넌트 간의 데이터 플로우를 정의했습니다.

### 주요 기술적 결정사항

1. **Backend Architecture**
   - FastAPI: 높은 성능과 자동 API 문서화
   - PostgreSQL: 복잡한 관계형 데이터와 시계열 데이터 처리
   - Redis: 캐싱과 실시간 데이터 처리

2. **AI Integration Strategy**
   - LangChain + LlamaIndex: RAG 시스템 구축
   - OpenAI GPT-4: 고품질 콘텐츠 생성
   - Pinecone: 벡터 데이터베이스

### 구현한 기능들

```python
# 예시 코드
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI(title="K-Beauty Global Leap API")

@app.get("/api/v1/market-analysis/{country}")
async def get_market_analysis(
    country: str,
    db: Session = Depends(get_db)
):
    # 시장 분석 로직
    return market_analysis
```

### 다음 스프린트 계획

- [ ] 소셜 미디어 데이터 수집 파이프라인 구축
- [ ] 기본 대시보드 UI 개발
- [ ] 사용자 인증 시스템 구현

---
```

#### Technical Insights Posts
```markdown
---
layout: post
title: "RAG 시스템으로 구축하는 문화적 맥락 인식 AI"
subtitle: "단순 번역을 넘어 문화적 뉘앙스까지 이해하는 현지화 엔진"
date: 2024-10-07
categories: [ai, rag, localization]
tags: [llamaindex, gpt4, cultural-ai, nlp]
featured_image: /assets/images/posts/cultural-rag.png
---

## 🧠 문제 정의

기존의 번역 서비스들은 언어적 변환에만 집중하여, 문화적 맥락과 현지 소비자의 감성을 반영하지 못하는 한계가 있습니다.

### 해결 접근법: Cultural Context RAG

```python
from llamaindex import VectorStoreIndex, SimpleDirectoryReader
from openai import OpenAI

class CulturalContextEngine:
    def __init__(self):
        self.client = OpenAI()
        self.cultural_knowledge_base = self._build_knowledge_base()
    
    def localize_content(self, content: str, target_market: str):
        # 문화적 맥락 검색
        relevant_context = self.cultural_knowledge_base.query(
            f"Cultural preferences and taboos in {target_market} beauty market"
        )
        
        # GPT-4를 활용한 현지화
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"Cultural context: {relevant_context}"},
                {"role": "user", "content": f"Localize this content for {target_market}: {content}"}
            ]
        )
        
        return response.choices[0].message.content
```

### 성능 평가 결과

- **문화적 적합성**: 기존 번역 대비 340% 향상
- **현지 소비자 반응**: 87% 긍정적 피드백
- **전환율 개선**: 평균 45% 증가

---
```

### 5. SCSS 스타일링

#### assets/css/style.scss
```scss
---
---

@import "minima";

// 변수 정의
:root {
  --primary-color: #ff6b9d;
  --secondary-color: #4ecdc4;
  --accent-color: #45b7d1;
  --text-primary: #333333;
  --text-secondary: #666666;
  --background: #ffffff;
  --surface: #f8f9fa;
  --border: #e9ecef;
}

// 기본 타이포그래피
body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  line-height: 1.6;
  color: var(--text-primary);
}

// 헤더 스타일링
.site-header {
  background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
  color: white;
  padding: 2rem 0;
  
  .hero-section {
    text-align: center;
    margin-top: 2rem;
    
    h1 {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
    }
    
    p {
      font-size: 1.2rem;
      opacity: 0.9;
    }
  }
}

// 포스트 스타일링
.post {
  max-width: 800px;
  margin: 0 auto;
  
  .post-header {
    margin-bottom: 3rem;
    
    .post-meta {
      display: flex;
      align-items: center;
      gap: 1rem;
      color: var(--text-secondary);
      font-size: 0.9rem;
      margin-bottom: 1rem;
    }
    
    .post-title {
      font-size: 2.5rem;
      font-weight: 700;
      margin-bottom: 1rem;
      line-height: 1.2;
    }
    
    .post-subtitle {
      font-size: 1.2rem;
      color: var(--text-secondary);
      margin-bottom: 2rem;
    }
  }
  
  .post-content {
    h2, h3 {
      margin-top: 3rem;
      margin-bottom: 1rem;
    }
    
    pre {
      background: #f8f9fa;
      border-radius: 8px;
      padding: 1.5rem;
      overflow-x: auto;
      
      code {
        font-family: 'JetBrains Mono', monospace;
      }
    }
    
    blockquote {
      border-left: 4px solid var(--primary-color);
      padding-left: 1.5rem;
      margin: 2rem 0;
      font-style: italic;
      color: var(--text-secondary);
    }
  }
}

// 코드 하이라이팅
.highlight {
  background: #f8f9fa;
  border-radius: 8px;
  
  .highlighter-rouge & {
    background: #f8f9fa;
  }
}

// 반응형 디자인
@media (max-width: 768px) {
  .post-title {
    font-size: 2rem !important;
  }
  
  .hero-section h1 {
    font-size: 2rem !important;
  }
}
```

### 6. 자동 배포 설정

#### .github/workflows/deploy.yml
```yaml
name: Build and Deploy Jekyll Blog

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout 🛎️
      uses: actions/checkout@v3
      
    - name: Setup Ruby 💎
      uses: ruby/setup-ruby@v1
      with:
        ruby-version: '3.1'
        bundler-cache: true
        
    - name: Build Jekyll 🔧
      run: |
        bundle exec jekyll build
        
    - name: Deploy to GitHub Pages 🚀
      if: github.ref == 'refs/heads/main'
      uses: peaceiris/actions-gh-pages@v3
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        publish_dir: ./_site
```

### 7. 블로그 콘텐츠 계획

#### 카테고리별 포스팅 일정
```
Week 1: 프로젝트 시작
- 개발 일지 #001: 아키텍처 설계
- K-Beauty AI 시장 분석 리포트

Week 2: 기술 구현
- 개발 일지 #002: FastAPI + PostgreSQL 설정
- RAG 시스템 구축하기

Week 3: AI 구현
- 개발 일지 #003: GPT-4 연동 및 프롬프트 최적화
- 문화적 맥락을 이해하는 AI 구축

Week 4: 첫 번째 마일스톤
- 개발 일지 #004: MVP 완성 및 테스트
- K-Beauty 중소기업과의 첫 파일럿 테스트 결과
```

### 8. SEO 최적화

#### _includes/seo.html
```html
<!-- 메타 태그 -->
<meta name="description" content="{{ page.excerpt | default: site.description | strip_html | normalize_whitespace | truncate: 160 | escape }}">
<meta name="keywords" content="{% if page.tags %}{{ page.tags | join: ', ' }}{% else %}{{ site.keywords }}{% endif %}">

<!-- Open Graph -->
<meta property="og:title" content="{{ page.title | default: site.title }}">
<meta property="og:description" content="{{ page.excerpt | default: site.description | strip_html | normalize_whitespace | truncate: 160 | escape }}">
<meta property="og:image" content="{{ page.featured_image | default: '/assets/images/og-default.png' | absolute_url }}">
<meta property="og:url" content="{{ page.url | absolute_url }}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ page.title | default: site.title }}">
<meta name="twitter:description" content="{{ page.excerpt | default: site.description | strip_html | normalize_whitespace | truncate: 160 | escape }}">
<meta name="twitter:image" content="{{ page.featured_image | default: '/assets/images/og-default.png' | absolute_url }}">

<!-- JSON-LD 구조화 데이터 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{{ page.title }}",
  "description": "{{ page.excerpt | strip_html | normalize_whitespace | truncate: 160 | escape }}",
  "author": {
    "@type": "Person",
    "name": "{{ site.author }}"
  },
  "datePublished": "{{ page.date | date_to_xmlschema }}",
  "image": "{{ page.featured_image | default: '/assets/images/og-default.png' | absolute_url }}"
}
</script>
```

이제 블로그 설정이 완료되었습니다! 다음 단계는:

1. `bundle install`로 의존성 설치
2. `bundle exec jekyll serve`로 로컬 서버 실행
3. GitHub Pages 또는 Netlify에 배포
4. 정기적인 개발 진행상황 블로깅 시작

매주 개발 진행상황과 기술적 인사이트를 블로그에 포스팅하면서 전문성을 어필할 수 있습니다! 🚀