# Flask Meal Planner App

## Overview
A simple Flask web application that allows users to add and manage meals using a PostgreSQL database.

## Project Structure
- `app.py` - Main Flask application with database operations and API endpoints
- `templates/index.html` - Frontend HTML page with styling and JavaScript
- `.gitignore` - Python-specific ignore patterns

## Features
- Add meals by typing in the input box and clicking "Add meal" or pressing Enter
- View all meals in a list below the button
- Delete meals by clicking the red X button next to each meal
- Automatic database initialization on startup

## Database
- PostgreSQL database with a `meals` table
- Table structure:
  - `id` (SERIAL PRIMARY KEY)
  - `name` (TEXT) - The meal name
  - `created_at` (TIMESTAMP) - When the meal was added

## API Endpoints
- `GET /` - Main page
- `GET /meals` - Get all meals
- `POST /meals` - Add a new meal
- `DELETE /meals/<id>` - Delete a meal by ID

## User Interface
- Clean, modern design with purple gradient background
- Input box for entering meal names
- "Add meal" button to save entries
- List of all meals with delete buttons (red X marks)
- Confirmation prompt before deleting meals

## Running the App
The app runs on port 5000 via the Flask App workflow.
Database is automatically initialized on startup.

## Technologies Used
- Python 3.11
- Flask 3.1.2
- PostgreSQL (via psycopg2-binary)
- HTML/CSS/JavaScript
