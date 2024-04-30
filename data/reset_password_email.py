from flask import render_template_string, url_for
from flask_mailman import EmailMessage
from static.message.reset_password_email_html_content import reset_password_email_html_content


def send_reset_password_email(user, config):
    reset_password_url = url_for(
        "users_function.reset_password",
        token=user.generate_token(config),
        user_id=user.id,
        _external=True,
    )

    # создаём сообщение
    email_body = render_template_string(
        reset_password_email_html_content, reset_password_url=reset_password_url
    )

    # отправляем сообщение
    message = EmailMessage(
        subject="Сброс пароля",
        body=email_body,
        to=[user.email]
    )
    message.content_subtype = "html"

    message.send()
