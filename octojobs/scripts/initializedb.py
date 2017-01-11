import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )
from ..models import Job


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        model = Job(
            city='Seattle',
            title='Windows UWP/Phone Developer, Seattle WA',
            company='Interloc Solutions',
            description="""Our Products & Technology group in Seattle has an immediate need for an experienced Windows developer (Windows 10/Windows Surface) to support our Informer mobile solution products. This position will contribute heavily to product builds, so prior mobile application development experience is essential. Experience with Windows 10/Windows Surface 3+ years demonstrated experience in .NET and C# development Strong knowledge of the .NET framework, C#, with component extensions Prior mobile application development SQLite (highly desired, but not required) Full SDLC experience, including release to operations and production This is a great opportunity to work with our progressive mobile team!""",
            url="www.interlocsolutions.com",
            language='C#'
            )
        dbsession.add(model)
