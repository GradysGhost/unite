# Unite!

Unite! is a modular REST API that aggregates data from multiple sources. At this point in
development, the goal is to provide a single point of entry for managing data from a variety of data
sources while remaining agnostic about how that data is accessed. For example, Unite's single API
might allow unified access to the contents of a Dropbox collection, an OwnCloud server, and content
from behind an Apache/mod_dav configuration with HTTP Basic Auth.

At the core, Unite provides a framework for adding functionality in the form of plugins. Plugins can
add data source types, API routes, and additional data to manage, perhaps media tagging and
plalisting, or a way of editing image EXIF data.

