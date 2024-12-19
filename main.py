import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI(title="Loyalty Customer Analysis Service")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class CustomerSegment(BaseModel):
    name: str
    size_percentage: float
    characteristics: List[str]
    preferred_rewards: List[str]
    engagement_level: str
    lifetime_value: str

class PreviousData(BaseModel):
    competitor_analysis: Optional[str] = None

class CurrentPromptData(BaseModel):
    existing_generated_output: str
    user_feedback: str

class CustomerAnalysisRequest(BaseModel):
    company_name: str
    previous_data: Optional[PreviousData] = None
    current_prompt_data: Optional[CurrentPromptData] = None
    other_input_data: Optional[Dict] = {}

class CustomerAnalysisResponse(BaseModel):
    generated_output: str
    structured_data: Dict

def generate_customer_analysis(
    company_name: str,
    competitor_analysis: Optional[str] = None,
    feedback: str = ""
) -> tuple[str, List[CustomerSegment]]:
    """Mock function to simulate OpenAI API call for customer analysis"""
    try:
        # In a real implementation, this would call OpenAI's API
        # completion = client.chat.completions.create(
        #     model="gpt-4",
        #     messages=[
        #         {"role": "system", "content": "You are a customer analysis expert..."}
        #         {"role": "user", "content": f"Analyze customer segments for {company_name}..."}
        #     ]
        # )
        
        # Mock response
        generated_text = f"Customer Analysis for {company_name}:\n\n"
        generated_text += "1. Overview of Customer Base\n"
        generated_text += "2. Key Customer Segments\n"
        generated_text += "3. Loyalty Program Engagement Patterns\n"
        
        if competitor_analysis:
            generated_text += "\n4. Competitive Context:\n"
            generated_text += "Based on competitor analysis, our customers show..."

        # Mock customer segments
        segments = [
            CustomerSegment(
                name="Premium Loyalists",
                size_percentage=15.0,
                characteristics=[
                    "High-frequency shoppers",
                    "Premium product preference",
                    "Long-term customers"
                ],
                preferred_rewards=[
                    "Exclusive early access",
                    "Premium service upgrades",
                    "VIP events"
                ],
                engagement_level="High",
                lifetime_value="$5000+"
            ),
            CustomerSegment(
                name="Value Seekers",
                size_percentage=40.0,
                characteristics=[
                    "Price-sensitive",
                    "Regular promotions usage",
                    "Medium purchase frequency"
                ],
                preferred_rewards=[
                    "Cash back",
                    "Discount offers",
                    "Points multipliers"
                ],
                engagement_level="Medium",
                lifetime_value="$1000-3000"
            )
        ]
        
        return generated_text, segments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=CustomerAnalysisResponse)
async def generate_analysis(request: CustomerAnalysisRequest):
    # Extract relevant data
    competitor_analysis = (
        request.previous_data.competitor_analysis
        if request.previous_data
        else None
    )
    feedback = (
        request.current_prompt_data.user_feedback
        if request.current_prompt_data
        else ""
    )
    
    # Generate analysis
    generated_text, segments = generate_customer_analysis(
        request.company_name,
        competitor_analysis,
        feedback
    )
    
    # Prepare response
    return CustomerAnalysisResponse(
        generated_output=generated_text,
        structured_data={
            "customer_segments": [segment.dict() for segment in segments]
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)