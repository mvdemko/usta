from data_retrieval.usta.tournaments import client
from data_retrieval.usta.tournaments.models.category import Category
from data_retrieval.usta.tournaments.models.section import Section
from dotenv import load_dotenv

from usta.models.tournament_summary import TournamentSummary


def main():
    load_dotenv()

    # llm_client = anthropic.Anthropic()

    category = Category("Adult (18+)")
    section = Section("Southern California")
    tournaments = client.fetch_tournaments(category, section)

    tournament_summaries = []
    for tournament in tournaments:
        tournament_summaries.append(TournamentSummary(tournament))

    print(tournament_summaries)


if __name__ == "__main__":
    main()
