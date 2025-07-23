import os

from data_retrieval.usta.tournaments.models.player import Player
from data_retrieval.usta.tournaments.models.tournament import Tournament
from pydantic import Field

from usta.tournaments.utils import calculate_distance


class TournamentSummary(Tournament):
    players: list[Player] = Field(exclude=True)
    players_by_event: dict[str, int] = None
    distance_from_home_mi: int = None

    def __init__(self, **data):
        super().__init__(**data)
        self.players_by_event = self._calculate_players_by_event()
        self.distance_from_home_mi = calculate_distance(
            os.getenv("HOME_ADDRESS"), self.facility.location
        )

    def _calculate_players_by_event(self) -> dict[str, int]:
        players_by_event = {}
        for player in self.players:
            events = player.events
            for event in events:
                players_by_event[event] = players_by_event.get(event, 0) + 1

        return dict(sorted(players_by_event.items()))
