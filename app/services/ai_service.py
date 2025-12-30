"""AI service for bottle research using OpenAI"""

from typing import Optional, Dict, Any
import logging
from app.config import settings

logger = logging.getLogger(__name__)


async def research_bottle(
    bottle_name: str,
    distillery: Optional[str] = None,
    spirit_type: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Research a bottle using OpenAI API and return detailed information.
    
    Args:
        bottle_name: Name of the bottle/whiskey
        distillery: Optional distillery name
        spirit_type: Type of spirit (whiskey, vodka, etc.)
    
    Returns:
        Dictionary with research details or None if research fails
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Build search query
        search_query = bottle_name
        if distillery:
            search_query += f" from {distillery}"
        if spirit_type:
            search_query += f" ({spirit_type})"
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are a spirits expert. When given a bottle name, provide detailed 
                    information in JSON format with the following fields:
                    - tasting_notes: Brief description of tasting profile
                    - history: Brief history of the brand/bottle
                    - production_process: Overview of production
                    - price_range: Estimated price range in USD
                    - rarity: Rarity assessment (common, uncommon, rare, very rare)
                    - recommended_glassware: Type of glass to drink from
                    - serving_suggestions: How to best enjoy it
                    - awards: Any notable awards or recognition""",
                },
                {
                    "role": "user",
                    "content": f"Please provide detailed information about: {search_query}",
                },
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        
        # Parse response
        content = response.choices[0].message.content
        
        # Try to extract JSON from response
        import json
        import re
        
        # Look for JSON block in response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            ai_details = json.loads(json_match.group())
            ai_details["source"] = "openai"
            return ai_details
        else:
            # If no JSON, store the raw content
            return {
                "source": "openai",
                "raw_response": content,
            }
            
    except Exception as e:
        logger.error(f"Error researching bottle {bottle_name}: {str(e)}")
        return None


async def generate_tasting_notes(
    bottle_name: str,
    distillery: Optional[str] = None,
    proof: Optional[float] = None,
) -> Optional[str]:
    """
    Generate tasting notes for a bottle using OpenAI.
    
    Args:
        bottle_name: Name of the bottle
        distillery: Optional distillery name
        proof: Optional proof of the spirit
    
    Returns:
        Generated tasting notes or None if generation fails
    """
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Build context
        context = bottle_name
        if distillery:
            context += f" from {distillery}"
        if proof:
            context += f" at {proof} proof"
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert spirits taster. Generate vivid, professional 
                    tasting notes for spirits. Format as:
                    Nose: [nose notes]
                    Palate: [palate notes]
                    Finish: [finish notes]""",
                },
                {
                    "role": "user",
                    "content": f"Generate tasting notes for: {context}",
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Error generating tasting notes for {bottle_name}: {str(e)}")
        return None
