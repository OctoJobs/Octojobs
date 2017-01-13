"""The test module for the Octojobs project."""

import faker
from octojobs.models import Job
from octojobs.models import get_tm_session
from octojobs.models.meta import Base
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
import pytest
import transaction


fake = faker.Faker()

DUMMY_JOBS = [Job(
    title=fake.job(),
    city=fake.city(),
    description=fake.text(100),
    company=fake.company(),
    url=fake.url()
) for i in range(10)]

KNOWN_JOB = Job(
    title="Python Developer",
    city="Seattle",
    description="3+ years of experience testing and writing test automation for desktop and web applications. Skilled with testing on multiple platforms. Knowledgeable about designing and implementing infrastructure and APIs for automated test systems. Strong familiarity of database concepts is a plus.",
    company="Python Coders",
    url="http://www.python-coders.com",
)

DUMMY_JOBS.append(KNOWN_JOB)


@pytest.fixture(scope="session")
def configuration(request):
    """Set up a Configurator instance.

    This Configurator instance sets up a pointer to the location of the
    database. It also includes the models from the octojobs model package.
    Finally it tears everything down, including the in-memory database.

    This configuration will persist for the entire duration of your PyTest run.
    """
    settings = {
        'sqlalchemy.url': 'postgres:///test_jobs'}
    config = testing.setUp(settings=settings)
    config.include('octojobs.models')
    config.include('octojobs.routes')

    def teardown():
        testing.tearDown()

    request.addfinalizer(teardown)
    return config


@pytest.fixture
def db_session(configuration, request):
    """Create a session for interacting with the test database.

    This uses the dbsession_factory on the configurator instance to create a
    new database session. It binds that session to the available engine
    and returns a new session for every call of the dummy_request object.
    """
    SessionFactory = configuration.registry['dbsession_factory']
    session = SessionFactory()
    engine = session.bind

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    def teardown():
        session.transaction.rollback()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(db_session):
    """It creates a fake HTTP Request and database session.

    This is a function-level fixture, so every new request will have a
    new database session.
    """
    return testing.DummyRequest(dbsession=db_session)


@pytest.fixture
def add_models(dummy_request):
    """Add a bunch of model instances to the database.

    Every test that includes this fixture will add jobs.
    """
    # dummy_request.dbsession.add_all(DUMMY_JOBS)

    dummy_request.dbsession.add_all(DUMMY_JOBS)


# ================ UNIT TESTS =======================

def test_new_jobs_are_added(db_session):
    """New Job objects get added to the database."""
    db_session.add_all(DUMMY_JOBS)
    query = db_session.query(Job).all()
    assert len(query) == len(DUMMY_JOBS)


def test_get_home_view_is_empty_dict(dummy_request):
    """Assert empty dict is returned, from Get request."""
    from octojobs.views.default import home_view
    assert home_view(dummy_request) == {}


def test_get_about_view_is_empty_dict(dummy_request):
    """Assert empty dict is returned, from Get request."""
    from octojobs.views.default import about_view
    assert about_view(dummy_request) == {}


def test_post_home_view_is_http_found(dummy_request):
    """Assert is instance of HTTP found, from POST request on home."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = home_view(dummy_request)

    assert isinstance(result, HTTPFound)


def test_post_result_view_is_http_found(dummy_request):
    """Assert is instance of HTTP found, from POST request on resultview."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = result_view(dummy_request)

    assert isinstance(result, HTTPFound)


def test_post_home_view_reroutes_with_url_query(dummy_request):
    """Assert search terms are passed on url when a post request."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = home_view(dummy_request)

    assert 'test' and 'seattle' in result.location


def test_post_home_view_with_only_location_query(dummy_request):
    """Test only one query with only location filled on url."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = "seattle"
    dummy_request.POST["searchbar"] = ""

    result = home_view(dummy_request)

    assert result.location == 'http://example.com/results?location=seattle'


