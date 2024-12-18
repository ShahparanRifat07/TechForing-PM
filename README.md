# TechForing-PM Project Setup

This guide provides step-by-step instructions to set up and run the this project locally.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.10+
- pip
- virtualenv
- Git

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ShahparanRifat07/TechForing-PM.git
cd TechForing-PM
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate   
# On Windows: source venv/Scripts/activate
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

Replace `your-secret-key` with a securely generated Django secret key. You can generate one [here](https://djecrety.ir/).

### 5. Apply Migrations

Run the following commands to set up the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser

To access the Django admin panel, create a superuser:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up the admin credentials.

### 7. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The server will start at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

### 8. Access the API Documentation

Swagger API documentation is available at:

```
http://127.0.0.1:8000/docs/
```


## Additional Notes


### Authentication

This project uses `JWT` for authentication. Include the `Authorization: Bearer <token>` header in your API requests.