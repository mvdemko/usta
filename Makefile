# Makefile for common dev tasks

.PHONY: update-data serve dev

# Update output.json by running the summary script
update-data:
	@echo "Updating tournament data..."
	cd src/usta/tournaments && poetry run python scripts/summarize_data.py
	@echo "Done. output.json updated at src/usta/tournaments/output.json"

# Start a simple static HTTP server serving src/usta/tournaments on port 8000
serve:
	@echo "Starting static server from src/usta/tournaments on http://localhost:8000"
	cd src/usta/tournaments && poetry run python3 -m http.server 8000

# Update data then start the server (dev convenience target)
dev: update-data serve
