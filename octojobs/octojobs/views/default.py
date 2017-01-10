"""Render views from configurations."""

# from pyramid.response import Response
from pyramid.view import view_config

from pyramid.httpexceptions import HTTPFound

from ..models import Job


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """On initial load, shows search bar. On query submit, loads results."""
    if request.method == 'POST':

        searchterm = request.POST['searchbar']

        # url = request.route_url('idea', idea='great', _query={'sort':'asc'})

        # url = '/results?search=' + searchterm

        return HTTPFound(location=request.route_url('results', _query={'search': searchterm}))
    return {}


@view_config(route_name='results', renderer='../templates/results.jinja2')
def result_view(request):
    """Generate result view."""
    # if request.method == 'GET':
    import pdb; pdb.set_trace()

    searchterm = request.GET.get('search') + '%'
    query = request.dbsession.query(Job).filter(Job.city.like(searchterm))

    return {'results': query}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Show basic about us view."""
    return {}
