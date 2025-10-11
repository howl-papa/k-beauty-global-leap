# K-Beauty Tech Blog

AI, 기술, 그리고 K-Beauty 산업의 교차점에서 얻은 통찰을 공유하는 기술 블로그입니다. 본 저장소는 Jekyll 기반으로 구축되었으며, K-Beauty Global Leap 프로젝트의 진행 상황과 기술적 연구를 기록합니다.

## 🚀 주요 특징

- **커스텀 Jekyll 테마**: Inter & JetBrains Mono 타이포그래피, 맞춤형 컬러 팔레트 적용
- **카테고리/태그 아카이브**: 프로젝트별, 주제별 콘텐츠 탐색 지원
- **SEO 최적화**: Open Graph, Twitter 카드, JSON-LD 메타데이터 자동 생성
- **CI/CD 파이프라인**: GitHub Actions를 활용한 자동 빌드 및 GitHub Pages 배포

## 📁 디렉토리 구조

```
k-beauty-tech-blog/
├── _config.yml
├── _includes/
├── _layouts/
├── _plugins/
├── _posts/
├── assets/
├── case-studies/
├── projects/
├── .github/workflows/
├── Gemfile
└── README.md
```

## 🛠 로컬 개발 방법

```bash
bundle install
bundle exec jekyll serve
```

로컬 서버는 `http://127.0.0.1:4000`에서 확인할 수 있습니다.

## 📦 배포

메인 브랜치에 푸시하면 GitHub Actions 워크플로우가 자동으로 빌드 및 Pages 배포를 수행합니다. `GITHUB_TOKEN`은 기본 제공되는 시크릿을 사용합니다.

## ✍️ 콘텐츠 카테고리

- **Development**: 주간 개발 일지와 아키텍처 결정 사항
- **AI Insights**: RAG, LLM, 문화적 현지화 등 AI 관련 기술 분석
- **Case Studies**: 파트너사와의 협업 사례 및 성과 공유

## 📬 문의

- Email: [contact@yongrak.pro](mailto:contact@yongrak.pro)
- LinkedIn: [yongrak-pro](https://linkedin.com/in/yongrak-pro)
- GitHub: [howl-papa](https://github.com/howl-papa)
