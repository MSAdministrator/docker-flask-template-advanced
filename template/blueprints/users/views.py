# app/blueprints/users/views.py
from datetime import datetime
from werkzeug.urls import url_parse
from flask import (
    render_template, 
    url_for, 
    redirect, 
    flash, 
    request
)
from flask_login import (
    login_user, 
    logout_user, 
    login_required, 
    current_user
)
from template.blueprints.users import blueprint
from template.blueprints.users.models import User
from template.blueprints.users.tasks import send_email
from template.blueprints.users.forms import (
    LoginForm, 
    RegisterForm, 
    PasswordResetForm,
    PasswordResetRequestForm,
    ChangeEmailForm
)


def generate_email_template(template_path, **kwargs):
    """Generates email templates based on defined templates

    You can find these templates in the templates/email directory

    Args:
        template_path (str): Path to the desired email template

    Returns:
        dict: A dictionary containing the rendered templates in html and text
    """
    return {
        'text_body': render_template(template_path + '.txt', **kwargs),
        'html_body': render_template(template_path + '.html', **kwargs)
    }


@blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        current_user.last_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        current_user.save()


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.members'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            username=form.username.data, 
            email=form.email.data)
        user.set_password(form.password.data)
        user.save()
        email_templates = generate_email_template(
            'users/email/confirm',
            user=user.get_json(),
            token=user.generate_token('register-new-user')
        )
        send_email.apply_async(
            args=[
                user.email, 
                'Confirm your Lophi.us account!'
            ],
            **email_templates
        )
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('user_bp.login'))
    return render_template('users/register.html', title='Register', form=form)


@blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('users/unconfirmed.html')


@blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('user_bp.profile'), username=current_user.username)
    if current_user.decode_token(token, 'register-new-user'):
        flash('You have confirmed your account. Thanks!')
        return redirect(url_for('user_bp.login'))
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('home_bp.home'))


@blueprint.route('/confirm')
@login_required
def resend_confirmation():
    email_templates = generate_email_template(
            'users/email/confirm',
            user=current_user.get_json(),
            token=current_user.generate_token('register-new-user')
        )
    send_email.apply_async(
            args=[current_user.email, 'Confirm your Lophi.us account!'],
            **email_templates
        )
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('user_bp.profile', username=current_user.username))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user_bp.login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('user_bp.profile', username=user.username)
        return redirect(next_page)
    return render_template('users/login.html', title='Sign In', form=form)


@blueprint.route("/users/<username>")
@login_required
def user_username(username):
    return redirect(url_for('user_bp.profile'))


@blueprint.route('/profile')
@login_required
def profile():
    return render_template("users/profile.html", user=current_user)


@blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out. Bye!", "success")
    return redirect(url_for("home_bp.home"))


@blueprint.route("/change-password", methods=['GET','POST'])
@login_required
def change_password():
    form = PasswordResetForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Invalid password')
            return redirect(url_for('user_bp.login'))
        current_user.set_password(form.new_password.data)
        current_user.save()
        flash('Congratulations, you have successfully reset your password!')
        return redirect(url_for('user_bp.members'))
    return render_template('users/change_password.html', title='Reset Password', form=form)


@blueprint.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous():
        return redirect(url_for('home.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user:
            email_templates = generate_email_template(
                'users/email/reset_password',
                user=current_user.get_json(),
                token=current_user.generate_token('password-reset-request')
            )
            send_email.apply_async(
                args=[current_user.email, 'Reset your password!'],
                **email_templates
            )
            flash('An email with instructions to reset your password has been sent to you.')
            return redirect(url_for('user_bp.login'))
    return render_template('users/reset_password.html')


@blueprint.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous():
        return redirect(url_for('home.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            return redirect(url_for('home.index'))
        if user.decode_token(token, 'password-reset-request') and user.check_password(form.current_password.data):
            user.set_password(form.new_password.data)
            flash('Your password has been updated.')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('home.index'))
    return render_template('users/reset_password.html', form=form)


@blueprint.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.check_password(form.password.data):
            new_email = form.email.data
            email_templates = generate_email_template(
                'users/email/change_email',
                user=current_user.get_json(),
                token=current_user.generate_token(new_email)
            )
            send_email.apply_async(
                args=[new_email, 'Confirm your email address'],
                **email_templates
            )
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('home.index'))
        else:
            flash('Invalid email or password.')
    return render_template("users/change_email.html", form=form)


@blueprint.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('home.index'))
