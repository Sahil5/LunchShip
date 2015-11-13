from auth import render_login
from flask import redirect, url_for, request, render_template, session
from flask.ext.login import current_user


def handle_user_form(form, template_name, data_handler, success_redirect_view, *args, **kwargs):
    if not form.validate():
        if current_user.is_authenticated:
            if callable(template_name):
                return template_name()
            return render_template(
                template_name,
                form=form,
            )
        else:
            # 403 Invalid if from IRC bot
            return 'Invalid', 403

    username = current_user.get_id() or form.get_username()
    if not username:
        return render_login()

    data_handler(username, form, *args, **kwargs)

    if current_user.is_authenticated:
        return redirect(url_for(success_redirect_view))
    else:
        # 204 No Content if from IRC bot
        return '', 204

