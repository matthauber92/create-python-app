#!/bin/bash

# Get the current directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Read project name from user input
read -p "Enter project name: " project_name

mkdir $project_name
cd $project_name

# Create a virtual environment
python3 -m venv venv

echo "Initialized Virtual env"

# Activate the virtual environment
source venv/bin/activate

pip install \
  fastapi \
  strawberry-graphql \
  requests \
  psycopg2-binary \
  sqlalchemy \
  pydantic \
  alembic \
  python-jose \
  python-dotenv

# Create requirements file
pip freeze > requirements.txt

echo "Installed all dependencies successfully!"

# Initialize migration tool
alembic init alembic

echo "Initialized Alembic migration tool."

# Copy over templates
cp -r "$SCRIPT_DIR/templates/bin" .
cp -r "$SCRIPT_DIR/templates/core" .
cp -r "$SCRIPT_DIR/templates/db" .
cp -r "$SCRIPT_DIR/templates/middleware" .
cp -r "$SCRIPT_DIR/templates/resolvers" .
cp -r "$SCRIPT_DIR/templates/services" .
cp -r "$SCRIPT_DIR/templates/utils" .
cp "$SCRIPT_DIR/templates/README.md" .
cp "$SCRIPT_DIR/templates/docker-compose.yml" .
cp "$SCRIPT_DIR/templates/.Dockerfile" .
cp "$SCRIPT_DIR/templates/.env" .
cp "$SCRIPT_DIR/templates/main.py" .

# Create git repository
git init

echo ""

echo "Your Python FastAPI Strawberry Graphql app is READY!"

echo ""


