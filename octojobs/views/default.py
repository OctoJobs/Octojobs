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

        if not location and not searchterm:
            return {'results': 'no result'}

        elif not location and searchterm:
            return HTTPFound(
                location=request.route_url('results', _query={'search': searchterm})
            )

        elif not searchterm and location:
            return HTTPFound(
                location=request.route_url('results', _query={'location': location})
            )

        elif searchterm and location:
            return HTTPFound(
                location=request.route_url('results', _query={'search': searchterm, 'location': location})
            )

    return {}


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
        import pdb; pdb.set_trace()
        if location and searchterm:
            print("search started")
            for field in field_category:
                print("field when both filled", field)
                if request.dbsession.query(Job).filter(and_(Job.city.ilike(location), field.ilike(searchterm))):
                    query = request.dbsession.query(Job).filter(and_(Job.city.ilike(location), field.ilike(searchterm)))
                    break

        elif searchterm and location is None:
            field_category.append(Job.city)
            for field in field_category:
                print("field when location is none", field)
                if request.dbsession.query(Job).filter(field.ilike(searchterm)):
                    query = request.dbsession.query(Job).filter(field.ilike(searchterm))
                    break

        elif location and searchterm is None:
            if request.dbsession.query(Job).filter(Job.city.ilike(location)):
                query = request.dbsession.query(Job).filter(Job.city.ilike(location))

        else:
            print("hit the else / failed search")
            return {'failed_search': "No results"}


    if request.method == 'POST':

        searchterm = request.POST['searchbar']
        location = request.POST['location']

        return HTTPFound(
            location=request.route_url('results', _query={'search': searchterm, 'location': location})
        )
    return {'results': query}


@view_config(route_name='about', renderer='../templates/about.jinja2')
def about_view(request):
    """Show basic about us view."""
    return {}
