import anthropic
from research import run_research

client = anthropic.Anthropic()

# Write a clean tour itinerary from the research data.
def write_itinerary(data):
    system = """You are a tour operations writer.
Write a clean, professional tour itinerary the tour manager can hand to the band.
Plain text. One clear section per city with date, weather note, transport, and suggested venues.
Open with the band name and a one-line summary. Keep it tight and scannable."""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system=system,
        messages=[{"role": "user", "content": str(data)}],
    )
    return msg.content[0].text

# Write a short outreach email the manager can send to a venue.
def write_outreach(data):
    system = """You are a tour booking assistant.
Write ONE short, warm outreach email to a venue.
Introduce the band, mention the city and date, ask about availability and booking.
Use [VENUE NAME] as a placeholder. Under 150 words.
Start the first line with 'Subject: ...'."""
    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        system=system,
        messages=[{"role": "user", "content": str(data)}],
    )
    return msg.content[0].text


if __name__ == "__main__":
    sample = """
    The band is Las Cafeteras, 6 people plus gear.
    We play Austin on August 10, Houston on August 12, San Antonio on August 14.
    Mostly driving between cities. Mid-size budget.
    """
    print("Gathering research...")
    data = run_research(sample)

    print("\n===== TOUR ITINERARY =====\n")
    print(write_itinerary(data))

    print("\n===== DRAFT VENUE EMAIL =====\n")
    print(write_outreach(data))