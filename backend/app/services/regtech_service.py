"""
RegTech Service - Cosmetic Regulation Compliance Analysis

This service provides AI-powered compliance checking for cosmetic products
against various international regulations (FDA MoCRA, EU CPNP, ASEAN, etc.)
"""

from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from openai import OpenAI
import json
import re

from app.models.regulation import ProhibitedIngredient, RegulationType
from app.models.product_compliance import (
    ProductAnalysis, 
    ComplianceStatus, 
    RiskLevel
)
from app.schemas.regtech import (
    ProductAnalysisRequest,
    IngredientFinding
)
from app.core.config import settings


class RegTechService:
    """Service for RegTech compliance analysis"""
    
    def __init__(self, db: Session):
        self.db = db
        self.openai_client = None
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def get_regulation_type(self, country_code: str) -> str:
        """Map country code to regulation type"""
        regulation_map = {
            "US": "FDA_MOCRA",
            "EU": "EU_CPNP",
            "DE": "EU_CPNP",
            "FR": "EU_CPNP",
            "IT": "EU_CPNP",
            "ES": "EU_CPNP",
            "UK": "EU_CPNP",
            "TH": "ASEAN",
            "SG": "ASEAN",
            "MY": "ASEAN",
            "ID": "ASEAN",
            "VN": "ASEAN",
        }
        return regulation_map.get(country_code.upper(), "OTHER")
    
    async def analyze_product_compliance(
        self, 
        request: ProductAnalysisRequest,
        user_id: int
    ) -> ProductAnalysis:
        """
        Analyze product compliance against target market regulations
        
        Args:
            request: Product analysis request with ingredients and target market
            user_id: ID of the user requesting the analysis
            
        Returns:
            ProductAnalysis object with compliance results
        """
        regulation_type = self.get_regulation_type(request.target_country)
        
        # Step 1: Check ingredients against prohibited/restricted database
        prohibited_findings, restricted_findings = await self._check_ingredients_database(
            request.ingredients_list,
            regulation_type,
            request.target_country
        )
        
        # Step 2: Use AI to analyze ingredients and provide insights
        ai_analysis = await self._ai_analyze_ingredients(
            request.ingredients_list,
            request.target_country,
            regulation_type,
            prohibited_findings,
            restricted_findings
        )
        
        # Step 3: Calculate compliance score and risk level
        compliance_score, risk_level = self._calculate_compliance_metrics(
            prohibited_findings,
            restricted_findings,
            len(request.ingredients_list)
        )
        
        # Step 4: Determine compliance status
        compliance_status = self._determine_compliance_status(
            prohibited_findings,
            restricted_findings,
            compliance_score
        )
        
        # Step 5: Generate warnings and recommendations
        warnings = self._generate_warnings(prohibited_findings, restricted_findings)
        recommendations = self._generate_recommendations(
            prohibited_findings,
            restricted_findings,
            ai_analysis
        )
        
        # Step 6: Create ProductAnalysis record
        product_analysis = ProductAnalysis(
            user_id=user_id,
            product_name=request.product_name,
            product_category=request.product_category,
            brand_name=request.brand_name,
            target_country=request.target_country,
            regulation_type=regulation_type,
            ingredients_list=request.ingredients_list,
            full_ingredient_text=request.full_ingredient_text,
            compliance_status=compliance_status,
            compliance_score=compliance_score,
            risk_level=risk_level,
            prohibited_ingredients_found=[f.dict() for f in prohibited_findings],
            restricted_ingredients_found=[f.dict() for f in restricted_findings],
            warnings=warnings,
            recommendations=recommendations,
            ai_analysis_summary=ai_analysis.get("summary", ""),
            ai_model_used="gpt-4" if self.openai_client else "rule-based"
        )
        
        self.db.add(product_analysis)
        self.db.commit()
        self.db.refresh(product_analysis)
        
        return product_analysis
    
    async def _check_ingredients_database(
        self,
        ingredients: List[str],
        regulation_type: str,
        country_code: str
    ) -> Tuple[List[IngredientFinding], List[IngredientFinding]]:
        """
        Check ingredients against prohibited/restricted database
        
        Returns:
            Tuple of (prohibited_findings, restricted_findings)
        """
        prohibited_findings = []
        restricted_findings = []
        
        for ingredient in ingredients:
            # Query database for matching ingredients
            db_results = self.db.query(ProhibitedIngredient).filter(
                ProhibitedIngredient.regulation_type == regulation_type,
                ProhibitedIngredient.country_code == country_code,
                ProhibitedIngredient.ingredient_name.ilike(f"%{ingredient}%")
            ).all()
            
            for db_ingredient in db_results:
                finding = IngredientFinding(
                    ingredient_name=db_ingredient.ingredient_name,
                    cas_number=db_ingredient.cas_number,
                    inci_name=db_ingredient.inci_name,
                    status=db_ingredient.status,
                    regulation_type=regulation_type,
                    max_concentration=db_ingredient.max_concentration,
                    restriction_notes=db_ingredient.restriction_notes,
                    hazard_category=db_ingredient.hazard_category,
                    alternatives=db_ingredient.alternative_ingredients
                )
                
                if db_ingredient.status == "PROHIBITED":
                    prohibited_findings.append(finding)
                elif db_ingredient.status in ["RESTRICTED", "ALLOWED_WITH_LIMITS"]:
                    restricted_findings.append(finding)
        
        return prohibited_findings, restricted_findings
    
    async def _ai_analyze_ingredients(
        self,
        ingredients: List[str],
        country_code: str,
        regulation_type: str,
        prohibited_findings: List[IngredientFinding],
        restricted_findings: List[IngredientFinding]
    ) -> Dict[str, Any]:
        """
        Use AI (GPT-4) to analyze ingredients and provide contextual insights
        """
        if not self.openai_client:
            return {
                "summary": "AI analysis unavailable. Please configure OpenAI API key.",
                "detailed_analysis": []
            }
        
        # Prepare prompt for GPT-4
        prompt = f"""
You are an expert cosmetic chemist and regulatory compliance specialist. 
Analyze the following cosmetic product ingredients for compliance with {regulation_type} regulations in {country_code}.

Ingredients: {', '.join(ingredients)}

Prohibited ingredients found: {len(prohibited_findings)}
Restricted ingredients found: {len(restricted_findings)}

Please provide:
1. A brief summary of the overall compliance status (2-3 sentences)
2. Key concerns or risks
3. Specific recommendations for reformulation if needed
4. Any additional regulatory considerations for {country_code}

Format your response as JSON with keys: summary, concerns, recommendations, regulatory_notes
"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a cosmetic regulatory compliance expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as JSON
            try:
                analysis = json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, return raw text
                analysis = {
                    "summary": content[:500],
                    "concerns": [],
                    "recommendations": [],
                    "regulatory_notes": ""
                }
            
            return analysis
            
        except Exception as e:
            print(f"AI analysis error: {str(e)}")
            return {
                "summary": "AI analysis encountered an error. Using rule-based analysis.",
                "concerns": [],
                "recommendations": [],
                "regulatory_notes": ""
            }
    
    def _calculate_compliance_metrics(
        self,
        prohibited_findings: List[IngredientFinding],
        restricted_findings: List[IngredientFinding],
        total_ingredients: int
    ) -> Tuple[float, RiskLevel]:
        """
        Calculate compliance score (0-100) and risk level
        """
        # Base score is 100
        score = 100.0
        
        # Deduct points for prohibited ingredients (severe penalty)
        prohibited_penalty = len(prohibited_findings) * 30
        score -= prohibited_penalty
        
        # Deduct points for restricted ingredients (moderate penalty)
        restricted_penalty = len(restricted_findings) * 10
        score -= restricted_penalty
        
        # Ensure score is within 0-100 range
        score = max(0.0, min(100.0, score))
        
        # Determine risk level based on findings
        if len(prohibited_findings) >= 3:
            risk_level = RiskLevel.CRITICAL
        elif len(prohibited_findings) >= 1:
            risk_level = RiskLevel.HIGH
        elif len(restricted_findings) >= 5:
            risk_level = RiskLevel.HIGH
        elif len(restricted_findings) >= 2:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        return score, risk_level
    
    def _determine_compliance_status(
        self,
        prohibited_findings: List[IngredientFinding],
        restricted_findings: List[IngredientFinding],
        compliance_score: float
    ) -> ComplianceStatus:
        """Determine overall compliance status"""
        if len(prohibited_findings) > 0:
            return ComplianceStatus.NON_COMPLIANT
        elif len(restricted_findings) > 0:
            return ComplianceStatus.WARNING
        elif compliance_score >= 95:
            return ComplianceStatus.COMPLIANT
        else:
            return ComplianceStatus.WARNING
    
    def _generate_warnings(
        self,
        prohibited_findings: List[IngredientFinding],
        restricted_findings: List[IngredientFinding]
    ) -> List[str]:
        """Generate warning messages"""
        warnings = []
        
        if prohibited_findings:
            warnings.append(
                f"⚠️ {len(prohibited_findings)} PROHIBITED ingredient(s) detected. "
                "This product cannot be sold in the target market without reformulation."
            )
        
        if restricted_findings:
            warnings.append(
                f"⚠️ {len(restricted_findings)} RESTRICTED ingredient(s) found. "
                "Please verify concentration limits and usage restrictions."
            )
        
        if not prohibited_findings and not restricted_findings:
            warnings.append("✅ No prohibited or restricted ingredients detected in our database.")
        
        return warnings
    
    def _generate_recommendations(
        self,
        prohibited_findings: List[IngredientFinding],
        restricted_findings: List[IngredientFinding],
        ai_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Add recommendations from AI analysis
        if ai_analysis.get("recommendations"):
            if isinstance(ai_analysis["recommendations"], list):
                recommendations.extend(ai_analysis["recommendations"])
            else:
                recommendations.append(str(ai_analysis["recommendations"]))
        
        # Add specific recommendations for prohibited ingredients
        for finding in prohibited_findings:
            if finding.alternatives:
                alternatives_str = ", ".join(finding.alternatives[:3])
                recommendations.append(
                    f"Replace '{finding.ingredient_name}' with alternatives: {alternatives_str}"
                )
            else:
                recommendations.append(
                    f"Remove '{finding.ingredient_name}' - consult with regulatory expert for alternatives"
                )
        
        # Add recommendations for restricted ingredients
        for finding in restricted_findings:
            if finding.max_concentration:
                recommendations.append(
                    f"Verify '{finding.ingredient_name}' concentration does not exceed {finding.max_concentration}"
                )
        
        # Add general recommendation if none exist
        if not recommendations:
            recommendations.append(
                "Consider consulting with a regulatory expert to verify all compliance requirements."
            )
        
        return recommendations
    
    def get_user_analyses(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[ProductAnalysis]:
        """Get all analyses for a user"""
        return self.db.query(ProductAnalysis).filter(
            ProductAnalysis.user_id == user_id
        ).order_by(
            ProductAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_analysis_by_id(
        self,
        analysis_id: int,
        user_id: int
    ) -> Optional[ProductAnalysis]:
        """Get specific analysis by ID"""
        return self.db.query(ProductAnalysis).filter(
            ProductAnalysis.id == analysis_id,
            ProductAnalysis.user_id == user_id
        ).first()
