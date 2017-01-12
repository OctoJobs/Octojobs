"""Render views from configurations."""

from pyramid.view import view_config
from sqlalchemy import and_

from pyramid.httpexceptions import HTTPFound

from ..models import Job


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """On initial load, shows search bar. On query submit, loads results."""
    if request.method == 'POST':

        return post_request(request)

    return {}


def redirect_search(request, query):
    """Function to redirect to result page."""
    return HTTPFound(location=request.route_url('results', _query=query))


def post_request(request):
    """If post request on form, collect search terms."""
    keyword = request.POST['searchbar']
    location = request.POST['location']

    search_terms = {}

    if not location and keyword:
        search_terms['search'] = keyword
        return redirect_search(request, search_terms)

    elif not keyword and location:
        search_terms['location'] = location
        return redirect_search(request, search_terms)

    elif keyword and location:
        search_terms['location'] = location
        search_terms['search'] = keyword
        return redirect_search(request, search_terms)

    else:
        return {'no_query': 'no result'}


@view_config(route_name='results', renderer='../templates/results.jinja2')
def result_view(request):
    """Generate results view."""
    if request.method == 'POST':

        return post_request(request)

    try:
        searchterm = '%' + request.GET.get('search') + '%'
    except TypeError:
        searchterm = None

    try:
        location = '%' + request.GET.get('location') + '%'
    except TypeError:
        location = None

    field_category = [Job.title, Job.company, Job.description]
    db_query = request.dbsession.query(Job)

    # if request.method == 'GET':

    if location and searchterm:

        for field in field_category:
            filter_query = db_query.filter(and_(
                Job.city.ilike(location),
                field.ilike(searchterm)
            ))
            if filter_query.count() > 0:
                search_hit = filter_query
                break

            return {'failed_search': 'No results'}

    elif searchterm and location is None:
        field_category.append(Job.city)

        for field in field_category:
            filter_query = db_query.filter(field.ilike(searchterm))
            if filter_query.count() > 0:
                search_hit = filter_query
                break

            return {'failed_search': 'No results'}

    elif location and searchterm is None:
        filter_query = db_query.filter(Job.city.ilike(location))

        if filter_query.count() > 0:
            search_hit = filter_query
        else:
            return {'failed_search': 'No results'}

    return {'results': search_hit}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Show basic about us view."""
    return {}
