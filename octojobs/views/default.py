"""Render views from configurations."""

from pyramid.view import view_config
from sqlalchemy import or_, and_

from pyramid.httpexceptions import HTTPFound, HTTPNotFound

from ..models import Job


@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    """On initial load, shows search bar. On query submit, loads results."""
    if request.method == 'POST':

        searchterm = request.POST['searchbar']
        location = request.POST['location']

        query = {}

        if not location and searchterm:
            query['search'] = searchterm
            return redirect_search(request, query)

        elif not searchterm and location:
            query['location'] = location
            return redirect_search(request, query)

        elif searchterm and location:
            query['location'] = location
            query['search'] = searchterm
            return redirect_search(request, query)

        else:
            return {'results': 'no result'}

    return {}

def redirect_search(request, query):
    """Function to redirect to result page."""
    return HTTPFound(location=request.route_url('results', _query=query))


@view_config(route_name='results', renderer='../templates/results.jinja2')
def result_view(request):
    """Generate results view."""

    if request.GET.get('search'):
        searchterm = '%' + request.GET.get('search') +'%'
    else:
        searchterm = None

    if request.GET.get('location'):
        location = '%' + request.GET.get('location') +'%'
    else:
        location = None


    field_category = [Job.title, Job.company, Job.description]

    if request.method == 'GET':
        if location and searchterm:
            for field in field_category:
                qr = request.dbsession.query(Job).filter(and_(Job.city.ilike(location), field.ilike(searchterm)))
                if qr.count() > 0:
                    query = request.dbsession.query(Job).filter(and_(Job.city.ilike(location), field.ilike(searchterm)))
                break
            return {'failed_search': 'No results'}

        elif searchterm and location is None:
            field_category.append(Job.city)
            for field in field_category:
                qr = request.dbsession.query(Job).filter(field.ilike(searchterm))
                if qr.count() > 0:
                    query = request.dbsession.query(Job).filter(field.ilike(searchterm))
                break
            return {'failed_search': 'No results'}

        elif location and searchterm is None:
            qr = request.dbsession.query(Job).filter(Job.city.ilike(location))
            if qr.count() > 0:
                query = request.dbsession.query(Job).filter(Job.city.ilike(location))
            return {'failed_search': 'No results'}

    if request.method == 'POST':

        searchterm = request.POST['searchbar']
        location = request.POST['location']

        query = {}

        if not location and searchterm:
            query['search'] = searchterm
            return redirect_search(request, query)

        elif not searchterm and location:
            query['location'] = location
            return redirect_search(request, query)

        elif searchterm and location:
            query['location'] = location
            query['search'] = searchterm
            return redirect_search(request, query)

        else:
            return {'results': 'no result'}

    return {'results': query}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Show basic about us view."""
    return {}
