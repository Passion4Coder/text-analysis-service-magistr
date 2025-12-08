#!/bin/bash

# Start Ollama in the background.
/bin/ollama serve &
# Record Process ID.
pid=$!

# Pause for Ollama to start.
sleep 5

echo "🔴 Retrieve mistral:latest model..."
ollama pull mistral:latest
echo "🟢 Done!"

# Wait for Ollama process to finish.
wait $pid
