
# MyBlogs

MyBlogs is a blogging platform built using Django, Jinja, and Django Rest Framework (DRF). The platform allows users to register, log in, and create their own blogs. Users can edit and delete only their own blogs, while all users can read others' blogs without logging in.

## Features

- User registration and login
- Create, edit, and delete own blogs
- View others' blogs without authentication
- RESTful API with DRF

## Requirements

- Python 3.8+
- Django 5.x
- Django Rest Framework 3.x

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Snoolf2002/myBlog.git
   cd myBlog
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

   Visit `http://127.0.0.1:8000/` to access the site.

## API Endpoints

The project provides a RESTful API built with Django Rest Framework:

- **GET /api/blogs/** - Get all blogs with optional filters (start_date, end_date, tag, username, first_name, last_name)
- **POST /api/blogs/** - Create a new blog (authentication required)
- **GET /api/blogs/{id}/** - Get specific blog
- **PUT /api/blogs/{id}/** - Update a blog (only if the blog belongs to the user)
- **DELETE /api/blogs/{id}/** - Delete a blog (only if the blog belongs to the user)


## Usage

- Users can register and log in to the platform.
- Once logged in, users can create new blogs and manage their own posts.
- All users (authenticated or not) can read any blog posts.
- The platform uses Jinja for the frontend templates.

## Authentication

- User authentication is managed through Django's default user model.
- API authentication is handled using JSON Web Tokens (JWT).

## Contributing

If you'd like to contribute to MyBlogs, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.