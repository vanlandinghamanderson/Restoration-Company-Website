# Restoration-Company-Website
A powerful, full-stack restoration application for StaDry Roofing and Restorations, built with Django.

## Description
This powerful full-stack restoration web application is called "StaDry Restorations", which built for a roofing and restoration company in Wilson, North Carolina. It provides an online presence where potential customers can learn about services, view gallery from past jobs, read company blog posts, and get in touch -- while giving the company a platform to showcase its work and generate leads.

**Main pages/features:**
- **Homepage** - overview and entry point to the site
- **Services** - details on the restoration services offered
- **Media** - photos/videos showcasing past work
- **About** - background on the company
- **Blog** - articles and company updates
- **Contact** - a way for vistiors to reach out the company

**Technology Stacks:**
- **Backend:** - Python (Django)
- **Frontend:** - HTML, CSS, JavaScript
- **Database:** - PostgreSQL
- **Deployment:** - AWS (coming soon)

## Installation
1. Clone the repository:
```bash
   git clone https://github.com/<your-username>/Restoration-Company-Website.git
   cd restoration-company-website
```
2. Create and activate a virtual enivronment:
```bash
   python -m venv venv
   source venv/bin/activate #On Windows: venv/Scripts/activate
```
3. Install dependencies:
``` bash
   pip install -r requirements.txt
```
4. Install python-dotenv for environment variables:
```bash
   pip install python-dotenv
```
5. Import the enviroment variable in your 'settings.py' file:
```bash
   from dotenv import load_dotenv
   import os
```
6. Set up environment variables (create a '.env' file):
```
   SECRET_KEY=your-secret-key
   DEBUG=True
   DB_NAME=your-database-name
   DB_USER=your-username
   DB_PASS=your-password
   DB_HOST=your-localhost
   DB_PORT=your-portnunber
```
7. Run migrations:
```bash
   python manage.py migrate
```
8. Run the development server:
```bash
   python manage.py runserver
```

## Usage
Once the development server is running, open your browser and go to:
``` bash
http://127.0.0.1:8000

To access the Django admin panel (for managing blog posts, media, services, gallery, the team, etc.)

Create a superuser:
```bash
python manage.py createsuperuser
```

Enter your username, email, and your password...

Then log in at:
```bash
http://127.0.0.1:8000/admin
```

## Contributing
This is currently a solo project built and maintained by me. That said, suggestions, bug reports, and pull requests are welcome - feel free to pen an issue if you spot something or have an idea for improvement.

## License
This project is not currently licensed for reuse. All rights reserved. You are welcome to view the code, but please do not copy, modify, or redistribute it without permission.
```


   
