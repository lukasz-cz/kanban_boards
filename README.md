# Kanban Boards

Flask application for Kanban boards management.

## Features

- Task management with drag-and-drop functionality
- User authentication and management
- Secure password storage with Argon2
- Configuration management with YAML

## Requirements

- Python 3.7+
- Flask
- Flask-PyMongo
- Flask-Login
- Flask-Argon2
- PyYAML

## Install on Linux

1. Clone the repository:
    ```bash
    git clone https://github.com/lukasz-cz/kanban_boards.git
    cd kanban_boards
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv flask-env
    source flask-env/bin/activate
    ```

3. Install the required packages:
    ```bash
    python3 -m pip install -r requirements.txt
    ```

4. Configure the application:

    - Copy example configuration file from the `config/` directory:
        ```bash
        cp config/example.yaml config/local.yaml
        ```

    - Edit the `config/local.yaml` file to match your setup.

5. Set the `FLASK_CONFIG` environment variable:
    ```bash
    export FLASK_CONFIG=production
    ```

## Run the App

1. Run the application:
    ```bash
    python3 run.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

## Usage

- Sign up, log in and manage your tasks using the drag-and-drop interface.
- Update your profile, reset your password, or delete your account from the profile page.

## License

This project is licensed under the MIT License.
