#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Flask
pip install flask gunicorn

echo "Build completed successfully"