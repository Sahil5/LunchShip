from auth import show_login, require_login
from flask import redirect, url_for, request, render_template, session
from flask.ext.login import current_user


def user_form_handler(form_class, template_name, get_username, data_handler, redirect_id):
    def handler(*args, **kwargs):
        form = form_class(request.form)

        if not form.validate():
            require_login()
            return render_template(
                template_name,
                form=form,
            )

        username = current_user.get_id()
        if not get_username(form) and not username:
            show_login()

        data_handler(get_username(form) or username, form, *args, **kwargs)

        if username:
            return redirect(url_for(redirect_id))
        else:
            # 204 No Content if from IRC bot
            return ('', 204)

    return handler
