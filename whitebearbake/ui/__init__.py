# Instantiate blueprint class
from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, session, url_for

bp = Blueprint('ui', __name__)

@bp.route('/', methods=['GET'])
def index():
    """ Index view """
    return render_template('index.html')