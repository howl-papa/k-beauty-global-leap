# System Architecture Overview

## K-Beauty Global Leap Platform Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend Layer                       │
│              (Next.js 14 + TypeScript + Tailwind)           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                     │
│                      (FastAPI + Uvicorn)                     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────┬───────────────┬─────────────────────┐
│  Market Intelligence │   Cultural    │   Partner           │
│       Service        │  Adaptation   │  Verification       │
│                      │    Engine     │    Network          │
└──────────────────────┴───────────────┴─────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                         AI/ML Layer                          │
│        (GPT-4, Claude, LangChain, LlamaIndex, Pinecone)     │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────┬────────────────┬──────────────────────┐
│   PostgreSQL     │     Redis      │   External APIs      │
│   (Primary DB)   │   (Caching)    │ (Social Media, etc)  │
└──────────────────┴────────────────┴──────────────────────┘
```

## Core Components

### 1. Frontend Layer
- **Technology**: Next.js 14 with App Router
- **State Management**: Zustand + SWR
- **UI Components**: Custom components with Tailwind CSS
- **Features**:
  - Server-side rendering for SEO
  - Real-time dashboard updates
  - Responsive design for mobile/desktop
  - Progressive Web App capabilities

### 2. API Gateway
- **Technology**: FastAPI with async support
- **Features**:
  - RESTful API endpoints
  - WebSocket support for real-time updates
  - JWT-based authentication
  - Rate limiting and request validation
  - Automatic API documentation (Swagger/OpenAPI)

### 3. Core Services

#### Market Intelligence Hub
- Real-time social media data collection
- Trend analysis using NLP
- Competitor monitoring
- Market entry scoring algorithms

#### Cultural Adaptation Engine
- AI-powered transcreation
- Cultural context analysis using RAG
- Visual localization recommendations
- Taboo detection and avoidance

#### Partner Verification Network
- Credibility assessment algorithms
- Influencer audience analysis
- Distributor performance tracking
- Contract risk detection

#### ROI Optimization Dashboard
- Campaign performance tracking
- Budget allocation optimization
- A/B testing framework
- Predictive analytics

### 4. AI/ML Layer
- **OpenAI GPT-4**: Content generation and analysis
- **Anthropic Claude**: Advanced reasoning tasks
- **LangChain**: Orchestration of LLM workflows
- **LlamaIndex**: RAG implementation for cultural knowledge
- **Pinecone**: Vector database for semantic search

### 5. Data Layer
- **PostgreSQL**: Primary relational database
  - User management
  - Market data
  - Campaign analytics
- **Redis**: Caching and session management
  - API response caching
  - Real-time data storage
  - Job queue for Celery

## Data Flow

### Example: Market Analysis Request

```
1. User Request → Frontend
2. Frontend → API Gateway (GET /api/v1/market-analysis/{country})
3. API Gateway → Market Intelligence Service
4. Service → AI/ML Layer (GPT-4 + RAG)
5. Service → External APIs (Social Media Data)
6. Service → PostgreSQL (Store Results)
7. Service → Redis (Cache Results)
8. API Gateway ← Service (JSON Response)
9. Frontend ← API Gateway (Display Results)
```

## Security Architecture

### Authentication Flow
```
1. User Login → API Gateway
2. Validate Credentials → PostgreSQL
3. Generate JWT Token
4. Return Token to Client
5. Store Token in HTTP-only Cookie
6. Subsequent Requests Include Token
7. API Gateway Validates Token
8. Access Granted to Protected Resources
```

### Security Measures
- JWT-based authentication
- Password hashing with bcrypt
- HTTPS-only in production
- CORS configuration
- Rate limiting per user/IP
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- CSRF token validation

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Load balancing with nginx
- Database read replicas
- Redis clustering for caching

### Vertical Scaling
- Connection pooling for database
- Async processing with Celery
- Caching strategies at multiple levels
- CDN for static assets

## Monitoring & Observability

### Metrics
- API response times
- Error rates
- Database query performance
- AI/ML model latency

### Logging
- Structured logging with Structlog
- Centralized log aggregation
- Error tracking with Sentry

### Health Checks
- `/health` endpoint for each service
- Database connectivity checks
- External API availability checks

## Deployment Architecture

### Development
- Docker Compose for local development
- Hot reloading for rapid development
- Local PostgreSQL and Redis instances

### Production
- Containerized deployment with Docker
- Backend on Railway/Render
- Frontend on Vercel
- PostgreSQL on managed service
- Redis on managed service

## Future Enhancements

1. **Microservices Architecture**: Split monolithic backend into microservices
2. **Message Queue**: RabbitMQ/Kafka for event-driven architecture
3. **GraphQL API**: Add GraphQL layer for flexible queries
4. **Real-time Collaboration**: WebSocket-based collaborative features
5. **Mobile Apps**: React Native for iOS/Android
