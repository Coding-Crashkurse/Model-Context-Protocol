#!/usr/bin/env bash
set -euo pipefail

S=http://127.0.0.1:8000/mcp/
ACCEPT='application/json, text/event-stream'
CT='application/json'

curl -sS \
  -H "Accept: $ACCEPT" \
  -H "Content-Type: $CT" \
  -X POST "$S" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
        "name":"add",
        "arguments":{"a":2,"b":3}
      }}'
echo
