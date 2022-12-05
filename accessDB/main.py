from flask import Blueprint, current_app, flash, request, render_template, redirect, url_for
import json

__version__ = '0.1.0'


def test():
    liste = {"test" : "Bonjour"}
    return liste


class AccessDB(Blueprint):

    def __init__(self, name='accessDB', import_name=__name__, *args, **kwargs):
        Blueprint.__init__(self, name, import_name, template_folder='templates', *args, **kwargs)
        self.add_url_rule('/test', 'test', test, methods=['GET'])

    def register(self, app, options):
        try:
            Blueprint.register(self, app, options)
        except Exception:
            app.logger.error("init AccessDB on register is failed")
