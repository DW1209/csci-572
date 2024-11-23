#!/bin/sh

echo '{
  "query": "{
    Get{
      SimSearch (
        limit: 5
        nearText: {
          concepts: [\"female singer\"],
        }
      ){
        musicGenre
        songTitle
        artist
      }
    }
  }"
}' | curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d @- \
  "http://localhost:8080/v1/graphql"
