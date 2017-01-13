"""The test module for the Octojobs project."""

import faker
from octojobs.models import Job
from octojobs.models import get_tm_session
from octojobs.models.meta import Base
from pyramid import testing
from pyramid.httpexceptions import HTTPFound
import pytest
import transaction
# import unittest.mock
# import requests

fake = faker.Faker()

DUMMY_JOBS = [Job(
    title=fake.job(),
    city=fake.city(),
    description=fake.text(100),
    company=fake.company(),
    url=fake.url()
) for i in range(10)]


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
    """Assert is instance of HTTP found, from POST request."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = home_view(dummy_request)

    assert isinstance(result, HTTPFound)


def test_post_home_view_reroutes_with_query(dummy_request):
    """Assert search terms are passed on url."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = home_view(dummy_request)

    assert 'test' and 'seattle' in result.location


def test_post_home_view_with_only_location_query(dummy_request):
    """Test only one query with only location filled."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = "seattle"
    dummy_request.POST["searchbar"] = ""

    result = home_view(dummy_request)

    assert result.location == 'http://example.com/results?location=seattle'


def test_post_home_view_with_only_searchterm_query(dummy_request):
    """Test only one query with only searchterm filled."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = "developer"

    result = home_view(dummy_request)

    assert result.location == 'http://example.com/results?search=developer'


def test_post_home_view_with_no_query(dummy_request):
    """Test only no queries on the home form are passed on url."""
    from octojobs.views.default import home_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = ""

    assert home_view(dummy_request) == {'no_query': 'no result'}


def test_post_result_view_reroutes_with_new_query(dummy_request):
    """Assert search terms are passed on url on result view."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    result = result_view(dummy_request)

    assert 'test' and 'seattle' in result.location


def test_post_results_view_with_location_query(dummy_request):
    """Test only one query with only location filled."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = "seattle"
    dummy_request.POST["searchbar"] = ""

    result = result_view(dummy_request)

    assert result.location == 'http://example.com/results?location=seattle'


def test_post_result_view_with_search_query_only(dummy_request):
    """Test only one query with only search filled."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = "test"

    result = result_view(dummy_request)

    assert result.location == 'http://example.com/results?search=test'


def test_post_result_view_with_no_query(dummy_request):
    """Test only no queries on the home form are passed on url."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["location"] = ""
    dummy_request.POST["searchbar"] = ""
    import pdb; pdb.set_trace()

    assert result_view(dummy_request) == {'no_query': 'no result'}


def test_get_result_view_with_no_query(dummy_request):
    """Test get request on result view."""
    from octojobs.views.default import result_view

    dummy_request.method = "POST"
    dummy_request.POST["searchbar"] = "test"
    dummy_request.POST["location"] = "seattle"

    get_info = dummy_request.GET.get('location')

    result_view(dummy_request)

    assert dummy_request.GET["location"] == "seattle"
    assert get_info == ""


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


# def test_search_returns_results(testapp, fill_the_db):
#     """When there's data in the database, the home page has rows."""
#     response = testapp.get('results', method="POST", location="Seattle")
#     html = response.html
#     assert html.find_all("Windows") is True


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