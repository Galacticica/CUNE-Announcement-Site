# CUNE Announcements
## What Is It?
It is a site in which CUNE students and faculty can submit announcements to be displayed during chapel and praise. The announcements are then sent to the proper channels to be added.

## Usage
#### Cloning Down The Code
1. Run ```gh repo clone Galacticica/CUNE-Announcement-Site```
2. Run ```uv sync```
3. Run ```uv run manage.py migrate```
4. Add a ```.env``` file and add the following:
     ```
     DEBUG = 1
     SECRET_KEY = whatever you want
     EMAIL_KEY = whatever
     ```

#### Run Locally
1. In the terminal, run ```uv run manage.py runserver```

## Contact
### Email : reaganzierke@gmail.com
### Discord : galacticica

