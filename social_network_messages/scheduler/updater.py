from apscheduler.schedulers.background import BackgroundScheduler

from social_network_messages.scheduler import load_newsfeed_from_vk
from social_network_messages.scheduler.workflow import workflow


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(load_newsfeed_from_vk.load_newsfeed, 'interval', days=1)
    scheduler.add_job(workflow, 'interval', hours=1)
    scheduler.start()