def test_post_home_view_with_only_searchterm_query(dummy_request):
    """Test only one query with only search filled on url."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = "testing"

    result = home_view(dummy_request)

    assert result.location == 'http://example.com/results?search=testing'


def test_post_home_view_with_no_query(dummy_request):
    """Test no query dictionary is returned on the home when left empty."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = ""

    assert home_view(dummy_request) == {'no_query': 'no result'}


def test_post_result_view_reroutes_with_new_query(dummy_request):
    """Assert search terms passed on url on result view with both fields."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = result_view(dummy_request)

    assert 'test' and 'seattle' in result.location


def test_post_results_view_with_location_query(dummy_request):
    """Test only 1 query with only location filled on url for results form."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = "seattle"
    dummy_request.POST["searchbar"] = ""

    result = result_view(dummy_request)

    assert result.location == 'http://example.com/results?location=seattle'


def test_post_result_view_with_search_query_only(dummy_request):
    """Test only one query with only search filled on url for results form."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = "test"

    result = result_view(dummy_request)

    assert result.location == 'http://example.com/results?search=test'


def test_post_result_view_with_no_query(dummy_request):
    """Test no query dictionary is returned on the results when left empty."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = ""

    assert result_view(dummy_request) == {'no_query': 'no result'}


def test_result_query_on_get_request_bad_location(dummy_request,
                                                  db_session,
                                                  add_models):
    """Test bad get on location with no results returns failed."""
    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'location': 'Sydney'}

    results = result_view(dummy_request)

    assert results == {'failed_search': 'No results'}


def test_result_query_on_get_request_bad_search(dummy_request,
                                                db_session,
                                                add_models):
    """Test GET on search with bad results returns failed search dict."""

    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'location': 'Seattle', 'search': 'Plsdkjg'}

    results = result_view(dummy_request)

    assert results == {'failed_search': 'No results'}


def test_result_query_on_get_matched_location_search(dummy_request,
                                                     db_session,
                                                     add_models):
    """Test GET on location with results returned."""
    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'location': 'Seattle'}

    results = result_view(dummy_request)

    assert results['results'][0].city == 'Seattle'


def test_result_query_on_get_matched_search(dummy_request,
                                            db_session,
                                            add_models):
    """Test GET on keyword search with results returned."""
    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'search': 'Python'}

    results = result_view(dummy_request)

    assert results['results'][0].title == 'Python Developer'


def test_result_no_location_bad_search(dummy_request,
                                       db_session,
                                       add_models):
    """Test GET on bad keyword search with no location specified.

    Expect the return the failed search dictionary.
    """
    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'search': 'kjhgs'}

    results = result_view(dummy_request)

    assert results == {'failed_search': 'No results'}


def test_result_query_on_get_matched_search_and_location(dummy_request,
                                                         db_session,
                                                         add_models):
    """Test GET on keyword search with results returned."""
    from octojobs.views.default import result_view

    dummy_request.method = "GET"
    dummy_request.GET = {'search': 'Python', 'location': 'Seattle'}

    results = result_view(dummy_request)

    # import pdb; pdb.set_trace()

    assert results['results'][0].title == 'Python Developer'


# ============= FUNTIONAL TESTS =====================


