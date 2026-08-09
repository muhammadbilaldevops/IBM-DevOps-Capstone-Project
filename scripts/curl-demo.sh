#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${BASE_URL:-http://localhost:8080}"
echo "== CREATE =="
curl -sS -X POST "$BASE_URL/accounts" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com","address":"1 Main St","phone_number":"555-0100","date_joined":"2025-01-15"}'
echo
echo "== LIST =="
curl -sS "$BASE_URL/accounts"
echo
echo "== READ =="
curl -sS "$BASE_URL/accounts/1"
echo
echo "== UPDATE =="
curl -sS -X PUT "$BASE_URL/accounts/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Updated"}'
echo
echo "== DELETE =="
curl -sS -i -X DELETE "$BASE_URL/accounts/1"
