#! /bin/sh

# It needs `ollama run deepseek-r1:7b` first to start the server.
# It seems the ollama starts freshly at every start.
# The curl's output is stream-like, one word (token) at a time.

# TODO: I need some good methods to link them together.

curl http://localhost:11434/api/generate -d '{
"model": "deepseek-r1:7b",
"prompt": "What is my name? In one word."
}'

