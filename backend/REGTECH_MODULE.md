# 🔬 RegTech Module - Cosmetic Regulatory Compliance

## Overview

The RegTech (Regulatory Technology) module is an AI-powered compliance analysis system for cosmetic products. It helps K-Beauty SMEs ensure their products meet international regulatory requirements before entering foreign markets.

## Key Features

### 🎯 Core Capabilities

1. **Ingredient Compliance Analysis**
   - Automated checking against prohibited/restricted ingredient databases
   - Support for FDA MoCRA (US), EU CPNP, and ASEAN regulations
   - Real-time ingredient validation

2. **AI-Powered Insights**
   - GPT-4 integration for contextual regulatory analysis
   - Natural language recommendations and warnings
   - Risk assessment and scoring

3. **Multi-Market Support**
   - United States (FDA MoCRA)
   - European Union (CPNP - Cosmetic Products Notification Portal)
   - ASEAN countries (Thailand, Singapore, Malaysia, Indonesia, Vietnam)

4. **Compliance Dashboard**
   - Real-time compliance scoring (0-100)
   - Risk level categorization (LOW, MEDIUM, HIGH, CRITICAL)
   - Historical analysis tracking

## Technical Architecture

### Database Models

#### 1. **RegulationDocument**
Stores regulation documents and guidelines from various markets.

```python
- regulation_type: FDA_MOCRA | EU_CPNP | ASEAN | OTHER
- country_code: ISO country code (US, EU, TH, etc.)
- title: Document title
- document_content: Full text content
- source_url: Official source URL
```

#### 2. **ProhibitedIngredient**
Database of prohibited and restricted cosmetic ingredients.

```python
- ingredient_name: Common name
- cas_number: Chemical Abstracts Service number
- inci_name: International Nomenclature Cosmetic Ingredient
- status: PROHIBITED | RESTRICTED | ALLOWED_WITH_LIMITS
- max_concentration: Maximum allowed concentration
- hazard_category: Risk classification
- alternative_ingredients: Suggested alternatives
```

#### 3. **ProductAnalysis**
Stores compliance analysis results for user products.

```python
- product_name: Name of the product
- ingredients_list: Array of ingredients
- compliance_status: COMPLIANT | WARNING | NON_COMPLIANT | PENDING
- compliance_score: 0-100 score
- risk_level: LOW | MEDIUM | HIGH | CRITICAL
- prohibited_ingredients_found: Detected prohibited ingredients
- restricted_ingredients_found: Detected restricted ingredients
- ai_analysis_summary: GPT-4 generated insights
```

#### 4. **ComplianceAlert**
Tracks regulation changes and updates.

```python
- title: Alert title
- description: Alert description
- severity: Risk level
- affected_ingredients: List of affected ingredients
- effective_date: When the regulation takes effect
```

### API Endpoints

#### POST `/api/v1/regtech/analyze`
Analyze a product for regulatory compliance.

**Request:**
```json
{
  "product_name": "Hydrating Face Serum",
  "product_category": "Skincare",
  "brand_name": "K-Beauty Labs",
  "target_country": "US",
  "ingredients_list": [
    "Water",
    "Glycerin",
    "Hyaluronic Acid",
    "Niacinamide",
    "Panthenol"
  ]
}
```

**Response:**
```json
{
  "id": 1,
  "product_name": "Hydrating Face Serum",
  "target_country": "US",
  "regulation_type": "FDA_MOCRA",
  "compliance_status": "COMPLIANT",
  "compliance_score": 100.0,
  "risk_level": "LOW",
  "prohibited_ingredients_found": [],
  "restricted_ingredients_found": [],
  "warnings": [
    "✅ No prohibited or restricted ingredients detected."
  ],
  "recommendations": [
    "Product appears compliant with FDA MoCRA requirements."
  ],
  "ai_analysis_summary": "...",
  "created_at": "2025-10-31T15:00:00"
}
```

#### GET `/api/v1/regtech/analyses`
Get all analyses for the current user.

#### GET `/api/v1/regtech/analyses/{analysis_id}`
Get specific analysis by ID.

#### GET `/api/v1/regtech/statistics`
Get compliance statistics for dashboard.

**Response:**
```json
{
  "total_analyses": 15,
  "compliant_count": 10,
  "warning_count": 3,
  "non_compliant_count": 2,
  "average_compliance_score": 87.5,
  "recent_analyses": [...]
}
```

#### DELETE `/api/v1/regtech/analyses/{analysis_id}`
Delete an analysis.

## Usage Examples

### Basic Compliance Check

