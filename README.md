# ML-PT

Welcome to ML-PT! This is a project aimed at demonstrating the use of an ML Model on User Personality Test answers. Below you'll find instructions on how to set up the project locally for development or testing purposes.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/theboyisred/ML-Project.git
cd ML-Project
```

### 2. Create a Virtual Environment (Optional but Recommended)

On macOS and Linux:

```bash
python3 -m venv venv
```

On Windows:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment (Optional but Recommended)

On macOS and Linux:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Perform Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser (Optional)

You can create a superuser to access the Django admin panel.

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Visit `http://127.0.0.1:8000` in your web browser to access the application.

## Project Structure

- **ML-PROJECT/**: Main project directory.
  - **backend/**: Django project settings and configurations.
  - **Main/**: Directory for Django apps.
    - **admin.py**: This is the file where we store information and settings related to our Admin Panel.
    - **models.py**: This is the file where we create models that represent a table in the database. E.g The Job Model represents a table called `job` in the database.
    - **preprocessing.py**: This file houses the ML Model and contains the function that generates the graph for the result.
    - **tasks.py**: Contains the `run_ML` and the `trigger_async_task` function that we use to run our ML.
    - **urls.py**: Contains the definitions for the different routes of the application.
    - **utils.py**: Contains the Utility Functions for the application.    
    - **views.py**: Server-side logic including the request handling, data storage from forms, calling the ML function, is handled here.    
    - **templates/**: Directory for HTML templates.
    - **partials/**: Directory for HTML that is shared across other templates. This includes the header and the layout.
    - **static/**: Directory for CSS, Javascript and Fonts.
  - **README.md**: This help text you are reading.
  - **requirements.txt**: Project requirements file.
  - **db.sqlite3**: Our SQLite3 Database File.
- **manage.py**: Django project management script.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature`)
6. Create a new Pull Request
