#!/usr/bin/env bash
set -euo pipefail
S=http://127.0.0.1:8000/mcp/
ACCEPT='application/json, text/event-stream'
CT='application/json'

# 1) initialize
SID=$(curl -sS -D - -o /dev/null \
  -H "Accept: $ACCEPT" -H "Content-Type: $CT" \
  -X POST $S \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{
        "protocolVersion":"2025-03-26",
        "capabilities":{},
        "clientInfo":{"name":"bash","version":"1.0"}
      }}' | sed -nE 's/^Mcp-Session-Id:[[:space:]]*//Ip' | tr -d '\r')
echo "SID=$SID"

# 2) notifications/initialized
curl -sS \
  -H "Accept: $ACCEPT" \
  -H "Content-Type: $CT" \
  -H "Mcp-Session-Id: $SID" \
  -X POST $S \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}'

# 3) tools/call
curl -sS \
  -H "Accept: $ACCEPT" -H "Content-Type: $CT" -H "Mcp-Session-Id: $SID" \
  -X POST $S \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{
        "name":"add","arguments":{"a":2,"b":3}}}'
echo