```python
import requests

# Analyze a product
response = requests.post(
    "http://localhost:8000/api/v1/regtech/analyze",
    json={
        "product_name": "Anti-Aging Night Cream",
        "product_category": "Skincare",
        "target_country": "EU",
        "ingredients_list": [
            "Aqua",
            "Glycerin",
            "Retinol",
            "Hyaluronic Acid",
            "Vitamin E"
        ]
    },
    headers={"Authorization": f"Bearer {access_token}"}
)

result = response.json()
print(f"Compliance Score: {result['compliance_score']}")
print(f"Risk Level: {result['risk_level']}")
```

### Check Analysis History

```python
# Get all analyses
response = requests.get(
    "http://localhost:8000/api/v1/regtech/analyses",
    headers={"Authorization": f"Bearer {access_token}"}
)

analyses = response.json()
for analysis in analyses:
    print(f"{analysis['product_name']}: {analysis['compliance_status']}")
```

## Compliance Scoring Algorithm

### Score Calculation

```
Base Score: 100

Penalties:
- Prohibited ingredient: -30 points each
- Restricted ingredient: -10 points each

Final Score: max(0, min(100, Base Score - Total Penalties))
```

### Risk Level Determination

| Condition | Risk Level |
|-----------|------------|
| 3+ prohibited ingredients | CRITICAL |
| 1+ prohibited ingredients | HIGH |
| 5+ restricted ingredients | HIGH |
| 2+ restricted ingredients | MEDIUM |
| Otherwise | LOW |

### Compliance Status

| Condition | Status |
|-----------|--------|
| Any prohibited ingredients | NON_COMPLIANT |
| Any restricted ingredients | WARNING |
| Score ≥ 95 | COMPLIANT |
| Otherwise | WARNING |

## AI Integration

### GPT-4 Analysis

The module uses OpenAI's GPT-4 to provide:
- Contextual regulatory insights
- Reformulation recommendations
- Market-specific considerations
- Risk assessment narratives

**Configuration:**
Set `OPENAI_API_KEY` in your `.env` file to enable AI analysis.

```bash
OPENAI_API_KEY=sk-your-api-key-here
```

## Database Setup

### 1. Run Migrations

```bash
cd backend
alembic upgrade head
```

### 2. Seed Sample Data

```bash
cd backend
python scripts/seed_regtech_data.py
```

This will populate the database with:
- 13 sample prohibited/restricted ingredients
- Covering US, EU, and ASEAN markets
- Common ingredients like Hydroquinone, Mercury, Parabens, etc.

## Testing

### Test with Sample Product

```bash
curl -X POST "http://localhost:8000/api/v1/regtech/analyze" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Test Serum",
    "target_country": "US",
    "ingredients_list": ["Water", "Glycerin", "Mercury compounds"]
  }'
```

Expected response: NON_COMPLIANT status due to mercury.

## Supported Regulations

### 1. FDA MoCRA (United States)
- **Effective:** December 2022
- **Key Requirements:**
  - Facility registration
  - Product listing
  - Adverse event reporting
  - Ingredient restrictions

### 2. EU CPNP (European Union)
- **Regulation:** EC No 1223/2009
- **Key Requirements:**
  - CPNP notification
  - Cosmetic Product Safety Report (CPSR)
  - Responsible Person (RP) designation
  - Strict ingredient bans

### 3. ASEAN Cosmetic Directive
- **Coverage:** Thailand, Singapore, Malaysia, Indonesia, Vietnam, Philippines
- **Key Requirements:**
  - Country-specific notifications
  - Harmonized ingredient restrictions
  - Local distributor requirements

## Future Enhancements

### Roadmap

- [ ] **Automated Regulation Crawling**
  - Real-time monitoring of FDA, EU Commission, ASEAN websites
  - Automatic database updates when regulations change

- [ ] **PDF Report Generation**
  - Professional compliance reports
  - Export to PDF with branding

- [ ] **Regulation Alerts**
  - Email/SMS notifications for regulation changes
  - Subscription to specific markets

- [ ] **Multi-Language Support**
  - Analyze products in Korean, English, Chinese, Japanese
  - Localized recommendations

- [ ] **Batch Analysis**
  - Upload multiple products via CSV/Excel
  - Bulk compliance checking

- [ ] **Integration with ERP Systems**
  - API for enterprise systems
  - Webhook notifications

## Contributing

Contributions are welcome! Areas for improvement:

1. **Regulation Data**
   - Add more prohibited/restricted ingredients
   - Update regulation documents
   - Add more markets (China, Japan, Australia, etc.)

2. **AI Improvements**
   - Fine-tune prompts for better insights
   - Add support for Claude, Gemini models
   - Implement RAG for regulation documents

3. **Features**
   - Implement PDF report generation
   - Add real-time regulation monitoring
   - Build mobile app

## License

MIT License - see LICENSE file for details.

## Support

For questions or issues:
- 📧 Email: support@beautyinsightlab.com
- 🌐 Website: http://www.beautyinsightlab.com
- 📚 Documentation: http://localhost:8000/docs

---

**Built with ❤️ for K-Beauty SMEs going global**
