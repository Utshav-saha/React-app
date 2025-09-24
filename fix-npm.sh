#!/bin/bash

echo "🔧 Fixing npm permissions for global installs..."

# Create a directory for global installs in your home directory
mkdir -p ~/.npm-global

# Configure npm to use the new directory path
npm config set prefix '~/.npm-global'

# Add the new path to your shell profile
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc

echo "✅ NPM permissions fixed!"
echo "📝 Please run: source ~/.zshrc"
echo "🔄 Then you can install global packages without sudo"