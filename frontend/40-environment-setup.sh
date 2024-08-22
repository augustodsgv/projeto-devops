#!/bin/sh
# Backend url
if [ -z "$BACKEND_URL" ]; then
    echo "BACKEND_URL environment variable must be set."
    exit 1
fi

# Backend port
if [ -z "$BACKEND_PORT" ]; then
    echo "BACKEND_PORT environment variable must be set."
    exit 1
fi

# File to write to env file
BACKEND_IP=$(dig +short $BACKEND_URL)
file="
const env = {
    BACKEND_URL: \"$BACKEND_IP\",
    BACKEND_PORT: $BACKEND_PORT
};

export default env;"

echo "$file" > /usr/share/nginx/html/env.js