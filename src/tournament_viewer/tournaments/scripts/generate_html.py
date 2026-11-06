import anthropic
from dotenv import load_dotenv


def main():
    load_dotenv()
    message = generate_visualization()
    print(message.content[0].text)
    # cd src/usta/tournaments
    # poetry run python3 -m http.server
    # enter http://localhost:8000/tournaments.html in the browser


def generate_visualization():
    client = anthropic.Anthropic()
    prompt_text = get_prompt_text()
    message = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=3500,
        temperature=1,
        system="You are an expert in map-based data visualization.",
        messages=[{"role": "user", "content": [{"type": "text", "text": prompt_text}]}],
    )

    return message


def get_prompt_text() -> str:
    prompt_text = """
    Your task is to generate code that displays a map-based visualization of USTA tournament
    data.

    Instructions:
    1. The map will be focused on the United States
    2. Each tournament in the data will be represented by a pin on the map
    3. Hovering over a pin on the map should display the following information:
        - Name
        - Url
        - Location
        - Dates
        - Players by event

    The data to be displayed is stored in a file called output.json. This file contains a list of
    tournaments. Each record has the following format:
    {
        "name": "Big Open Tournament",
        "url": "https://playtennis.usta.com/my_tourney",
        "facility": {
            "location": "101 Main Street, Somecity, CA, 90210"
        },
        "status": "Registrations open",
        "dates": "Fri, Jul 25 - Sat, Jul 26, 2025",
        "players_by_event": {
            "Women's Open Singles": 55,
            "Men's Open Singles": 51,
            "Men's Open Doubles": 40,
            "Women's Open Doubles": 44
        },
        "distance_from_home_mi": 100
    }
    """

    return prompt_text


if __name__ == "__main__":
    main()
