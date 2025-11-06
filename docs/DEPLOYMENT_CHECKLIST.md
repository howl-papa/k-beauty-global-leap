# MVP 실제 도메인 배포 업무 리스트
# Deployment Checklist for www.beautyinsightlab.com

**도메인**: www.beautyinsightlab.com (가비아 구매 완료)  
**목표**: MVP를 실제 프로덕션 환경에서 작동하도록 배포  
**예상 소요 시간**: 2-3주  
**작성일**: 2024년 10월 28일

---

## 📋 목차

1. [도메인 및 DNS 설정](#1-도메인-및-dns-설정)
2. [호스팅 환경 구성](#2-호스팅-환경-구성)
3. [백엔드 배포](#3-백엔드-배포)
4. [프론트엔드 배포](#4-프론트엔드-배포)
5. [데이터베이스 설정](#5-데이터베이스-설정)
6. [SSL/HTTPS 인증서](#6-sslhttps-인증서)
7. [환경 변수 설정](#7-환경-변수-설정)
8. [모니터링 및 로깅](#8-모니터링-및-로깅)
9. [성능 최적화](#9-성능-최적화)
10. [보안 설정](#10-보안-설정)
11. [테스팅 및 검증](#11-테스팅-및-검증)
12. [런치 준비](#12-런치-준비)

---

## 1. 도메인 및 DNS 설정

### 가비아 도메인 설정

#### 1.1 도메인 관리 페이지 접속
```
✅ 작업:
1. 가비아 (www.gabia.com) 로그인
2. [My가비아] → [서비스 관리] 이동
3. 도메인 목록에서 "beautyinsightlab.com" 선택
```

#### 1.2 DNS 레코드 설정

**서브도메인 구조**:
```
www.beautyinsightlab.com     → 프론트엔드 (메인 웹사이트)
api.beautyinsightlab.com     → 백엔드 API
admin.beautyinsightlab.com   → 관리자 대시보드 (향후)
```

**가비아 DNS 설정 방법**:

```
✅ 작업: DNS 관리 → DNS 정보 → 레코드 추가

A 레코드 설정:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
호스트명         타입    값/데이터           TTL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@               A       [프론트엔드 IP]     3600
www             A       [프론트엔드 IP]     3600
api             A       [백엔드 IP]         3600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CNAME 레코드 (또는 대안):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
호스트명         타입     값/데이터                    TTL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
www             CNAME    beautyinsightlab.vercel.app  3600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

참고:
- [프론트엔드 IP]: Vercel/Cloudflare Pages IP 또는 CNAME 사용
- [백엔드 IP]: AWS EC2/Lightsail 또는 Cloud Run IP
- TTL: 3600초 (1시간) 권장, 테스트 시에는 300초로 설정
```

#### 1.3 DNS 전파 확인

```bash
✅ 작업: DNS 전파 확인 (24-48시간 소요 가능)

# 로컬에서 확인
nslookup www.beautyinsightlab.com
nslookup api.beautyinsightlab.com

# 또는 온라인 도구 사용
https://www.whatsmydns.net/
```

**예상 결과**:
```
www.beautyinsightlab.com → [프론트엔드 서버 IP]
api.beautyinsightlab.com → [백엔드 서버 IP]
```

---

## 2. 호스팅 환경 구성

### 2.1 프론트엔드 호스팅 선택

**옵션 A: Vercel (권장)** ⭐
```
장점:
✅ Next.js에 최적화
✅ 자동 HTTPS/SSL
✅ 글로벌 CDN 포함
✅ 무료 티어 충분 (월 100GB 대역폭)
✅ 자동 배포 (Git 연동)

단점:
- 한국 서버 없음 (속도 영향 미미)

가격: 무료 (Pro: $20/월)
```

**옵션 B: Cloudflare Pages**
```
장점:
✅ 무제한 대역폭 (무료)
✅ 빠른 글로벌 CDN
✅ 자동 HTTPS

단점:
- Vercel보다 Next.js 호환성 낮음

가격: 무료
```

**옵션 C: AWS S3 + CloudFront**
```
장점:
✅ AWS 생태계 통합
✅ 완전한 제어 가능

단점:
- 설정 복잡
- 비용 예측 어려움

가격: ~$5-20/월
```

**추천**: Vercel (설정 간편, Next.js 최적화)

### 2.2 백엔드 호스팅 선택

**옵션 A: AWS EC2 (권장)** ⭐
```
장점:
✅ 완전한 제어
✅ PostgreSQL, Redis 동일 서버 가능
✅ 한국 리전 선택 가능 (ap-northeast-2)
✅ 확장성 우수

단점:
- 서버 관리 필요
- 초기 설정 복잡

권장 스펙:
- t3.medium (2 vCPU, 4GB RAM)
- 30GB SSD
- 가격: ~$40-50/월
```

**옵션 B: AWS Lightsail**
```
장점:
✅ EC2보다 간단한 설정
✅ 고정 가격
✅ 한국 리전 있음

단점:
- 확장성 제한

가격: $20-40/월
```

**옵션 C: Google Cloud Run**
```
장점:
✅ 서버리스 (자동 스케일링)
✅ 사용한 만큼만 과금
✅ Docker 기반 배포

단점:
- Cold start 이슈
- 한국 리전 없음

가격: ~$10-30/월 (사용량 기반)
```

**옵션 D: Heroku**
```
장점:
✅ 가장 간단한 배포
✅ Git push로 배포
✅ 무료 티어 있음 (제한적)

단점:
- 비쌈 (스케일링 시)
- 한국 서버 없음

가격: 무료 (Hobby: $7/월, Production: $25+/월)
```

**추천**: AWS EC2 (성능, 제어, 확장성)

### 2.3 데이터베이스 호스팅

**옵션 A: AWS RDS PostgreSQL (권장)** ⭐
```
장점:
✅ 관리형 서비스 (백업, 패치 자동)
✅ 높은 가용성
✅ EC2와 같은 VPC

권장 스펙:
- db.t3.micro (개발/테스트)
- db.t3.small (프로덕션)
- 20GB SSD

가격: ~$15-40/월
```

**옵션 B: EC2에 직접 설치**
```
장점:
✅ 비용 절감
✅ 완전한 제어

단점:
- 백업, 관리 직접 해야 함
- 고가용성 설정 복잡

가격: 포함 (EC2 비용에)
```

**옵션 C: Supabase (PostgreSQL SaaS)**
```
장점:
✅ 무료 티어 (500MB)
✅ 관리 불필요
✅ 자동 백업

단점:
- 한국 리전 없음
- 확장 시 비쌈

가격: 무료 (Pro: $25/월)
```

**추천**: 
- 개발 단계: Supabase 무료 티어
- 프로덕션: AWS RDS (안정성)

### 2.4 캐시 서버 (Redis)

**옵션 A: AWS ElastiCache Redis**
```
가격: ~$15-30/월
권장: cache.t3.micro
```

**옵션 B: EC2에 직접 설치**
```
가격: 무료 (EC2에 포함)
메모리: 1GB 할당
```

**추천**: EC2에 직접 설치 (비용 절감)

---

## 3. 백엔드 배포

### 3.1 AWS EC2 인스턴스 생성

```
✅ 작업: AWS Console에서 EC2 인스턴스 생성

설정:
1. 리전: 서울 (ap-northeast-2)
2. AMI: Ubuntu 22.04 LTS
3. 인스턴스 타입: t3.medium
4. 스토리지: 30GB gp3 SSD
5. 보안 그룹:
   - SSH (22): 본인 IP만
   - HTTP (80): 0.0.0.0/0
   - HTTPS (443): 0.0.0.0/0
   - Custom TCP (8000): 0.0.0.0/0 (백엔드 API)
   - PostgreSQL (5432): EC2 보안 그룹 내부만
   - Redis (6379): EC2 보안 그룹 내부만
```

### 3.2 서버 초기 설정

```bash
✅ 작업: SSH로 접속 후 초기 설정

# 1. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 2. 필수 패키지 설치
sudo apt install -y \
    python3.11 \
    python3.11-venv \
    python3-pip \
    postgresql-14 \
    redis-server \
    nginx \
    git \
    curl \
    build-essential \
    libpq-dev

# 3. Python 버전 확인
python3.11 --version

# 4. pip 업그레이드
pip3 install --upgrade pip
```

### 3.3 PostgreSQL 설정

```bash
✅ 작업: PostgreSQL 데이터베이스 생성

# 1. PostgreSQL 접속
sudo -u postgres psql

# 2. 데이터베이스 및 사용자 생성
CREATE DATABASE kbeauty_db;
CREATE USER kbeauty_user WITH PASSWORD 'your_secure_password_here';
ALTER ROLE kbeauty_user SET client_encoding TO 'utf8';
ALTER ROLE kbeauty_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE kbeauty_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE kbeauty_db TO kbeauty_user;
\q

# 3. 외부 접속 허용 (필요시)
sudo nano /etc/postgresql/14/main/postgresql.conf
# listen_addresses = 'localhost' → listen_addresses = '*'

sudo nano /etc/postgresql/14/main/pg_hba.conf
# 추가: host all all 0.0.0.0/0 md5

# 4. PostgreSQL 재시작
sudo systemctl restart postgresql
```

### 3.4 Redis 설정

```bash
✅ 작업: Redis 설정

# 1. Redis 설정 파일 수정
sudo nano /etc/redis/redis.conf

# 변경 사항:
# bind 127.0.0.1 → bind 0.0.0.0 (필요시, 보안 주의)
# maxmemory 1gb (캐시 최대 메모리)
# maxmemory-policy allkeys-lru (메모리 부족 시 LRU 정책)

# 2. Redis 재시작
sudo systemctl restart redis-server

# 3. Redis 상태 확인
sudo systemctl status redis-server

# 4. Redis 접속 테스트
redis-cli ping
# 응답: PONG
```

### 3.5 백엔드 코드 배포

```bash
✅ 작업: 백엔드 코드 배포 및 실행

# 1. 프로젝트 디렉토리 생성
sudo mkdir -p /var/www/kbeauty-backend
sudo chown $USER:$USER /var/www/kbeauty-backend
cd /var/www/kbeauty-backend

# 2. Git 저장소 클론
git clone https://github.com/howl-papa/k-beauty-global-leap.git .

# 3. Python 가상 환경 생성
python3.11 -m venv venv
source venv/bin/activate

# 4. 의존성 설치
cd backend
pip install -r requirements.txt

# 5. 환경 변수 설정
nano .env
# (환경 변수는 섹션 7 참조)

# 6. 데이터베이스 마이그레이션
alembic upgrade head

# 7. 애플리케이션 실행 테스트
uvicorn app.main:app --host 0.0.0.0 --port 8000
# Ctrl+C로 중단
```

### 3.6 Systemd 서비스 설정 (자동 시작)

```bash
✅ 작업: Systemd 서비스 파일 생성

# 1. 서비스 파일 생성
sudo nano /etc/systemd/system/kbeauty-backend.service

# 내용:
[Unit]
Description=K-Beauty Global Leap Backend API
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/kbeauty-backend/backend
Environment="PATH=/var/www/kbeauty-backend/venv/bin"
ExecStart=/var/www/kbeauty-backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# 2. 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable kbeauty-backend
sudo systemctl start kbeauty-backend

# 3. 상태 확인
sudo systemctl status kbeauty-backend

# 4. 로그 확인
sudo journalctl -u kbeauty-backend -f
```

### 3.7 Nginx 리버스 프록시 설정

```bash
✅ 작업: Nginx를 통한 백엔드 프록시 설정

# 1. Nginx 설정 파일 생성
sudo nano /etc/nginx/sites-available/api.beautyinsightlab.com

# 내용:
server {
    listen 80;
    server_name api.beautyinsightlab.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}

# 2. 심볼릭 링크 생성
sudo ln -s /etc/nginx/sites-available/api.beautyinsightlab.com /etc/nginx/sites-enabled/

# 3. Nginx 설정 테스트
sudo nginx -t

# 4. Nginx 재시작
sudo systemctl restart nginx

# 5. 상태 확인
sudo systemctl status nginx
```

### 3.8 백엔드 배포 스크립트 생성

```bash
✅ 작업: 자동 배포 스크립트 생성

# 파일: /var/www/kbeauty-backend/deploy.sh
nano /var/www/kbeauty-backend/deploy.sh

# 내용:
#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# 1. Git pull
cd /var/www/kbeauty-backend
git pull origin main

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. Restart service
sudo systemctl restart kbeauty-backend

# 6. Check status
sudo systemctl status kbeauty-backend

echo "✅ Deployment completed!"

# 실행 권한 부여
chmod +x /var/www/kbeauty-backend/deploy.sh

# 사용법:
# ./deploy.sh
```

---

## 4. 프론트엔드 배포

### 4.1 Vercel 계정 설정

```
✅ 작업: Vercel 가입 및 프로젝트 연결

1. Vercel 가입
   - https://vercel.com 접속
   - GitHub 계정으로 가입

2. 프로젝트 Import
   - Dashboard → New Project
   - GitHub 저장소 선택: k-beauty-global-leap
   - Root Directory 설정: frontend
   - Framework Preset: Next.js (자동 감지)

3. 환경 변수 설정
   - Settings → Environment Variables
   - 추가: NEXT_PUBLIC_API_URL = https://api.beautyinsightlab.com/api/v1

4. 빌드 설정 확인
   - Build Command: npm run build
   - Output Directory: .next
   - Install Command: npm install
```

### 4.2 커스텀 도메인 연결

```
✅ 작업: Vercel에 커스텀 도메인 연결

1. Vercel Dashboard → Settings → Domains
2. Add Domain 클릭
3. 입력: www.beautyinsightlab.com
4. Vercel이 제공하는 DNS 설정 따르기:

옵션 A: CNAME 방식 (권장)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
가비아 DNS 설정:
호스트명: www
타입: CNAME
값: cname.vercel-dns.com
TTL: 3600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

옵션 B: A 레코드 방식
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
가비아 DNS 설정:
호스트명: www
타입: A
값: 76.76.21.21 (Vercel IP)
TTL: 3600
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

5. DNS 전파 확인 (10분-24시간)
6. Vercel에서 SSL 자동 발급 확인
```

### 4.3 자동 배포 설정

```
✅ 작업: Git Push 시 자동 배포 설정

Vercel은 자동으로 설정됨:
- main 브랜치 push → 프로덕션 배포
- 다른 브랜치 push → 프리뷰 배포

확인:
1. 코드 수정
2. Git commit & push
3. Vercel Dashboard에서 배포 진행 상황 확인
4. 배포 완료 시 자동 URL 생성
```

### 4.4 프론트엔드 환경 변수 설정

```
✅ 작업: Vercel 환경 변수 설정

Vercel Dashboard → Settings → Environment Variables

추가할 변수:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Key                          Value
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT_PUBLIC_API_URL          https://api.beautyinsightlab.com/api/v1
NEXT_PUBLIC_APP_NAME         K-Beauty Global Leap
NEXT_PUBLIC_APP_VERSION      0.1.0
NEXT_PUBLIC_ENABLE_ANALYTICS false (처음에는)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Environment: Production, Preview, Development 모두 선택
```

---

## 5. 데이터베이스 설정

### 5.1 프로덕션 데이터베이스 생성

**AWS RDS 사용 시**:

```
✅ 작업: AWS RDS PostgreSQL 인스턴스 생성

1. AWS Console → RDS → Create Database

설정:
- Engine: PostgreSQL 14.x
- Template: Production (또는 Dev/Test)
- DB instance identifier: kbeauty-db-prod
- Master username: kbeauty_admin
- Master password: [강력한 비밀번호]
- DB instance class: db.t3.small (2 vCPU, 2GB RAM)
- Storage: 20GB gp3 SSD
- Multi-AZ: No (비용 절감, 필요 시 Yes)
- VPC: EC2와 같은 VPC
- Public access: No
- VPC security group: PostgreSQL (5432) 허용 (EC2에서만)
- Initial database name: kbeauty_db

2. RDS 엔드포인트 확인
   - kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com

3. 백엔드 .env 파일 업데이트
   - DATABASE_URL=postgresql://kbeauty_admin:password@kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com:5432/kbeauty_db
```

### 5.2 데이터베이스 마이그레이션

```bash
✅ 작업: 프로덕션 DB에 스키마 생성

# EC2 서버에서 실행
cd /var/www/kbeauty-backend/backend
source ../venv/bin/activate

# 마이그레이션 실행
alembic upgrade head

# 확인
psql -h kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com \
     -U kbeauty_admin \
     -d kbeauty_db \
     -c "\dt"

# 예상 출력: users, companies, instagram_posts 등 테이블 목록
```

### 5.3 데이터베이스 백업 설정

```
✅ 작업: 자동 백업 설정

AWS RDS:
1. RDS Console → Modify DB Instance
2. Backup retention period: 7 days
3. Backup window: 03:00-04:00 UTC (한국 시간 12:00-13:00)
4. Apply immediately

수동 백업 스크립트:
nano /var/www/kbeauty-backend/backup.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/var/backups/kbeauty"
mkdir -p $BACKUP_DIR

pg_dump -h kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com \
        -U kbeauty_admin \
        -d kbeauty_db \
        -F c \
        -f $BACKUP_DIR/kbeauty_db_$DATE.dump

# 7일 이상 오래된 백업 삭제
find $BACKUP_DIR -type f -mtime +7 -delete

chmod +x backup.sh

# Cron 설정 (매일 새벽 2시)
crontab -e
0 2 * * * /var/www/kbeauty-backend/backup.sh
```

---

## 6. SSL/HTTPS 인증서

### 6.1 프론트엔드 SSL (Vercel)

```
✅ 작업: Vercel 자동 SSL

Vercel은 Let's Encrypt SSL을 자동으로 발급합니다.

확인:
1. www.beautyinsightlab.com 접속
2. 브라우저 주소창에 자물쇠 아이콘 확인
3. 인증서 정보 확인: Let's Encrypt Authority X3

자동 갱신: Vercel이 자동으로 처리
```

### 6.2 백엔드 SSL (Certbot + Let's Encrypt)

```bash
✅ 작업: EC2에 SSL 인증서 설치

# 1. Certbot 설치
sudo apt install -y certbot python3-certbot-nginx

# 2. SSL 인증서 발급
sudo certbot --nginx -d api.beautyinsightlab.com

# 프롬프트 응답:
# Email: your-email@example.com
# Terms of Service: Agree (A)
# Share email: No (N)
# Redirect HTTP to HTTPS: Yes (2)

# 3. 자동 갱신 확인
sudo certbot renew --dry-run

# 4. Cron에 자동 갱신 등록 (이미 자동으로 설정됨)
sudo systemctl status certbot.timer

# 5. Nginx 설정 확인
sudo nano /etc/nginx/sites-available/api.beautyinsightlab.com

# Certbot이 자동으로 추가한 SSL 설정 확인:
server {
    listen 443 ssl;
    server_name api.beautyinsightlab.com;
    
    ssl_certificate /etc/letsencrypt/live/api.beautyinsightlab.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.beautyinsightlab.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # ... 기존 proxy 설정 ...
}

# HTTP → HTTPS 리다이렉트
server {
    listen 80;
    server_name api.beautyinsightlab.com;
    return 301 https://$server_name$request_uri;
}

# 6. Nginx 재시작
sudo systemctl restart nginx

# 7. HTTPS 접속 확인
curl https://api.beautyinsightlab.com/health
```

### 6.3 SSL 등급 확인

```
✅ 작업: SSL 보안 등급 확인

1. SSL Labs 테스트
   https://www.ssllabs.com/ssltest/

2. 도메인 입력: api.beautyinsightlab.com

3. 목표 등급: A 또는 A+

4. 만약 B 이하일 경우, Nginx SSL 설정 강화:
   sudo nano /etc/letsencrypt/options-ssl-nginx.conf
   # TLS 1.2, 1.3만 허용
   # Strong ciphers only
```

---

## 7. 환경 변수 설정

### 7.1 백엔드 환경 변수

```bash
✅ 작업: 프로덕션 환경 변수 설정

파일: /var/www/kbeauty-backend/backend/.env

# ===========================================
# 데이터베이스
# ===========================================
DATABASE_URL=postgresql://kbeauty_admin:YOUR_SECURE_PASSWORD@kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com:5432/kbeauty_db

# ===========================================
# Redis
# ===========================================
REDIS_URL=redis://localhost:6379/0

# ===========================================
# JWT 인증
# ===========================================
SECRET_KEY=your-super-secret-jwt-key-min-32-characters-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# ===========================================
# Instagram API
# ===========================================
INSTAGRAM_CLIENT_ID=your_instagram_app_id
INSTAGRAM_CLIENT_SECRET=your_instagram_app_secret
INSTAGRAM_REDIRECT_URI=https://www.beautyinsightlab.com/auth/instagram/callback

# ===========================================
# OpenAI
# ===========================================
OPENAI_API_KEY=sk-proj-your-openai-api-key-here

# ===========================================
# Anthropic (Optional Backup)
# ===========================================
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key-here

# ===========================================
# 애플리케이션 설정
# ===========================================
APP_NAME=K-Beauty Global Leap
APP_VERSION=0.1.0
ENVIRONMENT=production
DEBUG=False

# ===========================================
# CORS (프론트엔드 도메인)
# ===========================================
BACKEND_CORS_ORIGINS=["https://www.beautyinsightlab.com","https://beautyinsightlab.com"]

# ===========================================
# Email (향후 사용)
# ===========================================
# SMTP_HOST=smtp.gmail.com
# SMTP_PORT=587
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-specific-password

# ===========================================
# 모니터링 (선택)
# ===========================================
# SENTRY_DSN=https://your-sentry-dsn
# DATADOG_API_KEY=your-datadog-api-key
```

**보안 주의사항**:
```bash
# 파일 권한 설정
chmod 600 /var/www/kbeauty-backend/backend/.env
chown ubuntu:ubuntu /var/www/kbeauty-backend/backend/.env

# Git에 절대 커밋하지 않기 (.gitignore 확인)
cat .gitignore | grep .env
# 출력: .env
```

### 7.2 프론트엔드 환경 변수

```
✅ 작업: Vercel 환경 변수 (이미 섹션 4.4에서 설정)

Vercel Dashboard → Settings → Environment Variables

NEXT_PUBLIC_API_URL=https://api.beautyinsightlab.com/api/v1
NEXT_PUBLIC_APP_NAME=K-Beauty Global Leap
NEXT_PUBLIC_APP_VERSION=0.1.0
```

### 7.3 환경 변수 검증

```bash
✅ 작업: 설정된 환경 변수 확인

# 백엔드에서
cd /var/www/kbeauty-backend/backend
source ../venv/bin/activate
python -c "from app.core.config import settings; print(settings.DATABASE_URL)"
# 출력: postgresql://...

# 프론트엔드 빌드 로그에서 확인
# Vercel Dashboard → Deployments → Latest → Build Logs
# "Using environment variable: NEXT_PUBLIC_API_URL=..." 확인
```

---

## 8. 모니터링 및 로깅

### 8.1 백엔드 로깅 설정

```bash
✅ 작업: 로깅 설정

# 1. 로그 디렉토리 생성
sudo mkdir -p /var/log/kbeauty
sudo chown ubuntu:ubuntu /var/log/kbeauty

# 2. Systemd 서비스 로그
# 실시간 로그 보기
sudo journalctl -u kbeauty-backend -f

# 최근 100줄
sudo journalctl -u kbeauty-backend -n 100

# 특정 시간대
sudo journalctl -u kbeauty-backend --since "1 hour ago"

# 3. 애플리케이션 로그 파일 설정
# backend/app/main.py에 추가:
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("kbeauty")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(
    "/var/log/kbeauty/app.log",
    maxBytes=10485760,  # 10MB
    backupCount=10
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
```

### 8.2 Nginx 로깅

```bash
✅ 작업: Nginx 로그 확인

# 액세스 로그
sudo tail -f /var/log/nginx/access.log

# 에러 로그
sudo tail -f /var/log/nginx/error.log

# 로그 로테이션 설정 (자동으로 설정됨)
cat /etc/logrotate.d/nginx
```

### 8.3 데이터베이스 모니터링

```bash
✅ 작업: PostgreSQL 모니터링

# 활성 커넥션 확인
psql -h kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com \
     -U kbeauty_admin \
     -d kbeauty_db \
     -c "SELECT count(*) FROM pg_stat_activity;"

# 느린 쿼리 확인
psql -h kbeauty-db-prod.xxxx.ap-northeast-2.rds.amazonaws.com \
     -U kbeauty_admin \
     -d kbeauty_db \
     -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query 
         FROM pg_stat_activity 
         WHERE (now() - pg_stat_activity.query_start) > interval '5 seconds';"
```

### 8.4 서버 리소스 모니터링

```bash
✅ 작업: 시스템 리소스 모니터링

# 1. htop 설치 (실시간 모니터링)
sudo apt install -y htop
htop

# 2. 디스크 사용량
df -h

# 3. 메모리 사용량
free -h

# 4. CPU 사용량
top

# 5. 네트워크 트래픽
sudo apt install -y iftop
sudo iftop
```

### 8.5 애플리케이션 헬스 체크

```bash
✅ 작업: 헬스 체크 엔드포인트 추가

# backend/app/api/endpoints/health.py 생성
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "0.1.0"
    }

@router.get("/health/detailed")
def detailed_health():
    # DB 연결 확인
    # Redis 연결 확인
    # 등등
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected",
        "version": "0.1.0"
    }

# 등록: backend/app/main.py
app.include_router(health_router, prefix="/api/v1")

# 테스트
curl https://api.beautyinsightlab.com/api/v1/health
```

### 8.6 외부 모니터링 서비스 (선택)

**UptimeRobot (무료 모니터링)**:
```
✅ 작업: UptimeRobot 설정

1. https://uptimerobot.com 가입
2. New Monitor 추가
   - Type: HTTP(s)
   - URL: https://api.beautyinsightlab.com/api/v1/health
   - Monitoring Interval: 5 minutes
   - Alert Contacts: 이메일 등록

3. 프론트엔드 모니터 추가
   - URL: https://www.beautyinsightlab.com
   - Interval: 5 minutes

4. 다운타임 시 자동 알림 수신
```

---

## 9. 성능 최적화

### 9.1 백엔드 최적화

```bash
✅ 작업: Uvicorn 워커 수 조정

# /etc/systemd/system/kbeauty-backend.service 수정
ExecStart=/var/www/kbeauty-backend/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \  # CPU 코어 수에 맞춤 (권장: 코어 수 × 2)
    --worker-class uvicorn.workers.UvicornWorker

sudo systemctl daemon-reload
sudo systemctl restart kbeauty-backend
```

### 9.2 Nginx 캐싱

```nginx
✅ 작업: Nginx 정적 파일 캐싱

# /etc/nginx/sites-available/api.beautyinsightlab.com에 추가

http {
    # 캐시 경로 설정
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=1g inactive=60m use_temp_path=off;
}

server {
    # ... 기존 설정 ...

    # 정적 파일 캐싱
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API 응답 캐싱 (GET 요청만)
    location /api/v1/ {
        proxy_cache api_cache;
        proxy_cache_valid 200 10m;
        proxy_cache_use_stale error timeout updating http_500 http_502 http_503 http_504;
        add_header X-Cache-Status $upstream_cache_status;
        
        proxy_pass http://localhost:8000;
        # ... 기존 proxy 설정 ...
    }
}

sudo nginx -t
sudo systemctl restart nginx
```

### 9.3 데이터베이스 쿼리 최적화

```sql
✅ 작업: 인덱스 추가

-- users 테이블
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_instagram_user_id ON users(instagram_user_id);

-- instagram_posts 테이블
CREATE INDEX idx_instagram_posts_timestamp ON instagram_posts(timestamp DESC);
CREATE INDEX idx_instagram_posts_hashtags ON instagram_posts USING GIN(hashtags);

-- ai_analysis_results 테이블
CREATE INDEX idx_analysis_user_id ON ai_analysis_results(user_id);
CREATE INDEX idx_analysis_created_at ON ai_analysis_results(created_at DESC);

-- 쿼리 성능 확인
EXPLAIN ANALYZE SELECT * FROM instagram_posts WHERE hashtags @> ARRAY['kbeauty'];
```

### 9.4 Redis 캐시 설정 확인

```bash
✅ 작업: Redis 캐시 히트율 확인

redis-cli INFO stats | grep keyspace
# keyspace_hits, keyspace_misses 확인

# 목표: 70%+ 히트율
# Hit Rate = hits / (hits + misses)
```

### 9.5 CDN 설정 (프론트엔드)

```
✅ 작업: Vercel CDN (자동 설정됨)

Vercel은 자동으로 글로벌 CDN을 제공합니다.

확인:
1. www.beautyinsightlab.com 접속
2. 개발자 도구 → Network 탭
3. Response Headers 확인:
   - X-Vercel-Cache: HIT (캐시됨)
   - X-Vercel-ID: ...

추가 최적화:
- next.config.js에서 이미지 최적화 설정
- Static Generation 활용 (getStaticProps)
```

---

## 10. 보안 설정

### 10.1 방화벽 설정

```bash
✅ 작업: UFW 방화벽 설정

# 1. UFW 설치 확인
sudo apt install -y ufw

# 2. 기본 정책 설정
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. 필요한 포트만 허용
sudo ufw allow 22/tcp   # SSH (본인 IP만 허용 권장)
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS

# 4. 특정 IP에서만 SSH 허용 (권장)
sudo ufw delete allow 22/tcp
sudo ufw allow from YOUR_IP_ADDRESS to any port 22

# 5. UFW 활성화
sudo ufw enable

# 6. 상태 확인
sudo ufw status verbose
```

### 10.2 Fail2Ban 설치 (SSH 무차별 대입 공격 방어)

```bash
✅ 작업: Fail2Ban 설치 및 설정

# 1. 설치
sudo apt install -y fail2ban

# 2. 설정 파일 복사
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# 3. SSH 보호 설정
sudo nano /etc/fail2ban/jail.local

# 수정 내용:
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600  # 1시간 차단

# 4. 서비스 시작
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# 5. 상태 확인
sudo fail2ban-client status sshd
```

### 10.3 보안 헤더 설정

```nginx
✅ 작업: Nginx 보안 헤더 추가

# /etc/nginx/sites-available/api.beautyinsightlab.com에 추가

server {
    # ... 기존 설정 ...

    # 보안 헤더
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # ... 기존 설정 ...
}

sudo nginx -t
sudo systemctl restart nginx
```

### 10.4 비밀번호 및 시크릿 관리

```
✅ 작업: 강력한 비밀번호 생성 및 관리

# 강력한 비밀번호 생성
openssl rand -base64 32

# 비밀번호 저장 위치:
1. AWS Secrets Manager (권장, 프로덕션)
2. .env 파일 (개발, chmod 600)
3. 비밀번호 관리자 (1Password, LastPass)

# 절대 하지 말 것:
❌ Git에 커밋
❌ 평문으로 이메일 전송
❌ 팀 채팅에 공유
```

### 10.5 API 레이트 리미팅

```python
✅ 작업: API 요청 제한 설정

# backend/app/main.py에 추가
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# API 엔드포인트에 적용
@router.post("/sentiment")
@limiter.limit("10/minute")  # 분당 10 요청
async def analyze_sentiment(request: Request, ...):
    # ...
```

---

## 11. 테스팅 및 검증

### 11.1 백엔드 API 테스트

```bash
✅ 작업: API 엔드포인트 테스트

# 1. 헬스 체크
curl https://api.beautyinsightlab.com/api/v1/health
# 예상: {"status":"healthy","version":"0.1.0"}

# 2. 회원가입 테스트
curl -X POST https://api.beautyinsightlab.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123","full_name":"Test User"}'

# 3. 로그인 테스트
curl -X POST https://api.beautyinsightlab.com/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpass123"

# 4. 보호된 엔드포인트 테스트
TOKEN="your_jwt_token_here"
curl https://api.beautyinsightlab.com/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"

# 5. AI 분석 테스트
curl -X POST https://api.beautyinsightlab.com/api/v1/ai/sentiment \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"market":"DE","hashtags":["#kbeauty"],"sample_size":10}'
```

### 11.2 프론트엔드 기능 테스트

```
✅ 작업: 프론트엔드 사용자 시나리오 테스트

테스트 시나리오:
1. 회원가입
   - https://www.beautyinsightlab.com/signup 접속
   - 이메일, 비밀번호 입력
   - 성공 시 대시보드로 리다이렉트 확인

2. 로그인
   - https://www.beautyinsightlab.com/login 접속
   - 등록한 이메일/비밀번호로 로그인
   - JWT 토큰 localStorage 저장 확인 (개발자 도구)

3. 대시보드 접근
   - 로그인 후 대시보드 자동 이동 확인
   - 사용자 이름 표시 확인

4. 감성 분석 기능
   - 시장 선택 (Germany)
   - 해시태그 입력 (#kbeauty)
   - "Run Analysis" 클릭
   - 결과 표시 확인 (sentiment score, key themes)

5. 로그아웃
   - 로그아웃 버튼 클릭
   - 로그인 페이지로 리다이렉트 확인
   - localStorage 토큰 삭제 확인
```

### 11.3 성능 테스트

```bash
✅ 작업: 부하 테스트 (Apache Bench)

# 1. Apache Bench 설치
sudo apt install -y apache2-utils

# 2. 간단한 부하 테스트
ab -n 1000 -c 10 https://api.beautyinsightlab.com/api/v1/health
# -n 1000: 총 1000 요청
# -c 10: 동시 10 연결

# 3. 결과 분석:
# - Requests per second: 목표 100+ RPS
# - Time per request: 목표 <100ms
# - Failed requests: 0

# 4. 더 강력한 부하 테스트 도구 (선택)
# - Locust: Python 기반
# - k6: JavaScript 기반
# - JMeter: Java 기반
```

### 11.4 브라우저 호환성 테스트

```
✅ 작업: 다양한 브라우저에서 테스트

테스트 브라우저:
1. Chrome (최신 버전)
2. Firefox (최신 버전)
3. Safari (macOS/iOS)
4. Edge (최신 버전)

체크 포인트:
- 레이아웃 깨짐 없음
- 기능 정상 작동
- 콘솔 에러 없음
- 반응형 디자인 (모바일, 태블릿)
```

### 11.5 보안 취약점 스캔

```bash
✅ 작업: 보안 스캔

# 1. SSL Labs 테스트
https://www.ssllabs.com/ssltest/analyze.html?d=api.beautyinsightlab.com
# 목표: A 등급

# 2. Security Headers 테스트
https://securityheaders.com/?q=https://api.beautyinsightlab.com
# 목표: A 등급

# 3. OWASP ZAP (취약점 스캐너)
# 로컬에 설치 후 실행
# https://www.zaproxy.org/

# 4. Dependabot (GitHub)
# 자동으로 의존성 취약점 확인
# GitHub → Settings → Security → Dependabot alerts 활성화
```

---

## 12. 런치 준비

### 12.1 런치 체크리스트

```
✅ 최종 런치 전 체크리스트

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
항목                              상태     확인일
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. 도메인 설정
   □ DNS A/CNAME 레코드 설정        [ ]    ______
   □ DNS 전파 완료                  [ ]    ______
   □ www와 apex 모두 작동           [ ]    ______

2. SSL/HTTPS
   □ 프론트엔드 SSL 인증서 발급     [ ]    ______
   □ 백엔드 SSL 인증서 발급         [ ]    ______
   □ HTTP → HTTPS 리다이렉트        [ ]    ______
   □ SSL Labs 테스트 A 등급         [ ]    ______

3. 백엔드 배포
   □ EC2 인스턴스 실행 중           [ ]    ______
   □ PostgreSQL 연결 정상           [ ]    ______
   □ Redis 연결 정상                [ ]    ______
   □ API 엔드포인트 모두 작동       [ ]    ______
   □ Systemd 서비스 자동 시작       [ ]    ______
   □ Nginx 프록시 설정 완료         [ ]    ______

4. 프론트엔드 배포
   □ Vercel 배포 성공               [ ]    ______
   □ 커스텀 도메인 연결 완료        [ ]    ______
   □ 환경 변수 설정 완료            [ ]    ______
   □ 모든 페이지 로드 확인          [ ]    ______

5. 데이터베이스
   □ 프로덕션 DB 생성 완료          [ ]    ______
   □ 마이그레이션 적용 완료         [ ]    ______
   □ 백업 설정 완료                 [ ]    ______
   □ 연결 풀 설정 확인              [ ]    ______

6. 보안
   □ 방화벽 설정 (UFW)              [ ]    ______
   □ Fail2Ban 설치 및 설정          [ ]    ______
   □ 환경 변수 파일 권한 (600)      [ ]    ______
   □ 보안 헤더 설정                 [ ]    ______
   □ API 레이트 리미팅 설정         [ ]    ______

7. 모니터링
   □ 헬스 체크 엔드포인트 작동      [ ]    ______
   □ 로깅 설정 완료                 [ ]    ______
   □ UptimeRobot 설정               [ ]    ______
   □ 알림 이메일 등록               [ ]    ______

8. 테스팅
   □ API 엔드포인트 테스트          [ ]    ______
   □ 프론트엔드 시나리오 테스트     [ ]    ______
   □ 부하 테스트 (100+ RPS)         [ ]    ______
   □ 브라우저 호환성 테스트         [ ]    ______
   □ 모바일 반응형 확인             [ ]    ______

9. 성능
   □ API 응답 시간 <3s              [ ]    ______
   □ 페이지 로드 시간 <2s           [ ]    ______
   □ Redis 캐시 히트율 >70%         [ ]    ______
   □ 이미지 최적화 완료             [ ]    ______

10. 문서화
    □ API 문서 (Swagger) 접근 가능   [ ]    ______
    □ 사용자 가이드 준비             [ ]    ______
    □ FAQ 페이지 작성                [ ]    ______
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 12.2 롤백 계획

```
✅ 비상 롤백 계획

문제 발생 시:

1. 프론트엔드 롤백 (Vercel):
   - Vercel Dashboard → Deployments
   - 이전 버전 선택 → "Promote to Production"

2. 백엔드 롤백 (Git):
   cd /var/www/kbeauty-backend
   git log --oneline  # 이전 커밋 확인
   git checkout <previous-commit-hash>
   ./deploy.sh

3. 데이터베이스 롤백 (Alembic):
   alembic downgrade -1  # 한 단계 이전으로
   alembic downgrade <revision>  # 특정 리비전으로

4. 긴급 연락처:
   - CEO: +82-10-XXXX-XXXX
   - 개발자: +82-10-YYYY-YYYY
   - AWS Support: (프리미엄 플랜 가입 시)
```

### 12.3 런치 공지

```
✅ 작업: 런치 준비 공지

1. 내부 팀:
   - 런치 날짜/시간 공유
   - 역할 분담 확인
   - 비상 연락망 공유

2. 파일럿 고객:
   - 이메일 발송 (런치 1주일 전)
   - 새 도메인 안내: www.beautyinsightlab.com
   - 계정 마이그레이션 안내 (필요 시)

3. 소셜 미디어:
   - LinkedIn 포스팅 준비
   - 프레스 릴리스 작성 (선택)

4. 모니터링 체제:
   - 런치 당일 실시간 모니터링
   - 에러 알림 활성화
   - 빠른 대응 체계 구축
```

---

## 📊 예상 일정 및 비용

### 일정 (3주)

```
Week 1: 인프라 구축
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 1-2: 도메인 DNS 설정, 호스팅 환경 선택 및 구성
Day 3-4: 백엔드 배포 (EC2, PostgreSQL, Redis)
Day 5: 프론트엔드 배포 (Vercel)
Day 6-7: SSL 인증서, 환경 변수 설정

Week 2: 최적화 및 보안
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 8-9: 성능 최적화 (캐싱, CDN)
Day 10-11: 보안 설정 (방화벽, Fail2Ban, 보안 헤더)
Day 12-13: 모니터링 및 로깅 설정
Day 14: 백업 시스템 구축

Week 3: 테스팅 및 런치
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Day 15-16: 전체 기능 테스트
Day 17-18: 부하 테스트, 보안 스캔
Day 19: 최종 체크리스트 확인
Day 20-21: 소프트 런치, 모니터링

🚀 Day 21: 공식 런치
```

### 예상 비용 (월간)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
항목                       비용 (USD)      비고
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
도메인 (beautyinsightlab.com)
  - 가비아 .com 도메인      $12/year      이미 구매 완료

프론트엔드 호스팅
  - Vercel (Hobby)          $0            무료 티어
  - 또는 Vercel Pro         $20           선택

백엔드 호스팅
  - AWS EC2 t3.medium       $45           한국 리전
  - 또는 Lightsail          $20           (대안)

데이터베이스
  - AWS RDS t3.small        $30           관리형
  - 또는 EC2 내장           $0            (대안)

캐시 (Redis)
  - EC2 내장                $0            포함

SSL 인증서
  - Let's Encrypt           $0            무료

CDN
  - Vercel CDN              $0            포함
  - Cloudflare              $0            (선택)

모니터링
  - UptimeRobot             $0            무료 티어

AI API 비용
  - OpenAI GPT-4            $500-1,000    사용량 기반
  - (캐싱으로 70% 절감)     $150-300      최적화 후

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
월 총 비용 (최소)           $225-355
월 총 비용 (권장)           $245-375
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

연간 비용 (12개월):         ~$2,700-4,500
```

---

## 🆘 문제 해결 (Troubleshooting)

### 일반적인 문제

#### 1. DNS가 전파되지 않음
```
문제: www.beautyinsightlab.com에 접속되지 않음

해결:
1. DNS 설정 재확인 (가비아 DNS 관리)
2. 전파 시간 대기 (최대 48시간)
3. DNS 캐시 초기화:
   - Windows: ipconfig /flushdns
   - Mac: sudo dscacheutil -flushcache
4. 다른 네트워크에서 시도 (모바일 데이터 등)
```

#### 2. SSL 인증서 에러
```
문제: "Your connection is not private" 에러

해결:
1. Certbot 재실행: sudo certbot --nginx -d api.beautyinsightlab.com
2. Nginx 설정 확인: sudo nginx -t
3. 인증서 파일 권한 확인: ls -l /etc/letsencrypt/live/
4. 80 포트 열림 확인: sudo ufw status
```

#### 3. 백엔드 API 500 에러
```
문제: API 호출 시 500 Internal Server Error

해결:
1. 로그 확인: sudo journalctl -u kbeauty-backend -n 100
2. 데이터베이스 연결 확인: psql -h ... -U kbeauty_admin
3. 환경 변수 확인: .env 파일 존재 및 권한
4. 서비스 재시작: sudo systemctl restart kbeauty-backend
```

#### 4. CORS 에러
```
문제: 프론트엔드에서 API 호출 시 CORS 에러

해결:
1. backend/.env의 BACKEND_CORS_ORIGINS 확인
2. 프론트엔드 도메인 추가:
   BACKEND_CORS_ORIGINS=["https://www.beautyinsightlab.com","https://beautyinsightlab.com"]
3. 백엔드 재시작
```

#### 5. 데이터베이스 연결 실패
```
문제: "Could not connect to database"

해결:
1. PostgreSQL 상태 확인: sudo systemctl status postgresql
2. 방화벽 규칙 확인: sudo ufw status
3. pg_hba.conf 확인: 연결 허용 설정
4. DATABASE_URL 형식 확인: postgresql://user:pass@host:5432/db
```

---

## 📞 지원 및 연락처

**기술 지원**:
- Email: tech@beautyinsightlab.com
- GitHub Issues: https://github.com/howl-papa/k-beauty-global-leap/issues

**AWS 지원**:
- AWS Support Center (Basic Plan)
- https://console.aws.amazon.com/support/

**Vercel 지원**:
- Vercel Support: https://vercel.com/support
- Community: https://github.com/vercel/vercel/discussions

---

**문서 버전**: 1.0  
**최종 업데이트**: 2024년 10월 28일  
**작성자**: Beauty Insight Lab Development Team

---

## ✅ 다음 단계

배포 완료 후:
1. ✅ 파일럿 고객 5명 온보딩
2. ✅ 피드백 수집 및 개선
3. ✅ 마케팅 캠페인 시작
4. ✅ Series A 투자 유치 준비

**Good Luck with the Launch! 🚀**
