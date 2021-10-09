from apscheduler.schedulers.background import BackgroundScheduler

from social_network_messages.scheduler import load_newsfeed_from_vk


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(load_newsfeed_from_vk.load_newsfeed, 'interval', days=1)
    scheduler.start()
