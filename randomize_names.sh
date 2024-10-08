#!/bin/bash

# randomize_names.sh
# Random Mint Discs name to tag my containers...for fun

set -e
set -x  # Enable debugging

# Make API Request with all the headers
response=$(curl -s 'https://api.roguediscs.com/v1/category/?url=mint-discs' \
  -H 'accept: application/json, text/plain, */*' \
  -H 'accept-language: en-US,en;q=0.9' \
  -H 'origin: https://roguediscs.com' \
  -H 'priority: u=1, i' \
  -H 'referer: https://roguediscs.com/' \
  -H 'sec-ch-ua: "Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36')

# Check if the response is valid JSON
if ! echo "$response" | jq empty; then
  echo "Invalid JSON response" >&2
  exit 1
fi

# Extract names and randomize
names=$(echo "$response" | jq -r '.Data.tabs.discs | .. | .name? // empty' | shuf)

# Check if names are empty
if [ -z "$names" ]; then
  echo "No names found or invalid response" >&2
  exit 1
fi

# Output the randomized names
echo "$names"
