import logging
from celery import Task
from template.database import database_session


logger = logging.getLogger(__name__)


class BaseTask(Task):
    abstract = True

    def before_start(self, task_id, args, kwargs):
        # TODO: Add logic to save to database - especially for
        # attemped searches and tracking who searched for what
        print(f'task_id: {task_id}')
        print(f'args: {args}')
        print(f'kwargs: {kwargs}')

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.exception(str(einfo))
        logger.debug("Task_id {} failed, Arguments are {}".format(task_id, args))

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        database_session.client.close()
        return super().after_return(status, retval, task_id, args, kwargs, einfo)
