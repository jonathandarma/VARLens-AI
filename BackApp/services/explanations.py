from .pipeline import VideoAnalyzer
from ..config import settings

def explain(result: dict) -> dict:
    decision = result["decision"].replace("_", " ").lower()
    confidence = int(result["confidence"] * 100)
    text = f"The system classifies this phase as {decision} with {confidence}% confidence. It evaluated player positions at the selected pass frame and compared the leading attacker with the defensive line."
    result["explanation"] = text
    result["referee_explanation"] = text + " Confirm the pass moment and player identities before making the final call."
    result["fan_explanation"] = f"At the moment of the pass, the attacker appears {'ahead of' if result['decision'] == 'OFFSIDE' else 'level with or behind'} the defensive line."
    return result
