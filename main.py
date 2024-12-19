import os
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import json

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

def construct_system_prompt() -> str:
    return """
You are an expert in customer segmentation and loyalty program analysis. 
Analyze the provided company's customer base and recommend loyalty program strategies.

Consider:
1. Customer demographics and behavior patterns
2. Purchase frequency and value
3. Channel preferences and engagement levels
4. Loyalty program preferences
5. Competitive context (if provided)

Provide your response in two parts:
1. A detailed analysis in natural language
2. A structured JSON object containing customer segments with this exact schema:
{
    "customer_segments": [
        {
            "name": "Segment Name",
            "size_percentage": 25.0,
            "characteristics": ["characteristic1", "characteristic2"],
            "preferred_rewards": ["reward1", "reward2"],
            "engagement_level": "High/Medium/Low",
            "lifetime_value": "$X,XXX+"
        }
    ]
}

Separate the two parts with [JSON_START] and [JSON_END] markers.
"""

def construct_user_prompt(
    company_name: str,
    competitor_analysis: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> str:
    prompt = f"Please analyze the customer segments for {company_name}."
    
    if competitor_analysis:
        prompt += f"\n\nConsider this competitor analysis: {competitor_analysis}"
    
    if existing_output and feedback:
        prompt += f"""
\n\nPrevious analysis: {existing_output}
\nPlease refine the analysis based on this feedback: {feedback}
"""
    
    return prompt

def extract_json_from_text(text: str) -> dict:
    try:
        start_marker = "[JSON_START]"
        end_marker = "[JSON_END]"
        json_str = text[text.find(start_marker) + len(start_marker):text.find(end_marker)].strip()
        return json.loads(json_str)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse structured data from response: {str(e)}"
        )

def generate_customer_analysis(
    company_name: str,
    competitor_analysis: Optional[str] = None,
    existing_output: Optional[str] = None,
    feedback: Optional[str] = None
) -> tuple[str, dict]:
    """Generate customer analysis using OpenAI's API"""
    try:
        # Create completion using OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": construct_system_prompt()},
                {"role": "user", "content": construct_user_prompt(
                    company_name,
                    competitor_analysis,
                    existing_output,
                    feedback
                )}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract the response text
        full_response = response.choices[0].message.content
        
        # Split into analysis and structured data
        analysis = full_response[:full_response.find("[JSON_START]")].strip()
        structured_data = extract_json_from_text(full_response)
        
        return analysis, structured_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", response_model=CustomerAnalysisResponse)
async def generate_analysis(request: CustomerAnalysisRequest):
    # Extract data from request
    competitor_analysis = (
        request.previous_data.competitor_analysis
        if request.previous_data
        else None
    )
    
    existing_output = None
    feedback = None
    if request.current_prompt_data:
        existing_output = request.current_prompt_data.existing_generated_output
        feedback = request.current_prompt_data.user_feedback
    
    # Generate analysis
    generated_text, structured_data = generate_customer_analysis(
        request.company_name,
        competitor_analysis,
        existing_output,
        feedback
    )
    
    # Prepare response
    return CustomerAnalysisResponse(
        generated_output=generated_text,
        structured_data=structured_data
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
