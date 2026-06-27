import anthropic
import json

client = anthropic.Anthropic()

def build_plan(tour_description):
    system_prompt = """You are a tour planning agent.
Read the tour description and return ONLY a JSON object.
No preamble, no markdown, no backticks.

Use exactly this shape:
{
  "band_name": string,
  "party_size": number,
  "vehicle_hint": string,
  "stops": [
    {"city": string, "date": string, "needs": ["venue", "weather", "transport"]}
  ]
}

For vehicle_hint, recommend a vehicle based on party_size plus gear.
Always include venue, weather, and transport in each stop's needs.
"""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        system=system_prompt,
        messages=[{"role": "user", "content": tour_description}],
    )
    return json.loads(msg.content[0].text)


if __name__ == "__main__":
    sample = """
    The band is Las Cafeteras, 6 people plus gear.
    We play Austin on August 10, Houston on August 12, San Antonio on August 14.
    Mostly driving between cities. Mid-size budget.
    """
    plan = build_plan(sample)
    print("Band:", plan["band_name"])
    print("Party size:", plan["party_size"])
    print("Vehicle:", plan["vehicle_hint"])
    print()
    print("Stops:")
    for stop in plan["stops"]:
        print(" -", stop["city"], "on", stop["date"], "| research:", ", ".join(stop["needs"]))