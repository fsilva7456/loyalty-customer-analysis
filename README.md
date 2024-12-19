# Loyalty Customer Analysis Service

This FastAPI service generates customer segment analysis for loyalty programs using OpenAI's GPT-4 model.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/fsilva7456/loyalty-customer-analysis.git
   cd loyalty-customer-analysis
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## Running the Service

1. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

2. The service will be available at `http://localhost:8000`

## API Documentation

- API documentation is available at `http://localhost:8000/docs`
- OpenAPI specification is available at `http://localhost:8000/openapi.json`

### Generate Analysis Endpoint

`POST /generate`

Example request:
```json
{
  "company_name": "Example Corp",
  "previous_data": {
    "competitor_analysis": "Competitor analysis details..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous customer analysis...",
    "user_feedback": "Focus more on high-value segments"
  },
  "other_input_data": {}
}
```

Example response:
```json
{
  "generated_output": "Customer Analysis for Example Corp...\n\n1. Customer Base Overview...\n2. Key Segments...\n3. Loyalty Program Recommendations...",
  "structured_data": {
    "customer_segments": [
      {
        "name": "Premium Loyalists",
        "size_percentage": 15.0,
        "characteristics": [
          "High-frequency shoppers",
          "Premium product preference"
        ],
        "preferred_rewards": [
          "Exclusive early access",
          "VIP events"
        ],
        "engagement_level": "High",
        "lifetime_value": "$5000+"
      }
    ]
  }
}
```

## Key Features

- Uses OpenAI's GPT-4 model for analysis
- Provides both narrative analysis and structured segment data
- Integrates competitor analysis context
- Supports iterative refinement through feedback
- Input validation using Pydantic
- Error handling and API monitoring

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Notes

- The service uses GPT-4 by default. You can modify the `model` parameter in `generate_customer_analysis()` to use a different model.
- The response includes both a detailed text analysis and structured JSON data about customer segments.
- The system prompt is designed to provide consistent, structured analysis focusing on customer segmentation and loyalty program strategies.
- Previous analysis and feedback can be provided to refine and improve the analysis.
