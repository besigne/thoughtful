from robocorp.tasks import task
from Worker.Scrapper import Scrapper


@task
def challenge():
    scrapper = Scrapper()
    scrapper.run()
    