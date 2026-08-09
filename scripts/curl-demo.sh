#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
echo "== CREATE =="
curl -sS -X POST "$BASE_URL/api/accounts" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St"}'
echo
echo "== LIST =="
curl -sS "$BASE_URL/api/accounts"
echo
echo "== READ =="
curl -sS "$BASE_URL/api/accounts/1"
echo
echo "== UPDATE =="
curl -sS -X PUT "$BASE_URL/api/accounts/1" \
  -H "Content-Type: application/json" \
  -d '{"address":"2 Main St"}'
echo
echo "== DELETE =="
curl -sS -i -X DELETE "$BASE_URL/api/accounts/1"
