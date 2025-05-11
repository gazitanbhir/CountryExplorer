# Country Explorer 🌍

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-3.2%2B-green.svg)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/DRF-3.12%2B-red.svg)](https://www.django-rest-framework.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a Django-based web application developed for the Code Fusion AI Python Developer Assignment. It fetches comprehensive country data from an external API, stores it in a database, provides RESTful APIs for data interaction, and displays the information on a simple, secured web page.

## 📋 Table of Contents

1.  [🌟 Overview](#-overview)
2.  [✨ Features](#-features)
    *   [Phase 1: Data Fetching and Storage](#phase-1-data-fetching-and-storage)
    *   [Phase 2: RESTful API Development](#phase-2-restful-api-development)
    *   [Phase 3: Web Interface](#phase-3-web-interface)
    *   [Phase 4: Authentication and Security](#phase-4-authentication-and-security)
3.  [🛠️ Tech Stack](#️-tech-stack)
4.  [📁 Project Structure](#-project-structure)
5.  [🚀 Prerequisites](#-prerequisites)
6.  [⚙️ Setup and Installation](#️-setup-and-installation)
    *   [1. Clone the Repository](#1-clone-the-repository)
    *   [2. Create and Activate a Virtual Environment](#2-create-and-activate-a-virtual-environment)
    *   [3. Install Dependencies](#3-install-dependencies)
    *   [4. Database Setup](#4-database-setup)
    *   [5. Fetch Initial Country Data](#5-fetch-initial-country-data)
    *   [6. Create a Superuser](#6-create-a-superuser)
7.  [▶️ Running the Application](#️-running-the-application)
8.  [🔗 Accessing the Application](#-accessing-the-application)
    *   [Web Interface](#web-interface-1)
    *   [API Endpoints](#api-endpoints-1)
    *   [Admin Interface](#admin-interface)
9.  [🔌 API Endpoint Details](#-api-endpoint-details)
10. [🖼️ Screenshots (Placeholder)](#️-screenshots-placeholder)
11. [📄 License](#-license)

## 🌟 Overview

The Country Explorer application serves as a demonstration of backend development skills using Django. It integrates with the `restcountries.com` API to gather detailed information about countries worldwide. This data is then made accessible through a set of RESTful APIs and a user-friendly web interface, both secured with authentication.

Key functionalities include:
*   Fetching and storing country data.
*   Providing CRUD operations for country data via APIs.
*   Offering specialized API endpoints for regional and language-based country searches.
*   A searchable web interface for authenticated users to browse country information.

## ✨ Features

The project was developed in distinct phases, each adding core functionalities:

### Phase 1: Data Fetching and Storage
*   **Django Project & App:** A Django project named `country_explorer` with a core app `countries_api`.
*   **Data Source:** Fetches data from `https://restcountries.com/v3.1/all`.
*   **Data Modeling:** A comprehensive `Country` model (`countries_api/models.py`) stores diverse attributes like names, official codes (CCA2, CCA3, CCN3), capital cities, region, subregion, population, languages (as JSON), currencies (as JSON), flag URLs, and many more details.
*   **Data Persistence:** A Django management command `fetch_countries` (`countries_api/management/commands/fetch_countries.py`) is implemented to:
    *   Fetch data from the external API.
    *   Clean and process the received JSON data.
    *   Store or update country records in the SQLite database, using `cca2` as the unique identifier.

### Phase 2: RESTful API Development
Built using Django REST Framework, the API provides endpoints for:
*   `GET /api/countries/`: List all countries (paginated) or search by name.
*   `POST /api/countries/`: Create a new country entry.
*   `GET /api/countries/{cca2}/`: Retrieve details of a specific country by its CCA2 code.
*   `PUT /api/countries/{cca2}/`: Update an existing country's details.
*   `PATCH /api/countries/{cca2}/`: Partially update an existing country's details.
*   `DELETE /api/countries/{cca2}/`: Delete an existing country.
*   `GET /api/countries/{cca2}/regional-countries/`: List countries in the same region as the specified country.
*   `GET /api/countries/by-language/?lang_code={code}`: List countries where a specific language (e.g., 'eng' for English) is spoken.
*   All API endpoints are protected and require user authentication.

### Phase 3: Web Interface
A simple web interface for authenticated users:
*   **Country Listing:** Displays a paginated table with key country details: Name, CCA2 Code, Capital(s), Population, Timezone(s), and Flag.
*   **Search Functionality:** A search bar to filter countries by their common name, official name, or CCA2 code.
*   **Styling:** Basic HTML structure with Django Template Language. The assignment suggested Bootstrap/Bulma; the current implementation is minimal but functional.
*   **Data Rendering:** Uses Django's server-side template rendering (`countries_api/country_list.html`).
*   **Details Placeholder:** The assignment mentions a "Details" button for regional/language info. The APIs for this exist; the button's client-side logic in the template is a potential future enhancement.

### Phase 4: Authentication and Security
*   **API Security:** All endpoints under `/api/` are secured using Django REST Framework's `SessionAuthentication`, `BasicAuthentication`, and `IsAuthenticated` permission class. Only logged-in users can access the API.
*   **Web Security:** The country list page (`/web/countries/`) is protected and requires user login.
*   **Authentication System:** Utilizes Django's built-in authentication system (`django.contrib.auth`).
*   **Login/Logout:** Standard Django login (`/login/`) and logout (`/logout/`) views are provided.

## 🛠️ Tech Stack

*   **Backend Framework:** Python 3.x, Django (version used: see `requirements.txt`)
*   **REST API:** Django REST Framework
*   **Database:** SQLite (default, configurable in `settings.py`)
*   **HTTP Client:** `requests` library (for external API communication)
*   **Templating:** Django Template Language (DTL)
*   **Version Control:** Git

## 🚀 Prerequisites

Before you begin, ensure you have met the following requirements:
*   Python (3.8 or higher recommended)
*   `pip` (Python package installer)
*   `git` (for cloning the repository)

## ⚙️ Setup and Installation

Follow these steps to get your development environment set up:

### 1. Clone the Repository

```bash
git clone https://github.com/<your-github-username>/<your-repository-name>.git
cd <your-repository-name> # Should be CF-AI or similar
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
IGNORE_WHEN_COPYING_END

(Replace <your-github-username>/<your-repository-name> with the actual path to your repository)

2. Create and Activate a Virtual Environment

Using a virtual environment is highly recommended to manage project dependencies in isolation.

On macOS and Linux:

python3 -m venv venv
source venv/bin/activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

On Windows:

python -m venv venv
.\venv\Scripts\activate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
3. Install Dependencies

The project dependencies are listed in requirements.txt. (If requirements.txt is not present in the root, create one with the content below, or generate it using pip freeze > requirements.txt from your working development environment).

Example requirements.txt:

Django>=3.2,<4.3
djangorestframework>=3.12,<3.15
requests>=2.25,<2.32
# Add other dependencies if any, e.g., Pillow for image fields if used
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Txt
IGNORE_WHEN_COPYING_END

Install them using pip:

pip install -r requirements.txt
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
4. Database Setup

Apply the database migrations to create the necessary tables, including the Country model schema.

python manage.py migrate
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END
5. Fetch Initial Country Data

Run the custom management command to populate the database with country information from the restcountries.com API. This command can be run again to update existing data.

python manage.py fetch_countries
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

This process might take a few minutes depending on your internet connection and the API response time. You'll see console output indicating progress.

6. Create a Superuser

A superuser account is needed to access the Django admin interface and to log into the web application.

python manage.py createsuperuser
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

Follow the prompts to set a username, email address (optional), and a strong password.

▶️ Running the Application

Once the setup is complete, you can start the Django development server:

python manage.py runserver
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Bash
IGNORE_WHEN_COPYING_END

By default, the application will be accessible at http://127.0.0.1:8000/.

🔗 Accessing the Application
Web Interface

Root URL: http://127.0.0.1:8000/

If you are not authenticated, you will be redirected to the login page.

If authenticated, you will be redirected to the country list page (/web/countries/).

Login Page: http://127.0.0.1:8000/login/

Use the superuser credentials created earlier, or any other registered user's credentials.

Country List Page: http://127.0.0.1:8000/web/countries/

Displays a searchable and paginated list of countries. Requires login.

Logout: http://127.0.0.1:8000/logout/

API Endpoints

All API endpoints require authentication (Session or Basic Auth). You can use tools like Postman, Insomnia, or curl for testing.

Base API URL: http://127.0.0.1:8000/api/

See 🔌 API Endpoint Details for more.

Admin Interface

Admin Panel: http://127.0.0.1:8000/admin/

Log in with your superuser credentials to manage Country data and other Django models directly.

🔌 API Endpoint Details

The CountryViewSet in countries_api/views.py provides the following RESTful actions:

Method	Endpoint	Description
GET	/api/countries/	List all countries (paginated). Supports ?search= query param for name search.
POST	/api/countries/	Create a new country entry. Requires valid country data in the request body.
GET	/api/countries/{cca2}/	Retrieve details of a specific country using its 2-letter cca2 code.
PUT	/api/countries/{cca2}/	Update all fields of an existing country.
PATCH	/api/countries/{cca2}/	Partially update an existing country.
DELETE	/api/countries/{cca2}/	Delete a specific country.
GET	/api/countries/{cca2}/regional-countries/	List other countries in the same region as the specified country.
GET	/api/countries/by-language/?lang_code={lang_code}	List countries that speak a specific language (e.g., ?lang_code=eng).

All API responses are in JSON format. All endpoints require authentication.