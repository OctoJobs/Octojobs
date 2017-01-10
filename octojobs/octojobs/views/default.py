from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Job


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """On initial load, shows search bar. On query submit, loads results."""
    # If user presses submit button, load db query results:
    # try
        if request.method == 'POST':
            searchterm = request.POST['searchbar'] + '%'
            query = session.query(Job).filter(Job.city.like(searchterm))

    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    # Else, display searchbar
    return {}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Shows basic about us view."""
    return {}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_octojobs_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
