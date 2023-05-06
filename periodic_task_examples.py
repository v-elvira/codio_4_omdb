# Task Signatures:
# Celery provides a Signature object that combined the task and arguments into a single object. 
# The Signature can then be executed, for example, by using delay()

def function_executor(fn, *args, **kwargs):								# variant 1
    return fn.delay(args, **kwargs)

function_executor(notify_of_new_search_term, "lord of the rings")		# way of calling


def signature_executor(s):	# a function that works on Signature objects instead # variant 2
    return s.delay()

task_signature = notify_of_new_search_term.s("lord of the rings")  # way of calling
signature_executor(task_signature)



# Types of add_periodic_task() first argument:

# int, sec, timedelta => repeatedly with this delay 
app.add_periodic_task(60.0, search_and_save.s("star wars"))  # (every minute)

# crontab
from celery.schedules import crontab

app.add_periodic_task(crontab(
    minute=30,
    hour=7,
    day_of_month=1
), search_and_save.s("star wars"))  # (at 7:30 AM on the first of the month) Units are * if not defined (=every)


# solar 
from celery.schedules import solar

app.add_periodic_task(
    solar("sunrise", -36.848461, 174.763336),	# at sunrise in Auckland, New Zealand
    search_and_save.s("star wars")
)


# PeriodicTask:
# Before a PeriodicTask can be scheduled it must be associated with a schedule object. 
# The schedule for the PeriodicTask is set on one of the fields interval, crontab, solar or clocked, 
# which are related to the models IntervalSchedule, CrontabSchedule, SolarSchedule or ClockedSchedule, respectively. 
# Exactly one of these fields must be set, with the rest set to null.

schedule = IntervalSchedule(period=IntervalSchedule.MINUTES, every=30) # every 30 min

schedule = CrontabSchedule(minute="30", hour="7", day_of_month="1") # 7:30 AM on the first of each month
# crontab rules can be used: minute="*/15" (every 15 min), hour="1,3,5,7,9,11,13,15,17,19,21,23", day_of_month="1-7"

# clocked_time: (DateTimeField) field. The PeriodicTask would therefore only run once (ClockSchedule)


# Example: 
# to keep our database of movies about python up to date by searching for them every day
from django_celery_beat.models import IntervalSchedule

day_schedule, created = IntervalSchedule.objects.get_or_create(period=IntervalSchedule.DAYS, every=1)


from django_celery_beat.models import PeriodicTask
import json

args = json.dumps(["python"])					# so args should be json encoded (list, dir, str, numbers)

pt = PeriodicTask.objects.create(
    name="Daily python movie search",
    interval=day_schedule,						# because day_schedule is IntervalSchedule
    args=args,
    task="movies.tasks.search_and_save"
)

