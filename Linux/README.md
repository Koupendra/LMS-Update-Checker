# LMS-Update-Checker

What Is This?
-------------

This is a Python application that gives a Desktop notification if any of the courses you enrolled in LMS has got updates.


How To Use This?
----------------

1. Download the project from this directory if you're using a Linux distribution.
2. Run `pip install -r requirements.txt` to install dependencies inside the project folder.
3. Run `python3 setup.py` and complete the setup.
4. Run `python3 main.py` (which is the acutal application).
5. You can start and run this application at specific time intervals by configuring Cronjobs.


NOTE
----

1. The `Config` file will contain your credentials for LMS, so make sure it's inaccessible by others.
2. The project is still in development, so it might have bugs.
3. Turn off "Focus Assist" or "Do not Disturb" mode to receive notifications.
