from robocorp.tasks import task
from worker import Worker

@task
def minimal_task():
    bot = Worker("https://www.cbsnews.com/")
    bot.open_browser()
    bot.click_search_icon()
    bot.type_search_string()