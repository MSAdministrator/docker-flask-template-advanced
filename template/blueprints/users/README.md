# Users Blueprint

This document outlines the User model, tasks, forms, and views (endpoints).

## User Model

The User model contains the following list of attributes:

* name
* username
* email
* password
* registered_on - DateTime registration occurred
* confirmed - Whether or not the user has confirmed their registration
* confirmed_at - DateTime registration was confirmed
* last_seen - DateTime user was last seen on the site
* last_ip - The last IP address of the user
* is_admin - Whether or not the user has admin access
* is_authenticated - Whether or not the current user is authenticated
* is_active - Whether or not the user account is active
* avatar - A Gravatar url to the users photo based on their email address
* is_anonymous - Whether or not the user is anonymous

A User object also has the following methods avaiable:

* set_password
* check_password - Checks the entered password against a hash stored in the User object
* generate_token - Used for registration confirmation via email, resetting of users password via email, and changing of the users email address via email
* decode_token - Used to decode a token with the provided salt
* get_json - Gets the User object properties in JSON: name, username, email

## Users Views (Endpoints)

The following views are currently implemented for the Users blueprint:

* register - User registers via RegistrationForm and is sent an email to confirm
* unconfirmed - Displays whether the current User or anonymous user is not confirmed
* confirm/{token} - User received an email to confirm their account and is directed here - If the link has expired than we redirect them.
* confirm - Accessible via their profile page and allows them to send confirmation email again
* login - User login via the LoginForm and redirects them to their profile page
* users/{username} - Redirects the logged in user to their profile page
* profile - Displays the current logged in users profile dashboard
* logout - Logs out the current user
* change-password - Displays the PasswordResetForm for the logged in user and sets the users password if old password matches current password
* reset - Request that they reset their user account and by displaying the PasswordResetRequestForm. Send email with link to the reset/{token} 
* reset/{token} - Verifies the password reset request and allows the user to reset their password 
* change-email - Displays the ChangeEmailForm and sends an email to the user to the new email address with a link to change-email/{token}
* change-email/{token} - If verified then allows the logged in User to change their email address

## Users Forms

The following is a list of current Forms:

* PasswordResetRequestForm
    * email
    * submit
* ChangeEmailForm
    * email
    * password
    * submit
* PasswordResetForm
    * current_password
    * new_password
    * confirm
    * submit
* LoginForm
    * username
    * password
    * remember_me
    * submit
* RegistrationForm
    * name
    * username
    * email
    * password
    * confirm
    * submit

## Users Tasks

The following are the currently avialable tasks (sent to Redis for Celery worker to pick up):

* users.send_registration_confirmation_email

