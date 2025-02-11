# Learning Platform Project

This is a Django-based learning platform that provides features for tutorials, challenges, community interaction, and user management.

## Project Structure

```
myproject/
├── accounts/            # User authentication and profile management
├── community/           # Community features and interactions
├── core/               # Core functionality and shared components
├── forum/              # Discussion forum functionality
├── myproject/          # Main project configuration
├── static/             # Static files (CSS, JS, images)
│   └── css/
│   └── styles/
├── staticfiles/        # Collected static files for production
├── templates/          # HTML templates
│   ├── forum/
│   ├── styles/
│   └── base.html
└── manage.py          # Django management script
```

## Main Components

### 1. Core Application (`core/`)
- Contains essential functionality shared across the platform
- Manages basic site configuration and shared utilities

### 2. Accounts System (`accounts/`)
- Handles user authentication and authorization
- Manages user profiles and account settings
- Custom views and forms for user management
- URLs defined in `accounts/urls.py`

### 3. Community Features (`community/`)
- Manages community interactions and social features
- Includes community pages and user interactions
- Styled with `templates/styles/community.css`

### 4. Forum System (`forum/`)
- Provides discussion forum functionality
- Features post listing (`post_list.html`) and detailed views (`post_detail.html`)
- Allows users to create and interact with discussion threads

### 5. Templates Structure
- `base.html`: Base template that other templates extend
- `dashboard.html`: User dashboard interface
- `challenge.html`: Coding challenges interface
- `tutorials.html`: Learning tutorials section
- `index.html`: Main landing page
- `community.html`: Community interaction pages

### 6. Static Files
- CSS files organized by feature:
  - `challenge.css`: Styles for coding challenges
  - `dashboard.css`: Dashboard styling
  - `main.css`: Global styles
  - `tutorials.css`: Tutorial page styling

## Frontend Structure

The frontend is organized with a component-based approach:
- Each major section has its own template file
- Corresponding CSS files in `static/css/` and `templates/styles/`
- Modular design for easy maintenance and updates

## Configuration

- Project settings are in `myproject/settings.py`
- Uses SQLite database by default (`db.sqlite3`)
- Static files are served from `static/` and collected to `staticfiles/`
- Templates are located in the `templates/` directory

## Getting Started

1. Clone the repository
2. Install dependencies (requirements.txt)
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Run the development server: `python manage.py runserver`

## Contributing

When contributing to this project:
1. Follow the existing file structure
2. Place new templates in the appropriate subdirectory
3. Add corresponding CSS in the relevant style files
4. Update this README when adding new major features

## URL Structure

- Main URLs configured in root `urls.py`
- Account-related URLs in `accounts/urls.py`
- Forum URLs managed by the forum app
- Community features have their own URL patterns

## Static Files Management

- Development: Files served from `static/`
- Production: Files collected to `staticfiles/`
- Run `python manage.py collectstatic` before deployment

## Security Notes

- Debug mode should be disabled in production
- Secret key should be properly configured
- Follow Django's deployment checklist 