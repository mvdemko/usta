from data_retrieval.usta.tournaments import client
from data_retrieval.usta.tournaments.models.category import Category
from data_retrieval.usta.tournaments.models.section import Section
from pydantic import TypeAdapter

from usta.models.tournament_summary import TournamentSummary


def main():
    tournament_summaries = summarize_tournaments()
    write_data(tournament_summaries)
    # cd src/usta/tournaments
    # poetry run python3 -m http.server
    # enter http://localhost:8000/tournaments.html in the browser


def summarize_tournaments():
    category = Category("Adult (18+)")
    section = Section("Southern California")
    tournaments = client.fetch_tournaments(category, section)

    return [TournamentSummary(**tournament.model_dump()) for tournament in tournaments]


def write_data(tournament_summaries: list[TournamentSummary]) -> None:
    adapter = TypeAdapter(list[TournamentSummary])
    json_data_adapter = adapter.dump_json(tournament_summaries, indent=4).decode(
        "utf-8"
    )
    file_path = "output.json"
    with open(file_path, "w") as f:
        f.write(json_data_adapter)


if __name__ == "__main__":
    main()
