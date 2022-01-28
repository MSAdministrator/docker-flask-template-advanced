from flask import (
    render_template, 
    request,
)
from flask_login import current_user
from template.blueprints.search import blueprint
from template.blueprints.search.tasks import search_task_chain


@blueprint.route('/search', methods=['GET', 'POST'])
def search():
    if current_user.is_authenticated:
        user = current_user.json()
    else:
        user = {}
    if request.method == 'GET':
        # retrieve query from search form
        search_string = request.values.get('keyword')
        if search_string:
            # search_task_group saves the search in the database
            chain = search_task_chain(
                search_string=search_string,
                user=user,
                **user
            )
            task = chain()
            task.save()
            # waiting for tasks to complete before continuing
            task.join()
            if task.successful():
                return render_template('search/search.html', results=task.get())
    return render_template('search/search.html')
