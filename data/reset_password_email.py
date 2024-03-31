from flask import render_template_string, url_for
from flask_mailman import EmailMessage

from static.message.reset_password_email_html_content import reset_password_email_html_content


def send_reset_password_email(user, app):
    reset_password_url = url_for(
        "reset_password",
        token=user.generate_reset_password_token(app),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    message = EmailMessage(
        subject="Reset your password",
        body=email_body,
        to=[user.email]
    )
    message.content_subtype = "html"

    message.send()
