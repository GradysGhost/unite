# Unite!

Unite! is a modular REST API that aggregates data from multiple sources. At this point in
development, the goal is to provide a single point of entry for managing data from a variety of data
sources while remaining agnostic about how that data is accessed. For example, Unite's single API
might allow unified access to the contents of a Dropbox collection, an OwnCloud server, and content
from behind an Apache/mod_dav configuration with HTTP Basic Auth.

At the core, Unite provides a framework for adding functionality in the form of plugins. Plugins can
add data source types, API routes, and additional data to manage, perhaps media tagging and
plalisting, or a way of editing image EXIF data.

## Install

    sudo pip install unite

## Configure

Unite likes to find a `config.yml` file in its root that tells it how to run. This section describes
how to configure it in the general sense. Each plugin may demand the presence of other options, and
you should refer to each plugin's documentation for details. Some sane values are shown below.

    logging:
      level: WARN
      format: [%(asctime)s] [%(levelname)s] %(message)s 

`logging.level` should be one of the Python logger levels described here:
https://docs.python.org/2/library/logging.html#logging-levels

`logging.format` should be a log format string as described in these documents:

  * https://docs.python.org/2/library/logging.html#formatter-objects
  * https://docs.python.org/2/library/logging.html#logrecord-attributes
  * https://docs.python.org/2/library/stdtypes.html#string-formatting

Set how Unite listens with these options:

    bind_address: 127.0.0.1
    bind_port: 12321

Include some plugins by listing their names:

    plugins:
      - status

## Plugins

### status

The `status` plugin adds a route to handle GET calls to /status. It returns a JSON object with a
'status' field set to 'online' if the service is meant to be online or 'maintenance' if you set the
'maintenance' config value to 'yes'. Note that setting this to 'yes' doesn't actually prevent
requests from being processed. This plugin is intended as a health check endpoint, allowing you to
"soft remove" a server from a load balancer by invalidating its health check in this manner.

#### Config

    plugins:
      - status

    maintenance: yes|no


## Writing Plugins

Your plugin can do just about anything. You can add routes in standard Flask fashion by decorating
functions with `@app.route()`. You can write plugins that provide common library functionality
without having them handle any requests at all, just exposing some functions to other plugins. You
can also listen in on a few events simply by including a few specially-named functions in your
plugin module. They are:

  * `__event_request_received__(request)`: When Unite receives a request, this function is called
    in each plugin that has one.
  * `__event_request_processed__(request)`: After calling each of the "`received`" event handlers,
    the request is handled by the function set up in Flask to handle it. After that, but before
    sending the response back to the client, this function is called in each plugin that has one.
  * `__event_quit__(signum, stack)`: This function is called in each plugin that has one when Unite
    is told to quit, having received one of these system signals:
      * SIGHUP
      * SIGINT
      * SIGTERM

The entirety of the configuration file's contents is loaded into a dictionary stored within the
Flask app. Just import the app...

    from unite import app

...and get at the config:

    print(app.config)


