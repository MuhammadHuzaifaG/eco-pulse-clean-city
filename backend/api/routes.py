from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
import logging

from services.huggingface_service import HuggingFaceService
from services.openai_service import OpenAIService

logger = logging.getLogger(__name__)

router = APIRouter()

class UrbanReportRequest(BaseModel):
    location: str = Field(
        ..., 
        example="Gulberg III, Lahore", 
        description="The specific city zone or district where the issue is reported."
    )
    report_text: str = Field(
        ..., 
        example="Thick black smoke and burning smell coming from the open dump near the main road.",
        description="Unstructured text describing the urban issue or sensor anomaly."
    )

class UrbanAnalysisResponse(BaseModel):
    location: str
    primary_category: str
    severity_score: float
    public_advisory: str
    status: str

@router.post("/analyze-report", response_model=UrbanAnalysisResponse, tags=["Urban Intelligence"])
async def process_urban_report(request: UrbanReportRequest):
    hf_service = HuggingFaceService()
    ai_service = OpenAIService()

    try:
        categorization_result = await hf_service.categorize_urban_issue(request.report_text)
        
        if "labels" not in categorization_result or "scores" not in categorization_result:
            raise ValueError("Unexpected response format from classification model.")

        primary_category = categorization_result["labels"][0]
        severity_score = categorization_result["scores"][0]

        advisory_message = await ai_service.generate_public_advisory(
            issue_category=primary_category,
            severity=severity_score,
            location=request.location
        )

        return UrbanAnalysisResponse(
            location=request.location,
            primary_category=primary_category,
            severity_score=round(severity_score, 4),
            public_advisory=advisory_message,
            status="success"
        )

    except ValueError as ve:
        logger.error(f"Validation Error during analysis: {str(ve)}")
        raise HTTPException(status_code=422, detail=str(ve))
    
    except Exception as e:
        logger.error(f"System Error during analysis chain: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing the urban intelligence report: {str(e)}"
        )