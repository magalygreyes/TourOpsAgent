import anthropic
import requests
import json
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

# Send the finished itinerary to n8n, which emails it.
def send_to_n8n(itinerary):
    webhook_url = "https://magalygreyes.app.n8n.cloud/webhook/tour-itinerary"
    try:
        response = requests.post(webhook_url, json={"itinerary": itinerary}, timeout=30)
        print("n8n responded:", response.status_code)
        if response.status_code == 200:
            print("Email sent. Check your inbox.")
    except Exception as e:
        print("Send failed:", e)


if __name__ == "__main__":
    sample = """
    The band is Las Cafeteras, 6 people plus gear.
    We play Austin on August 10, Houston on August 12, San Antonio on August 14.
    Mostly driving between cities. Mid-size budget.
    """
    print("Gathering research...")
    data = run_research(sample)

    print("\n===== TOUR ITINERARY =====\n")
    itinerary = write_itinerary(data)
    print(itinerary)

    print("\n===== DRAFT VENUE EMAIL =====\n")
    print(write_outreach(data))

    print("\n===== SENDING TO N8N =====\n")
    send_to_n8n(itinerary)