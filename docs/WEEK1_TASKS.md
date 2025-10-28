# 📅 Week 1 상세 작업 목록

> **기간**: 2025년 10월 28일 - 11월 3일  
> **목표**: 기반 인프라 완성 + 첫 데모 준비

---

## ✅ 완료된 작업 (Day 1)

- [x] 프로젝트 디렉토리 구조 생성
- [x] Backend FastAPI 초기 설정
- [x] Frontend Next.js 초기 설정
- [x] Docker Compose 환경 구성
- [x] 핵심 문서 작성 (README, 아키텍처)
- [x] Git 저장소 설정 및 첫 커밋
- [x] Pull Request 생성

---

## 🎯 남은 작업 (Day 2-7)

### Day 2: 데이터베이스 스키마 설계 및 구현

#### Backend 작업

**1. User 모델 생성**
```python
# backend/app/models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    company_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    analyses = relationship("Analysis", back_populates="user")
```

**2. Company 모델 생성**
```python
# backend/app/models/company.py
class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    industry = Column(String)  # "skincare", "makeup", etc.
    target_markets = Column(JSON)  # ["germany", "france", "japan"]
    website = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="company")
```

**3. Analysis 모델 생성**
```python
# backend/app/models/analysis.py
class Analysis(Base):
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # "trend", "localization", "competitor"
    input_data = Column(JSON)
    output_data = Column(JSON)
    status = Column(String)  # "pending", "processing", "completed", "failed"
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="analyses")
```

**4. Alembic 마이그레이션 생성**
```bash
cd backend
alembic revision --autogenerate -m "Create user, company, and analysis models"
alembic upgrade head
```

#### 체크리스트
- [ ] User 모델 구현
- [ ] Company 모델 구현
- [ ] Analysis 모델 구현
- [ ] Alembic 마이그레이션 실행
- [ ] 테스트 데이터 생성 스크립트

---

### Day 3: 인증 시스템 구현

#### Backend 작업

**1. Password 유틸리티**
```python
# backend/app/core/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt
```

**2. 회원가입 API**
```python
# backend/app/api/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import get_password_hash

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        company_name=user_data.company_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user
```

**3. 로그인 API**
```python
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
```

**4. 현재 사용자 가져오기**
```python
# backend/app/api/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
```

**5. Pydantic 스키마**
```python
# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    company_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    company_name: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
```

#### 체크리스트
- [ ] 보안 유틸리티 구현
- [ ] 회원가입 API
- [ ] 로그인 API
- [ ] JWT 토큰 검증
- [ ] 현재 사용자 의존성
- [ ] Pydantic 스키마

---

### Day 4: 프론트엔드 레이아웃 및 인증 UI

#### Frontend 작업

**1. Next.js 페이지 구조**
```typescript
// frontend/src/app/page.tsx - 랜딩 페이지
// frontend/src/app/login/page.tsx - 로그인
// frontend/src/app/signup/page.tsx - 회원가입
// frontend/src/app/dashboard/page.tsx - 대시보드 (인증 필요)
```

**2. API 클라이언트 설정**
```typescript
// frontend/src/utils/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

// Request interceptor to add token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

**3. 인증 스토어 (Zustand)**
```typescript
// frontend/src/store/authStore.ts
import { create } from 'zustand';
import api from '@/utils/api';

interface User {
  id: number;
  email: string;
  full_name: string | null;
  company_name: string | null;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  
  login: async (email, password) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/api/v1/auth/login', formData);
    const { access_token } = response.data;
    
    localStorage.setItem('access_token', access_token);
    
    // Get user info
    const userResponse = await api.get('/api/v1/users/me');
    set({ 
      user: userResponse.data, 
      token: access_token, 
      isAuthenticated: true 
    });
  },
  
  signup: async (data) => {
    await api.post('/api/v1/auth/signup', data);
    // Auto login after signup
    await useAuthStore.getState().login(data.email, data.password);
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null, token: null, isAuthenticated: false });
  },
}));
```

**4. 로그인 페이지**
```typescript
// frontend/src/app/login/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/store/authStore';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();
  const login = useAuthStore((state) => state.login);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8 p-8 bg-white rounded-xl shadow-lg">
        <div>
          <h2 className="text-3xl font-bold text-center text-gray-900">
            K-Beauty Global Leap
          </h2>
          <p className="mt-2 text-center text-gray-600">
            Sign in to your account
          </p>
        </div>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded">
              {error}
            </div>
          )}
          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <input
                id="email"
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Password
              </label>
              <input
                id="password"
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              />
            </div>
          </div>
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            Sign in
          </button>
          <div className="text-center">
            <a href="/signup" className="text-sm text-primary-600 hover:text-primary-500">
              Don't have an account? Sign up
            </a>
          </div>
        </form>
      </div>
    </div>
  );
}
```

**5. 대시보드 레이아웃**
```typescript
// frontend/src/app/dashboard/layout.tsx
'use client';

