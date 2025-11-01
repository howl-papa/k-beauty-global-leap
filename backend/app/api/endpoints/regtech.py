"""
RegTech API Endpoints

API endpoints for cosmetic regulatory compliance analysis
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies.auth import get_current_user
from app.models.user import User
from app.models.product_compliance import ProductAnalysis
from app.schemas.regtech import (
    ProductAnalysisRequest,
    ProductAnalysisResponse,
    ProductAnalysisSummary,
    ComplianceStatistics,
    IngredientFinding
)
from app.services.regtech_service import RegTechService


router = APIRouter(prefix="/regtech", tags=["RegTech"])


@router.post(
    "/analyze",
    response_model=ProductAnalysisResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Analyze Product Compliance",
    description="""
    Analyze a cosmetic product for regulatory compliance.
    
    This endpoint checks product ingredients against international regulations
    (FDA MoCRA, EU CPNP, ASEAN) and provides:
    - Compliance status and score
    - Prohibited/restricted ingredients detection
    - Risk level assessment
    - AI-powered recommendations
    
    **Required**: User authentication
    """
)
async def analyze_product_compliance(
    request: ProductAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Analyze product compliance against target market regulations
    
    **Example Request:**
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
    """
    try:
        service = RegTechService(db)
        analysis = await service.analyze_product_compliance(request, current_user.id)
        
        # Convert to response schema
        return ProductAnalysisResponse(
            id=analysis.id,
            product_name=analysis.product_name,
            product_category=analysis.product_category,
            brand_name=analysis.brand_name,
            target_country=analysis.target_country,
            regulation_type=analysis.regulation_type,
            compliance_status=analysis.compliance_status,
            compliance_score=analysis.compliance_score,
            risk_level=analysis.risk_level,
            prohibited_ingredients_found=[
                IngredientFinding(**item) for item in (analysis.prohibited_ingredients_found or [])
            ],
            restricted_ingredients_found=[
                IngredientFinding(**item) for item in (analysis.restricted_ingredients_found or [])
            ],
            warnings=analysis.warnings or [],
            recommendations=analysis.recommendations or [],
            ai_analysis_summary=analysis.ai_analysis_summary,
            ai_model_used=analysis.ai_model_used,
            created_at=analysis.created_at,
            updated_at=analysis.updated_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get(
    "/analyses",
    response_model=List[ProductAnalysisSummary],
    summary="Get User's Product Analyses",
    description="Retrieve all compliance analyses for the current user"
)
async def get_user_analyses(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all product analyses for the authenticated user"""
    service = RegTechService(db)
    analyses = service.get_user_analyses(current_user.id, skip, limit)
    
    return [
        ProductAnalysisSummary(
            id=a.id,
            product_name=a.product_name,
            target_country=a.target_country,
            compliance_status=a.compliance_status,
            compliance_score=a.compliance_score,
            risk_level=a.risk_level,
            created_at=a.created_at
        )
        for a in analyses
    ]


@router.get(
    "/analyses/{analysis_id}",
    response_model=ProductAnalysisResponse,
    summary="Get Product Analysis by ID",
    description="Retrieve detailed compliance analysis by ID"
)
async def get_analysis_by_id(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific product analysis by ID"""
    service = RegTechService(db)
    analysis = service.get_analysis_by_id(analysis_id, current_user.id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    return ProductAnalysisResponse(
        id=analysis.id,
        product_name=analysis.product_name,
        product_category=analysis.product_category,
        brand_name=analysis.brand_name,
        target_country=analysis.target_country,
        regulation_type=analysis.regulation_type,
        compliance_status=analysis.compliance_status,
        compliance_score=analysis.compliance_score,
        risk_level=analysis.risk_level,
        prohibited_ingredients_found=[
            IngredientFinding(**item) for item in (analysis.prohibited_ingredients_found or [])
        ],
        restricted_ingredients_found=[
            IngredientFinding(**item) for item in (analysis.restricted_ingredients_found or [])
        ],
        warnings=analysis.warnings or [],
        recommendations=analysis.recommendations or [],
        ai_analysis_summary=analysis.ai_analysis_summary,
        ai_model_used=analysis.ai_model_used,
        created_at=analysis.created_at,
        updated_at=analysis.updated_at
    )


@router.get(
    "/statistics",
    response_model=ComplianceStatistics,
    summary="Get Compliance Statistics",
    description="Get compliance statistics and dashboard metrics for the current user"
)
async def get_compliance_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get compliance statistics for dashboard"""
    service = RegTechService(db)
    analyses = service.get_user_analyses(current_user.id, skip=0, limit=1000)
    
    # Calculate statistics
    total_analyses = len(analyses)
    compliant_count = sum(1 for a in analyses if a.compliance_status.value == "COMPLIANT")
    warning_count = sum(1 for a in analyses if a.compliance_status.value == "WARNING")
    non_compliant_count = sum(1 for a in analyses if a.compliance_status.value == "NON_COMPLIANT")
    
    avg_score = sum(a.compliance_score for a in analyses) / total_analyses if total_analyses > 0 else 0.0
    
    # Get recent analyses
    recent_analyses = analyses[:5]
    
    return ComplianceStatistics(
        total_analyses=total_analyses,
        compliant_count=compliant_count,
        warning_count=warning_count,
        non_compliant_count=non_compliant_count,
        average_compliance_score=round(avg_score, 2),
        recent_analyses=[
            ProductAnalysisSummary(
                id=a.id,
                product_name=a.product_name,
                target_country=a.target_country,
                compliance_status=a.compliance_status,
                compliance_score=a.compliance_score,
                risk_level=a.risk_level,
                created_at=a.created_at
            )
            for a in recent_analyses
        ]
    )


@router.delete(
    "/analyses/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Product Analysis",
    description="Delete a compliance analysis"
)
async def delete_analysis(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a product analysis"""
    service = RegTechService(db)
    analysis = service.get_analysis_by_id(analysis_id, current_user.id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    db.delete(analysis)
    db.commit()
    
    return None


@router.get(
    "/analyses/{analysis_id}/pdf",
    summary="Generate PDF Report",
    description="Generate and download PDF compliance report for an analysis"
)
async def generate_pdf_report(
    analysis_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate PDF report for analysis"""
    from fastapi.responses import StreamingResponse
    from app.services.pdf_report_service import PDFReportService
    
    service = RegTechService(db)
    analysis = service.get_analysis_by_id(analysis_id, current_user.id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    try:
        pdf_service = PDFReportService()
        pdf_buffer = pdf_service.generate_compliance_report(analysis)
        
        filename = f"compliance_report_{analysis.product_name.replace(' ', '_')}_{analysis.id}.pdf"
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF generation failed: {str(e)}"
        )
