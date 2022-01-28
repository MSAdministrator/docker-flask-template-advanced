from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    SubmitField,
)
from wtforms.validators import (
    DataRequired, 
    Email, 
    Length, 
)


class IdeaSubmissionForm(FlaskForm):

    name = StringField(
        'Name', 
        validators=[DataRequired()]
    )
    email = StringField(
        'Email', 
        validators=[
            DataRequired(), 
            Email(), 
            Length(min=6, max=40)
        ]
    )
    org = StringField(
        'Organization', 
        validators=[
            DataRequired(),  
            Length(min=6, max=40)
        ]
    )
    feedback = StringField(
        'Feedback',
        validators=[
            DataRequired(),  
            Length(min=6, max=40)
        ]
    )
    submit = SubmitField('Submit')
