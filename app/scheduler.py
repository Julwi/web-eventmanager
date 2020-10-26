import queue
from datetime import datetime
from time import localtime, strftime, strptime

from apscheduler.triggers.combining import OrTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

from app import app

# Event validation variables
events_completed = queue.Queue()
basis_seconds = datetime(1970, 1, 1)

# Trigger 
# trigger = OrTrigger([DateTrigger(), CronTrigger(minute="*")])

def schedule_jobs(events, current_jobs):
    """
    Checks for each event if a due date check is performed.
    If not a new job 'check_date' is created and started.

    Parameter:
    events (Event.query): Query that contains all events for current user.
    current_jobs (list): List that contains all jobs of the current apscheduler instance.
    """
    for event in events:

        # Check if job is already running
        job_running = False
        for job in current_jobs:
            if job.name == str(event.id):
                job_running = True
                continue
        
        # Continue or create job 'check_date' for event
        if job_running:
            continue
        else:
            print("Started jobs")
            app.apscheduler.add_job(func=check_date, trigger='cron', minute="*", args=[
                event.id, event.due_date], id=str(event.id))


def check_date(event_id, event_due_date):
    """
    Scheduled function to check event date every minute. 
    Passes the event id to global queue if event is completed.

    Parameters:
    event_id (str): Event id of respective event as a string.
    event_due_date (datetime.datetime): Scheduled datetime of event. 
    """
    completed = False

    # Get current time
    current_datetime = strftime("%m/%d/%Y %I:%M %p", localtime())
    time_current = datetime.strptime(current_datetime, "%m/%d/%Y %I:%M %p")

    # Check if event is in the past
    if (time_current-basis_seconds).total_seconds() >= (event_due_date-basis_seconds).total_seconds():
        completed = True
        events_completed.put(event_id)

    # Status
    print("Job for event id {} is alive. Event completed: {}." .format(
        event_id, completed))
