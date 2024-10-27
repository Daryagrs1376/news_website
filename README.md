# News Website Backend

This project is the backend API for a news website built with Django. It provides endpoints for managing and delivering news articles, categories, users, and other content necessary for a news website.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies](#technologies)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [API Endpoints](#api-endpoints)
7. [Running Tests](#running-tests)
8. [Contributing](#contributing)
9. [License](#license)

## Project Overview
This project serves as the backend for a news portal, handling all CRUD operations (Create, Read, Update, Delete) for news articles, categories, users, and comments. The backend is developed using Django and Django REST Framework, which provides APIs for frontend integration.

## Features
- **User Authentication**: Registration, login, and token-based authentication
- **Article Management**: CRUD operations for news articles
- **Category Management**: Organizing articles by category
- **Commenting System**: Adding comments to articles
- **Search and Filter**: Search articles by title and filter by category
- **Admin Panel**: Django Admin for managing the site content

## Technologies
- **Backend**: Django, Django REST Framework
- **Database**: SQLite (default, can be configured for PostgreSQL/MySQL)
- **Authentication**: Token-based authentication using Django REST Framework's authentication system
- **Environment Management**: Python virtual environment

## Installation
Follow these steps to set up and run the project locally.

### Prerequisites
- Python 3.x installed
- Git installed (optional)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/news_website_backend.git
   cd news_website_backend
