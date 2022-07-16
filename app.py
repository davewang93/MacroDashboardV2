import dash

# bootstrap theme
# https://bootswatch.com/lux/

app = dash.Dash()

server = app.server
app.config.suppress_callback_exceptions = True