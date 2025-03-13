# SmartScout

SmartScout is a Smart Recruitment and Employee Management System designed to simplify the recruitment process for employees and employers alike.

## Tech Stack

- **Backend:** Django
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Other Libraries:** Tailwind CSS, Vanta.js

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Node.js (for frontend dependencies)
- SQLite (default database)

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/SmartScout.git
   cd SmartScout

2. **Create a virtual environment and activate it:**
    ```sh
      python -m venv venv
      venv\Scripts\activate  # On Windows
      source venv/bin/activate  # On macOS/Linux

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt

4. **Apply migrations:**
    ```sh
    python manage.py migrate

5. **Run the development server:**
    ```sh
    python manage.py runserver

6. **Open your browser and navigate to:**
    ```sh
    http://localhost:8000

## Endpoints

### Home
- **URL:** `/`
- **Method:** GET
- **Description:** Renders the home page.

### Employee

#### Home
- **URL:** `/employee/`
- **Method:** GET
- **Description:** Renders the employee home page.

#### Create Profile
- **URL:** `/employee/create/`
- **Method:** POST
- **Description:** Creates a new employee profile.

#### Get Jobs
- **URL:** `/employee/jobs/`
- **Method:** GET
- **Description:** Retrieves a list of active job postings.

### Manager

#### Home
- **URL:** `/manager/`
- **Method:** GET
- **Description:** Renders the manager home page.

#### Generate Recruitment Form
- **URL:** `/manager/forms/create/`
- **Method:** POST
- **Description:** Creates a new recruitment form.

#### Get Recruitment Forms
- **URL:** `/manager/forms/`
- **Method:** GET
- **Description:** Retrieves a list of recruitment forms.

### Admin

#### Home
- **URL:** `/myadmin/`
- **Method:** GET
- **Description:** Renders the admin home page.

#### Manage Managers
- **URL:** `/myadmin/manage_managers/`
- **Method:** GET
- **Description:** Retrieves a list of managers.

### Authentication

#### Register
- **URL:** `/myauth/register/`
- **Method:** POST
- **Description:** Registers a new user.

#### Login
- **URL:** `/myauth/login/`
- **Method:** POST
- **Description:** Authenticates a user.

#### Logout
- **URL:** `/myauth/logout/`
- **Method:** GET
- **Description:** Logs out the current user.

