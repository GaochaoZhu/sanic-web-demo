class Config:
    """
    Basic config
    """
    # Application config
    FLAG = '~/flag/flag.csv'
    DEBUG = True

    @staticmethod
    def init_conf(app):
        app.static('static', '~/sanic_web/static')
        app.url_for("static", filename="css/steps.css")
        app.url_for("static", filename="js/steps.js")