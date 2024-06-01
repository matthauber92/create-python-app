#!/bin/bash

# Set database connection parameters
DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="postgres"
DB_USER="root"
DB_PASSWORD="password"

# SQL commands to seed users table
PSQL_COMMAND="psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME"

$PSQL_COMMAND <<EOF
-- SQL commands to insert seed data into users table
INSERT INTO users (id, username, password, email) VALUES
  ('$(uuidgen)', 'user1', 'password1', 'user1@example.com'),
  ('$(uuidgen)', 'user2', 'password2', 'user2@example.com'),
  ('$(uuidgen)', 'user3', 'password3', 'user3@example.com');
EOF

echo "Seed data inserted successfully."
