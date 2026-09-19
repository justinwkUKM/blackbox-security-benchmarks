# Running locally

1. Install Docker and Python 3.10+.
2. Start a challenge with `docker compose up -d` from that challenge directory.
3. Confirm the exposed target port from its `docker-compose.yml`.
4. Run the matching evaluator from the repository root.
5. Tear down the environment with `docker compose down` when finished.

Keep the agent workspace separate from this repository so the agent cannot inspect challenge implementation or grading files.
