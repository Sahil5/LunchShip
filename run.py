from app import app, ssl_context
import views

app.config['PROPAGATE_EXCEPTIONS'] = True
app.run('0.0.0.0', ssl_context=ssl_context)
