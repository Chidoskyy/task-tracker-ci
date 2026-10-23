#!/bin/bash
# validate.sh: smoke test; the deployment fails if /health does not answer ok
for attempt in 1 2 3 4 5 6 7 8 9 10; do
  if curl -s localhost:8080/health | grep -q '"status": "ok"'; then
    echo "Smoke test passed on attempt $attempt"
    exit 0
  fi
  sleep 2
done
echo "Smoke test failed: Task Tracker did not answer on /health" >&2
exit 1
