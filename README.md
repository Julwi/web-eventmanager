<!-- ABOUT THE PROJECT -->
## About The Project

I wanted to use the knowledge I had acquired to build a kind of event manager that helps people keep track of important things. I was inspired by people from my social environment.

To do this, you register with the web app and log in to your account. After that you will get an overview page with all events entered, you can add new events using a form and will be notified with an alarm when events are due. Already registered events can be edited and deleted on the overview page. Finally, finished events are inserted into an archive.



### Built With
* [Bootstrap](https://getbootstrap.com)
* [JQuery](https://jquery.com)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [WTForms](https://wtforms.readthedocs.io/en/2.3.x/)
* [APScheduler](https://apscheduler.readthedocs.io/en/stable/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

<!-- GETTING STARTED -->
## Getting Started

Before running this project you need to install the packages from the requirement.txt file.
If you prefer a virtual environment you should create and activate this one before installing the packages.

```sh
pip install requirements.txt
```

To run the application simply run the following code in your terminal.

```sh
python run.py
```

By default the debug mode is turned off. If you would like to change that set debug=True in the run.py file.