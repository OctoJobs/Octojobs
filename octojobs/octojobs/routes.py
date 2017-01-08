def includeme(config):
    config.add_static_view(name='static', path='octojobs:static', cache_max_age=3600)
    config.add_route('home', '/')