import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated, user, logout } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-primary-600">
                K-Beauty Global Leap
              </h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-700">{user?.email}</span>
              <button
                onClick={logout}
                className="text-sm text-gray-600 hover:text-gray-900"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Sidebar & Content */}
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white h-screen shadow-sm">
          <nav className="mt-5 px-2">
            <a
              href="/dashboard"
              className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-900 bg-gray-100"
            >
              Dashboard
            </a>
            <a
              href="/dashboard/trend-analysis"
              className="mt-1 group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            >
              Trend Analysis
            </a>
            <a
              href="/dashboard/localization"
              className="mt-1 group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            >
              Localization
            </a>
            <a
              href="/dashboard/competitors"
              className="mt-1 group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
            >
              Competitors
            </a>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          {children}
        </main>
      </div>
    </div>
  );
}
```

#### 체크리스트
- [ ] API 클라이언트 설정
- [ ] 인증 스토어 (Zustand)
- [ ] 로그인 페이지
- [ ] 회원가입 페이지
- [ ] 대시보드 레이아웃
- [ ] Protected Route 구현

---

### Day 5-6: Instagram API 연동 준비

#### 사전 작업

**1. Instagram Graph API 설정**
- [ ] Facebook Developer 계정 생성
- [ ] Instagram Business 계정 연결
- [ ] Graph API Access Token 발급
- [ ] API 권한 설정

**2. 테스트 데이터 준비**
```python
# backend/app/services/instagram_service.py
import aiohttp
from typing import List, Dict
from app.core.config import settings

class InstagramService:
    def __init__(self):
        self.access_token = settings.INSTAGRAM_ACCESS_TOKEN
        self.base_url = "https://graph.instagram.com/v18.0"
    
    async def search_hashtag(self, hashtag: str) -> Dict:
        """Search for posts by hashtag"""
        # Implementation
        pass
    
    async def get_hashtag_insights(self, hashtag_id: str) -> Dict:
        """Get insights for a specific hashtag"""
        # Implementation
        pass
    
    async def analyze_posts(self, posts: List[Dict]) -> Dict:
        """Analyze engagement metrics"""
        total_posts = len(posts)
        total_likes = sum(post.get('like_count', 0) for post in posts)
        total_comments = sum(post.get('comments_count', 0) for post in posts)
        
        return {
            "total_posts": total_posts,
            "avg_likes": total_likes / total_posts if total_posts > 0 else 0,
            "avg_comments": total_comments / total_posts if total_posts > 0 else 0,
            "engagement_rate": (total_likes + total_comments) / total_posts if total_posts > 0 else 0
        }
```

**3. Mock 데이터 생성 (API 대기 중)**
```python
# backend/app/services/mock_data.py
def get_mock_instagram_data(hashtag: str, country: str) -> Dict:
    """Generate mock data for testing"""
    return {
        "hashtag": hashtag,
        "country": country,
        "posts_count": 1250,
        "avg_engagement_rate": 4.2,
        "top_posts": [
            {
                "caption": "Amazing Korean skincare routine...",
                "likes": 2500,
                "comments": 145,
                "posted_at": "2025-10-25"
            }
        ],
        "trending_keywords": ["glass skin", "hydration", "vegan"],
        "insights": "Glass skin trend is growing +340% in Germany"
    }
```

#### 체크리스트
- [ ] Instagram Developer 계정 설정
- [ ] API 토큰 발급
- [ ] Instagram Service 클래스 구현
- [ ] Mock 데이터 생성
- [ ] API 엔드포인트 생성

---

### Day 7: 첫 데모 준비 및 블로그 포스팅

#### 데모 준비

**1. 간단한 트렌드 분석 페이지**
```typescript
// frontend/src/app/dashboard/trend-analysis/page.tsx
'use client';

