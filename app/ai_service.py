

import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"


def _call_llm(prompt: str, timeout: int = 120) -> str:
   
    resp = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=timeout,
    )
    resp.raise_for_status()
    return resp.json().get("response", "")



# AGENT 1 — RESEARCHER

def researcher_agent(destination: str, budget: float, days: int, preferences: str) -> str:
    """Destination ki research karta hai. Iska output Agent 2 use karega."""
    prompt = (
        "You are a TRAVEL RESEARCHER agent.\n"
        f"Research the destination: {destination}.\n"
        f"Trip is {days} days with a total budget of {budget} INR.\n"
        f"Traveller preferences: {preferences or 'general sightseeing'}.\n\n"
        "Provide a concise research brief covering:\n"
        "1. Top 5-6 attractions/places to visit\n"
        "2. Approximate daily cost (food + local transport + entry fees)\n"
        "3. Best area to stay\n"
        "4. 2-3 practical travel tips\n"
        "Keep it factual and short."
    )
    return _call_llm(prompt)



# AGENT 2 — PLANNER (uses Agent 1's research)

def planner_agent(destination: str, budget: float, days: int,
                  preferences: str, research: str) -> str:
    """Researcher ke output ko leke day-by-day itinerary banata hai."""
    prompt = (
        "You are a TRIP PLANNER agent.\n"
        "Another agent has already researched the destination. "
        "Use their research below to build the plan.\n\n"
        f"--- RESEARCH FROM RESEARCHER AGENT ---\n{research}\n--- END RESEARCH ---\n\n"
        f"Now create a {days}-day itinerary for {destination} within {budget} INR total. "
        f"Preferences: {preferences or 'general sightseeing'}.\n\n"
        "Respond ONLY with valid JSON in EXACTLY this format, no extra text:\n"
        "{\n"
        '  "summary": "2-3 line trip overview",\n'
        '  "days": [\n'
        '    {"day_number": 1, "activities": "morning, afternoon, evening plan", "estimated_cost": 1500}\n'
        "  ]\n"
        "}"
    )
    return _call_llm(prompt)



# ORCHESTRATOR — dono agents ko sequence me chalata hai (AGENTIC FLOW)

def generate_trip_plan(destination: str, budget: float, duration_days: int,
                       preferences: str = "") -> dict:
    """
    Agentic flow:
      Step 1: Researcher agent destination research karta hai.
      Step 2: Planner agent us research ko use karke itinerary banata hai.
    """
    try:
        # --- AGENT 1 ---
        research = researcher_agent(destination, budget, duration_days, preferences)
        # --- AGENT 2 (uses Agent 1 output) ---
        plan_raw = planner_agent(destination, budget, duration_days, preferences, research)
        return _parse_plan(plan_raw, destination, budget, duration_days)
    except Exception:
        return _fallback_plan(destination, budget, duration_days)


def _parse_plan(raw: str, destination: str, budget: float, days: int) -> dict:
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        data = json.loads(raw[start:end])
        if "days" in data and isinstance(data["days"], list) and data["days"]:
            return data
    except Exception:
        pass
    return _fallback_plan(destination, budget, days)


def _fallback_plan(destination: str, budget: float, days: int) -> dict:
    per_day = round(budget / days, 2) if days else budget
    return {
        "summary": f"A {days}-day trip to {destination} planned within {budget} INR. "
                   "(Offline plan - start Ollama for full AI-powered itinerary.)",
        "days": [
            {"day_number": i + 1,
             "activities": f"Day {i+1}: Explore {destination} - sightseeing, local food, key attractions.",
             "estimated_cost": per_day}
            for i in range(days)
        ],
    }
