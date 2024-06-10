# Capstone Project: Reel Report
# ReelReport

ReelReport is a web application designed to help anglers keep track of their fishing catches. Users can log their catches, including details such as the species of fish, the lake where it was caught, date and time, and the size and weight of the fish, and more. Using the lake, date, and time the user inputs, it will automatically capture and store weather data.
-**Link to site:** Coming Soon. Finding alternative free database then will be deployed on render.

## Features

- **User Authentication:** Users can sign up and log in to their accounts securely.
- **Fish Catches:** Logged-in users can add, view, edit, and delete their fishing catches.
- **Lake Information:** Users can view information about lakes, including their names, locations, and nearby towns.
- **Fish Species:** Users can view information about different fish species, including their names and master angler sizes.
- **Lure Management:** Users can manage their collection of fishing lures, including adding, editing, and deleting them.

- **Standard User Flow:**
    1. **Sign Up/Login:** Users can sign up for a new account or log in with their existing credentials.
    2. **View Profile** After logging in, users will be directed to their profile page that summarazies their most recent catches, master angler catches, and some statistics on the fish they have caught. 
    3. **View Lakes:** After logging in, users can view information about lakes, including their names, locations, and nearby towns. Click on a lake name to view forecast data for the lake. Admin users have the option to delete and edit. 
    4. **View Fish Species:** Users can browse through a list of fish species and view details about each species, such as their names and master angler sizes. Admin users have the option to delete and edit. 
    5. **Manage Tackle Box:** Users can manage their collection of fishing lures by adding, editing, and deleting them from their tackle box.
    6. **Log Fishing Catches:** Users can log their fishing catches, providing details such as the species of fish, the lake where it was caught, date and time, and the size and weight of the fish.
    7. **View Individual Fish Catches:** Logged-in users can view specific details about their logged fishing catches, including species of fish, the lake where it was caught, and the date and time of the catch, image and various weather data. 
    8. **Edit/Delete Fishing Catches:** Users can edit or delete their previously logged fishing catches.
    9. **Log Out:** Users can log out of their accounts to securely end their session.

## Technologies Used
- **Flask:** The backend of the application is built using Flask, a lightweight and flexible web framework for Python.
- **SQLAlchemy:** SQLAlchemy is used as the ORM (Object-Relational Mapping) library to interact with the database.
- **PostgreSQL:** PostgreSQL is used as the database management system to store application data.
- **HTML/CSS:** The frontend of the application is built using HTML for structure and CSS for styling.
- **Bootstrap:** Bootstrap is used for responsive and mobile-first front-end web development.

## Installation

To run the ReelReport application locally, follow these steps:

1. Clone this repository to your local machine:

   ```bash
    git clone https://github.com/yourusername/reelreport.git
2. Navigate to repository"
   ```bash 
    cd reelreport
3. Create virtual environment
    ```bash
    python3 -m venv venv
4. Start virtual environment
    ```bash
    source venv/bin/activate
5. Install the required dependencies
    ```bash
    pip install -r requirements.txt
6. Create a PostgreSQL database named reel_report"
    ```bash
    createdb reel_report
7. seed database by running seed.py file
8. Run the Flask application:
    ```bash
    flask run --debug
9. Access the application in your web browser at http://localhost:5000.

## Testing
1. Make sure you have activated the virtual environment (if not already activated):
    ```bash
    source venv/bin/activate
2. Run the unit tests using the following command:
    ```bash
    python -m unittest discover -v




