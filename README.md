# Loyalty Customer Analysis Service

This FastAPI service generates customer segment analysis for loyalty programs using OpenAI's GPT models.

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
    "competitor_analysis": "Previous competitor analysis..."
  },
  "current_prompt_data": {
    "existing_generated_output": "Previous analysis...",
    "user_feedback": "Focus more on high-value segments"
  },
  "other_input_data": {}
}
```

Example response:
```json
{
  "generated_output": "Customer Analysis for Example Corp...",
  "structured_data": {
    "customer_segments": [
      {
        "name": "Premium Loyalists",
        "size_percentage": 15.0,
        "characteristics": [
          "High-frequency shoppers",
          "Premium product preference",
          "Long-term customers"
        ],
        "preferred_rewards": [
          "Exclusive early access",
          "Premium service upgrades",
          "VIP events"
        ],
        "engagement_level": "High",
        "lifetime_value": "$5000+"
      }
    ]
  }
}
```

## Development

- The service uses FastAPI for the API framework
- OpenAI's GPT models for generating customer analysis
- Pydantic for data validation

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)

## Note

This is a basic implementation. The OpenAI API call is currently mocked. To use real OpenAI API calls, uncomment and modify the relevant code in the `generate_customer_analysis` function.