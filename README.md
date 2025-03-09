# Portfolio Website

A professional portfolio website built with Flask, featuring:

- Admin dashboard for content management
- Project showcase
- Skills and experience sections
- Contact form
- Resume upload/download
- Responsive design

## Features

- User authentication
- Project management
- Skills management
- Experience tracking
- Profile customization
- Resume handling
- Contact form

## Tech Stack

- Flask
- SQLAlchemy
- PostgreSQL/SQLite
- HTML/CSS (Tailwind CSS)
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-portfolio
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your own settings

5. Initialize the database:
```bash
python init_db.py
```

6. Run the application:
```bash
flask run
```

7. Access the website at `http://localhost:5000`

## Admin Access

After initializing the database, you can log in with the following credentials:
- Email: admin@example.com
- Password: admin123

## Project Structure

```
flask-portfolio/
├── app.py                  # Main application file
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── models/                 # Database models
│   ├── __init__.py
│   ├── user.py
│   ├── profile.py
│   ├── project.py
│   ├── category.py
│   ├── skill.py
│   └── experience.py
├── routes/                 # Route handlers
│   ├── __init__.py
│   ├── main.py
│   ├── auth.py
│   ├── admin.py
│   └── projects.py
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── images/
└── templates/              # HTML templates
    ├── layout.html
    ├── includes/
    ├── main/
    ├── auth/
    ├── admin/
    └── projects/
```

## Customization

### Profile Information
1. Log in as admin
2. Go to the Admin Dashboard
3. Click on "Edit Profile"
4. Update your personal information

### Adding Projects
1. Log in as admin
2. Go to the Admin Dashboard
3. Click on "Add Project"
4. Fill in the project details and save

### Adding Categories
1. Log in as admin
2. Go to the Admin Dashboard
3. Click on "Manage Categories"
4. Add new categories for your projects

## Technologies Used

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: Tailwind CSS, JavaScript, Font Awesome
- **Authentication**: OAuth (GitHub)
- **Editor**: CKEditor for rich text editing
- **Database**: SQLite (can be easily changed to PostgreSQL, MySQL, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Font Awesome](https://fontawesome.com/)
- [CKEditor](https://ckeditor.com/)
