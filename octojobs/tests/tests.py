"""The test module for the Octojobs project."""

import transaction
import pytest
from octojobs.models import Job
from octojobs.models import get_tm_session
from octojobs.models.meta import Base
import faker
from pyramid import testing


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


# ============= FUNTIONAL TESTS =====================

@pytest.fixture
def testapp(request):
    """The fixture creates a test app."""
    from webtest import TestApp
    from pyramid.config import Configurator

    def main(global_config, **settings):
        """The function returns a Pyramid WSGI application."""
        config = Configurator(settings=settings)
        config.include('pyramid_jinja2')
        config.include('.models')
        config.include('.routes')
        config.scan()
        return config.make_wsgi_app()

    app = main({}, **{
        "sqlalchemy.url": 'postgres:///test_jobs'
    })
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
