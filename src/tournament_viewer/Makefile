# Makefile for common dev tasks

.PHONY: update-data serve dev

# Update output.json by running the summary script
update-data:
	@echo "Updating tournament data..."
	poetry run python tournaments/scripts/summarize_data.py
	@echo "Done. output.json updated at src/tournament_viewer/tournaments/output.json"

# Start a simple static HTTP server serving src/usta/tournaments on port 8000
serve:
	@echo "Starting static server from src/tournament_viewer/tournaments on http://localhost:8000"
	poetry run python3 -m http.server 8000

# Update data then start the server (dev convenience target)
dev: update-data serve
