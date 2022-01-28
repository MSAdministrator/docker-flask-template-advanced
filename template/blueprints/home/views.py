from flask import (
    render_template,
    url_for
)
from werkzeug.utils import redirect
from template.blueprints.home import blueprint
from template.blueprints.home.forms import IdeaSubmissionForm


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/home', methods=['GET', 'POST'])
def home():
    form = IdeaSubmissionForm()
    if form.validate_on_submit():
        # do something
        return redirect(url_for('home_bp.thanks'))
    return render_template('home/index.html', welcome='Docker Flask Template', form=form)


@blueprint.route('/thanks')
def thanks():
    return render_template('home/thanks.html')
