#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve models..."
ollama pull mistral:latest
ollama pull nomic-embed-text
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