import { useState } from 'react';
import api from '@/utils/api';

export default function TrendAnalysisPage() {
  const [country, setCountry] = useState('germany');
  const [hashtag, setHashtag] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const response = await api.post('/api/v1/analysis/trend', {
        country,
        hashtag,
      });
      setResults(response.data);
    } catch (error) {
      console.error('Analysis failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">Instagram Trend Analysis</h1>
      
      <div className="bg-white p-6 rounded-lg shadow">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2">Country</label>
            <select
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="germany">Germany</option>
              <option value="france">France</option>
              <option value="japan">Japan</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Hashtag</label>
            <input
              type="text"
              value={hashtag}
              onChange={(e) => setHashtag(e.target.value)}
              placeholder="#koreanbeauty"
              className="w-full border rounded px-3 py-2"
            />
          </div>
        </div>
        
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="mt-4 bg-primary-600 text-white px-6 py-2 rounded hover:bg-primary-700"
        >
          {loading ? 'Analyzing...' : 'Analyze Trend'}
        </button>
        
        {results && (
          <div className="mt-6">
            <h3 className="text-lg font-semibold mb-4">Results</h3>
            <pre className="bg-gray-50 p-4 rounded">
              {JSON.stringify(results, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
```

**2. 데모 영상 촬영 스크립트**
```
[0:00-0:10] 인트로
"안녕하세요, 뷰티인사이드랩의 박용락입니다. 
오늘은 K-뷰티 브랜드를 위한 AI 트렌드 분석 도구를 소개합니다."

[0:10-0:30] 문제 제시
"해외 진출 시 가장 큰 고민이 무엇인가요?
현지 트렌드를 모른다는 것입니다.
우리 플랫폼이 이 문제를 해결합니다."

[0:30-1:00] 데모
"독일 시장의 #koreanbeauty 트렌드를 분석해보겠습니다.
클릭 한 번으로 실시간 데이터를 수집하고,
AI가 자동으로 인사이트를 제공합니다."

[1:00-1:20] 결과 설명
"보시는 것처럼, 글로잉 스킨케어가 급상승 중이고,
비건 성분에 대한 관심이 높습니다.
이런 인사이트를 바탕으로 마케팅 전략을 수립할 수 있습니다."

[1:20-1:30] 클로징
"K-뷰티 브랜드의 글로벌 성공을 위한 첫 걸음,
지금 바로 시작하세요. www.beautyinsightlab.com"
```

**3. 기술 블로그 포스트 #1 작성**
```markdown
제목: "K-뷰티 AI 플랫폼 개발 시작 - 개발 일지 #1"

목차:
1. 왜 이 프로젝트를 시작했는가
2. 기술 스택 선정 이유
   - FastAPI: 높은 성능과 자동 문서화
   - Next.js: SEO와 사용자 경험
   - PostgreSQL: 복잡한 데이터 관계
3. 1주차 개발 성과
   - 전체 아키텍처 구축
   - 인증 시스템 완성
   - 첫 기능 프로토타입
4. 다음 주 계획
   - Instagram API 연동
   - AI 트렌드 분석 엔진
5. 함께 성장하고 싶은 분들을 찾습니다
```

#### 체크리스트
- [ ] 트렌드 분석 프로토타입 UI
- [ ] 데모 영상 촬영
- [ ] LinkedIn 포스트 작성
- [ ] 기술 블로그 포스트 작성 및 발행
- [ ] GitHub README 업데이트

---

## 📊 Week 1 완료 기준

### 개발 측면
- ✅ 로컬 환경에서 전체 스택 실행 가능
- ✅ 회원가입/로그인 동작
- ✅ 대시보드 접근 가능
- ✅ 첫 번째 분석 기능 프로토타입 완성

### 비즈니스 측면
- 📝 기술 블로그 포스트 1개 발행
- 🎥 데모 영상 1개 제작
- 💼 LinkedIn 포스트 3개 이상
- 📧 잠재 고객 리스트 20곳 수집

---

## 🚀 다음 주 미리보기 (Week 2)

1. Instagram Graph API 완전 통합
2. OpenAI GPT-4 트렌드 분석
3. 데이터 시각화 (Recharts)
4. 첫 파일럿 고객 컨택 시작

---

**"매일 조금씩, 꾸준히. 완벽함보다 완료가 중요하다!"** 💪
