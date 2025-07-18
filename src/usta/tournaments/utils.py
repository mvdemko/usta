from data_retrieval.usta.tournaments.models.tournament import Tournament


def get_players_by_event(tournament: Tournament) -> dict[str, int]:
    players_by_event = {}
    players = tournament.players
    for player in players:
        events = player.events
        for event in events:
            if event not in players_by_event:
                players_by_event[event] = 1
            else:
                players_by_event[event] += 1

    return players_by_event