@pytest.fixture(scope="session")
def testapp(request):
    """The fixture creates a test app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """The function returns a Pyramid WSGI application."""
        settings["sqlalchemy.url"] = 'postgres:///test_jobs'
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{})
    testapp = TestApp(app)

    SessionFactory = app.registry["dbsession_factory"]
    engine = SessionFactory().bind

    Base.metadata.create_all(bind=engine)

    def tear_down():
        Base.metadata.drop_all(bind=engine)

    request.addfinalizer(tear_down)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """It fills the database."""
    SessionFactory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(SessionFactory, transaction.manager)
        dbsession.add_all(DUMMY_JOBS)


def test_the_home_page_has_a_form(testapp):
    """The home page has 2 input boxes."""
    response = testapp.get('/', status=200)
    html = response.html
    assert html.find_all("form")


def test_the_results_page_has_a_form(testapp):
    """The results page has 2 input boxes."""
    response = testapp.get('/results?search=Python', status=200)
    html = response.html
    assert html.find_all("form")


def test_the_home_page_has_two_input_boxes(testapp):
    """The home page has 2 input boxes."""
    response = testapp.get('/', status=200)
    html = response.html
    searchbar = html.find("input", {"name": "searchbar"})
    location = html.find("input", {"name": "location"})
    assert searchbar and location


def test_the_results_page_has_two_input_boxes(testapp):
    """The results page has 2 input boxes."""
    response = testapp.get('/results?location=new+york', status=200)
    html = response.html
    searchbar = html.find("input", {"name": "searchbar"})
    location = html.find("input", {"name": "location"})
    assert searchbar and location


def test_results_page_has_no_title_id_in_results_section(testapp):
    """The results page has no title, if no query submitted."""
    response = testapp.get('/results?search=Python', status=200)
    html = response.html
    assert len(html.find_all("item")) == 0


def test_results_page_has_python_in_results_when_searched_on(testapp, fill_the_db):
    """The results page query with python in it renders python results page."""
    response = testapp.post("/results", params={
        "searchbar": "Python",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Python").count("Python") > 0


def test_home_page_has_python_in_results_when_searched_on(testapp, fill_the_db):
    """The home page query with python in it renders python results page."""
    response = testapp.post("/", params={
        "searchbar": "Python",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Python").count("Python") > 0

def test_results_page_has_api_in_results_when_description_searched_on(testapp, fill_the_db):
    """The results page query with api in it renders api results page."""
    response = testapp.post("/results", params={
        "searchbar": "API",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("API").count("API") > 0


def test_home_page_has_api_in_results_when_description_searched_on(testapp, fill_the_db):
    """The home page query with api in it renders api results page."""
    response = testapp.post("/", params={
        "searchbar": "API",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("API").count("API") > 0


def test_results_page_has_api_in_results_when_description_searched_on_and_no_location(testapp, fill_the_db):
    """The results page query with api in kw box, but no location renders api results page."""
    response = testapp.post("/results", params={
        "searchbar": "API",
        "location": ""
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("API").count("API") > 0


def test_home_page_has_api_in_results_when_description_searched_on_and_no_location(testapp, fill_the_db):
    """The home page query with api in kw box, but no location renders api results page."""
    response = testapp.post("/", params={
        "searchbar": "API",
        "location": ""
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("API").count("API") > 0


def test_results_page_has_seattle_in_results_when_searched_on(testapp, fill_the_db):
    """The results page query with seattle in it renders seattle results page."""
    response = testapp.post("/results", params={
        "searchbar": "Python",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Seattle").count("Seattle") > 0


def test_home_page_has_seattle_in_results_when_searched_on(testapp, fill_the_db):
    """The home page query with seattle in it renders seattle results page."""
    response = testapp.post("/", params={
        "searchbar": "Python",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Seattle").count("Seattle") > 0


def test_results_page_has_seattle_in_results_when_only_argument(testapp, fill_the_db):
    """The results page search on seattle only gives a seattle results page."""
    response = testapp.post("/results", params={
        "searchbar": "",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Seattle").count("Seattle") > 0


def test_home_page_has_seattle_in_results_when_only_argument(testapp, fill_the_db):
    """The home page search on seattle only gives a seattle results page."""
    response = testapp.post("/", params={
        "searchbar": "",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Seattle").count("Seattle") > 0


def test_results_page_has_python_in_results_when_only_argument(testapp, fill_the_db):
    """The results page search with python only gives a python results page."""
    response = testapp.post("/results", params={
        "searchbar": "",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Python").count("Python") > 0


def test_home_page_has_python_in_results_when_only_argument(testapp, fill_the_db):
    """The home page search with python only gives a python result page."""
    response = testapp.post("/", params={
        "searchbar": "",
        "location": "Seattle"
    }, status=302)
    full_response = response.follow()
    assert full_response.html.get_text("Python").count("Python") > 0


def test_results_page_has_sad_octo_when_nothing_found(testapp, fill_the_db):
    """The results page has sad octo, when nothing found on query."""
    response = testapp.post("/results", params={
        "searchbar": "Fortran",
        "location": "Chicago"
    }, status=302)
    full_response = response.follow()
    sad_octo = full_response.html.find(id="sad_octo")
    assert sad_octo


def test_home_page_has_sad_octo_when_nothing_found(testapp, fill_the_db):
    """The home page has sad octo, when nothing found on query."""
    response = testapp.post("/", params={
        "searchbar": "Fortran",
        "location": "Chicago"
    }, status=302)
    full_response = response.follow()
    sad_octo = full_response.html.find(id="sad_octo")
    assert sad_octo


def test_results_page_has_mad_octo_when_nothing_entered_on_search(testapp, fill_the_db):
    """The results page has mad octo, when nothing entered on query."""
    response = testapp.post("/results", params={
        "searchbar": "",
        "location": ""
    }, status=200)
    mad_octo = response.html.find(id="mad_octo")
    assert mad_octo


def test_home_page_has_sad_octo_when_nothing_entered_on_search(testapp, fill_the_db):
    """The home page has mad octo, when nothing entered on query."""
    response = testapp.post("/", params={
        "searchbar": "",
        "location": ""
    }, status=200)
    html = response.html
    mad_octo = html.find(id="mad_octo")
    assert mad_octo


# ============= SPIDER TESTS =====================


@pytest.fixture(scope="session")
def spider():
    """Create a JobSpider fixture to run through your code."""
    from octopus.spiders.spider import JobSpider
    spider = JobSpider()
    return spider


@pytest.fixture(scope="session")
def empty_test_dict():
    """Create an empty dictionary for tests."""
    return {}


@pytest.fixture(scope="session")
def full_test_dict():
    """Create a full dictionary for tests."""
    return {"http:://www.example.com": {
            'city': "Seattle, WA",
            'company': "Google",
            'description': "This is a job.",
            'title': "Job",
            'url': "http:://www.example.com"}}


@pytest.fixture(scope="session")
def none_test_dict():
    """Create a dictionary with none values for testing."""
    return {None: {
            'city': None,
            'company': None,
            'description': None,
            'title': None,
            'url': None}}


def test_create_empty_dict(testapp, spider, empty_test_dict, none_test_dict):
    """Test that create dict method returns null values in dict when empty."""
    assert spider.create_dict(empty_test_dict) == none_test_dict


def test_create_octopusitem_instance_empty_values(testapp,
                                                  spider,
                                                  empty_test_dict,
                                                  none_test_dict):
    """Input a dict with missing values.

    Test that you still create an OctopusItem.
    """
    items = {}
    key = None
    assert spider.build_items(items, empty_test_dict, key) == none_test_dict


def test_create_octopusitem_instance(testapp, spider, full_test_dict):
    """Test that when you input a dict, it returns an OctopusItem."""
    items = {}
    spider.build_items(items, full_test_dict, "http:://www.example.com")
    assert items["http:://www.example.com"]['city'] == 'Seattle, WA'


def test_create_full_dict(testapp, spider, empty_test_dict):
    """Test that create dict method returns expected values when dict full."""
    url = "http:://www.example.com"
    title = "Job"
    company = "Google"
    city = "Seattle, WA"
    description = "This is a job."
    new_dict = spider.create_dict(
        empty_test_dict,
        url=url,
        title=title,
        company=company,
        city=city,
        description=description)
    assert new_dict[url]["title"] == "Job"
