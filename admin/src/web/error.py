
from flask import render_template


def not_found(e):
    kwargs = {
        "error_name": "Ups... algo salio mal",
        "error_description": "Lo sentimos"
    }
    
    return render_template("error.html.jinja", **kwargs), 404