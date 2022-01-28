from datetime import datetime
from bson.json_util import dumps
from urllib.parse import urlparse
from celery import (
    chain
)
from template.extensions import celery
from template.tasks.base import BaseTask
from template.database import database_session



def search_task_chain(search_string: str, user: dict = {}):
    return chain(
        celery.signature('search.save_search', args=[search_string], kwargs={'user': user})
    )

@celery.task(name='search.save_search', base=BaseTask)
def save_search(
    search_string: str,
    **kwargs
    ):
    record = database_session.database.search.find_one_and_update(
        {'value': search_string},
        {
            '$currentDate': {'last_searched': True},
            '$setOnInsert': {'first_searched': datetime.now()},
            '$addToSet': {'users': kwargs.get('user')}
        },
        upsert=True
    )
    return dumps(record)
