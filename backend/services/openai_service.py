from openai import AsyncOpenAI
import logging
from config import settings

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        """
        Initializes the async OpenAI client for generating public health 
        and preparedness broadcasts.
        """
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini" # Optimized for low latency and cost-effectiveness in hackathon environments

    async def generate_public_advisory(self, issue_category: str, severity: float, location: str) -> str:
        """
        Generates actionable, bilingual behaviour-change messaging for public preparedness.
        
        Args:
            issue_category (str): The classification output from Hugging Face.
            severity (float): Confidence score or calculated severity metric (0.0 to 1.0).
            location (str): The specific district or zone in Lahore (e.g., Gulberg, DHA).
            
        Returns:
            str: The generated advisory text.
        """
        if not settings.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not configured.")

        # Map severity float to human-readable context
        urgency = "Critical/Immediate Action Required" if severity > 0.75 else "Advisory/Caution"

        prompt = (
            f"You are a public safety and environmental AI for the city of Lahore. "
            f"An urban issue has been identified:\n"
            f"- Category: {issue_category}\n"
            f"- Urgency Level: {urgency} ({severity:.2f} threshold)\n"
            f"- Location: {location}\n\n"
            f"Generate a short, urgent, and highly actionable public broadcast message. "
            f"Include specific behavioral changes citizens should make immediately to stay safe or mitigate the issue. "
            f"Keep the formatting clean and strictly under 4 sentences. "
            f"Provide the output first in English, followed by an accurate Urdu translation."
        )

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert urban intelligence assistant designed for the Smart City Hackathon Lahore."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.4, # Lower temperature for factual, serious emergency advisories
                max_tokens=400
            )
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API integration error: {str(e)}")
            raise Exception("Failed to generate public preparedness advisory via OpenAI.")