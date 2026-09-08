from flask import Flask, request, jsonify
import re

app = Flask(__name__)

KNOWLEDGE_BASE = {
    r'\b(chok(e|ing)|swallow)\b': {
        "title": "Choking Response",
        "steps": [
            "Ask 'Are you choking?' If they cannot cough or speak, act immediately.",
            "Give 5 sharp back blows between the shoulder blades with the heel of your hand.",
            "Perform 5 abdominal thrusts (Heimlich maneuver).",
            "Repeat until the object is dislodged or help arrives."
        ]
    },
    r'\b(cpr|heart|breath(e|ing)?|pulse)\b': {
        "title": "CPR Protocol",
        "steps": [
            "Check responsiveness and breathing.",
            "Call 108 / emergency services immediately.",
            "Place hands in the center of the chest.",
            "Push hard and fast (100–120 compressions per minute).",
            "Continue until emergency medical help takes over."
        ]
    },
    r'\b(burn(s|ed)?|fire|scald)\b': {
        "title": "Burn Emergency",
        "steps": [
            "Cool the burn under cool running water for 10–20 minutes.",
            "Remove tight clothes or jewelry before swelling occurs.",
            "Cover loosely with sterile, non-fluffy cloth.",
            "Do NOT apply ice, oil, butter, or toothpastes."
        ]
    },
    r'\b(bleed(ing)?|cut|wound)\b': {
        "title": "Severe Bleeding",
        "steps": [
            "Apply firm, continuous direct pressure with a clean cloth.",
            "Elevate the injured area above the heart if possible.",
            "Keep pressure applied continuously until paramedics arrive.",
            "Do NOT remove blood-soaked cloths; add new ones on top."
        ]
    },
    r'\b(snake|bite|bitten)\b': {
        "title": "Snake Bite Management",
        "steps": [
            "Keep the patient calm, immobilized, and still.",
            "Position the bitten limb below or at heart level.",
            "Remove rings, watches, or tight clothing near the bite.",
            "Do NOT cut the wound, suck out venom, or apply a tourniquet."
        ]
    },
    r'\b(stroke|face|speech|arm)\b': {
        "title": "Stroke (F.A.S.T. Assessment)",
        "steps": [
            "F - Face Drooping: Ask them to smile.",
            "A - Arm Weakness: Ask them to raise both arms.",
            "S - Speech Difficulty: Ask them to repeat a simple sentence.",
            "T - Time to Call 108 immediately if any signs are present."
        ]
    }
}

def analyze_intent(user_text):
    text = user_text.lower()
    if re.search(r'\b(hi|hello|hey|start|help)\b', text):
        return {
            "type": "greeting",
            "title": "Welcome",
            "message": "Select an emergency quick-chip below or describe the situation directly."
        }

    for pattern, protocol in KNOWLEDGE_BASE.items():
        if re.search(pattern, text):
            return {
                "type": "protocol",
                "title": protocol['title'],
                "steps": protocol['steps']
            }

    return {
        "type": "unknown",
        "title": "Unclear Request",
        "message": "Emergency intent not recognized. Please choose a chip or state the situation clearly (e.g., 'bleeding', 'CPR'). <strong>If critical, call 108 immediately.</strong>"
    }

# Accept any route pattern forwarded by Vercel
@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def handle_chat(path):
    data = request.get_json(silent=True) or {}
    user_msg = data.get('message', '')
    return jsonify(analyze_intent(user_msg))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
