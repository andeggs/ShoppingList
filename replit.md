# Flask Meal Planner App with AI Shopping List

## Overview
A Flask web application that allows users to add and manage meals using a PostgreSQL database, and generate intelligent shopping lists using Google Gemini AI.

## Project Structure
- `app.py` - Main Flask application with database operations, API endpoints, and Gemini AI integration
- `templates/index.html` - Frontend HTML page with styling and JavaScript
- `.gitignore` - Python-specific ignore patterns

## Features
- **Add Meals**: Type in the input box and click "Add meal" or press Enter
- **View All Meals**: See all your meals in a list below the button
- **Delete Meals**: Click the red X button next to each meal to remove it
- **AI Shopping List**: Click "Create shopping list" to generate a comprehensive ingredient list using Google Gemini AI
- **Persistent Storage**: All meals are saved in the database and remain between sessions

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
- `POST /shopping-list` - Generate shopping list using Google Gemini AI

## Google Gemini Integration
- Uses Google Gemini API to analyze meal list and generate comprehensive shopping lists
- Automatically groups ingredients and suggests quantities
- API key stored securely in Replit Secrets as `GEMINI_API_KEY`

## User Interface
- Clean, modern design with purple gradient background
- Input box for entering meal names
- Blue "Add meal" button
- Green "Create shopping list" button
- List of all meals with delete buttons (red X marks)
- Ingredients section that appears after generating shopping list
- Confirmation prompt before deleting meals
- Loading indicator while AI generates shopping list

## Running the App
The app runs on port 5000 via the Flask App workflow.
Database is automatically initialized on startup.

## Technologies Used
- Python 3.11
- Flask 3.1.2
- PostgreSQL (via psycopg2-binary)
- Google Gemini AI (via google-genai)
- HTML/CSS/JavaScript

## Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `GEMINI_API_KEY` - Google Gemini API key
