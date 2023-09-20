# Project_TokioSchool

# Gaming User Management System

A simple yet powerful Flask-based application tailored for user authentication, profile management, and game activity tracking. Especially designed for gaming communities, it comes with specialized features to handle game metrics and user ranking.


## Features

- **User Authentication**: Secure registration and login system.
- **Profile Management**: View and manage personal gaming statistics.
- **Game Tracking**: Keep track of games played and view metrics.
- **Admin Functions**: User management, metrics visualization, and user ranking adjustments.

## Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/rafu6891/Project_TokioSchool
    ```

2. Navigate to the project directory:
    ```bash
    cd gaming-user-management
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt   
    ```

4. Run the application:
    ```bash
    python app.py
    ```

The application should now be running on `http://127.0.0.1:5000/`.

## Usage

1. **Homepage**: Access the application's homepage on `http://127.0.0.1:5000/`.
2. **Signup**: Register a new user via `/signup`.
3. **Login**: Authenticate a user via `/login`.
4. **Profile**: View the authenticated user's game statistics at `/profile`.

Admin functions can be accessed through the `/admin` routes.

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

