from app import app

if __name__ == '__main__':
    DEBUG = True
    WSGI_OPTIONS = dict()

    if DEBUG:
        WSGI_OPTIONS['use_debugger'] = True
        WSGI_OPTIONS['use_reloader'] = False

    app.run(**WSGI_OPTIONS, debug=DEBUG)
