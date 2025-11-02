# Flask Random Message App

## Overview
A simple Flask web application that displays a random inspirational message from a PostgreSQL database when the user clicks a button.

## Project Structure
- `app.py` - Main Flask application with database initialization and API endpoints
- `templates/index.html` - Frontend HTML page with styling and JavaScript
- `.gitignore` - Python-specific ignore patterns

## Features
- Homepage displays "Hello" with a styled button
- Clicking "Get Random Message" button fetches a random message from the database
- Database stores 5 inspirational messages
- Beautiful gradient background with clean UI

## Database
- PostgreSQL database with a `messages` table
- Contains 5 pre-populated messages:
  1. "Have a wonderful day!"
  2. "You're doing amazing!"
  3. "Keep up the great work!"
  4. "Believe in yourself!"
  5. "Success is just around the corner!"

## Running the App
The app runs on port 5000 via the Flask App workflow.
Database is automatically initialized on startup.

## Technologies Used
- Python 3.11
- Flask 3.1.2
- PostgreSQL (via psycopg2-binary)
- HTML/CSS/JavaScript
