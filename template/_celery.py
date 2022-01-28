from template.config import Config
from celery import Celery


class MyCelery(Celery):

    def gen_task_name(self, name, module):
        if module.endswith('.tasks'):
            module = module[:-6]
        return super(MyCelery, self).gen_task_name(name, module)

app = MyCelery(
    'template',
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_RESULT_BACKEND,
)

app.autodiscover_tasks([
    'template.blueprints.home',
    'template.blueprints.users',
],
force=True)