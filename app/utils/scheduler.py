from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def schedule_task(func, time_str, *args, **kwargs):
    hour, minute = map(int, time_str.split(':'))
    scheduler.add_job(func, 'cron', hour=hour, minute=minute, args=args, kwargs=kwargs)