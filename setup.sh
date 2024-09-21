#!/bin/bash

# Use this script to setup the project.

OS=$(uname)
echo "You are running on $OS."

# 1. Clear Logs
if [ -z "$CLEAR_LOGS" ]; then
    echo "CLEAR_LOGS is not set. Please set it to true in your environment file if you would like to clear the logs. Skipping log clearing..."
else
    if [ "$CLEAR_LOGS" = "true" ]; then
        (
            cd ./logs
            rm -rf *
        )
        (
            cd ./simpan/logs
            rm -rf *
        )
        echo "Logs cleared."
    else
        echo "CLEAR_LOGS is set to false. Skipping log clearing..."
    fi
fi

# 2. Install Dependencies
echo "Installing required Python packages..."
poetry install

# 3. Update git submodules
echo "Initializing/Updating git submodules..."
git submodule update --init --recursive

# 4. Setup third_party PDF.js
echo "Setting up PDF.js..."
(
    cd ./third_party/pdf
    # If macOS
    if [ "$OS" = "Darwin" ]; then
        echo "You are running on macOS. Installing dependencies..."
        brew install pkg-config cairo pango libpng jpeg giflib librsvg pixman
    fi
    npm install
    npx gulp generic
)

# 5. Run Django specifics
echo "Running Django specifics..."
(
    cd ./simpan
    python manage.py collectlitegraph
    python manage.py collectpdf
    python manage.py makemigrations
    python manage.py migrate
)