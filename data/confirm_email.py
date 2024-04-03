from flask import render_template_string, url_for
from flask_mailman import EmailMessage
from static.message.confirm_email_html_content import confirm_email_html_content


def send_confirm_email(user, config):
    confirm_url = url_for(
        "users_function.confirm_email",
        token=user.generate_token(config),
        user_id=user.id,
        _external=True,
    )

    email_body = render_template_string(
        confirm_email_html_content, confirm_url=confirm_url
    )

    message = EmailMessage(
        subject="Подтверждение почты",
        body=email_body,
        to=[user.email]
    )
    message.content_subtype = "html"

    message.send()
