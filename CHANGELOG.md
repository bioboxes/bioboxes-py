# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## v0.3.2 - 2016-07-20

### Fixed

  * A bug in tox configuration file meant the library was not being tested with
    python3 and therefore was not actually python3 compatible. This tox
    configuration was fixed and the library is now python3 compatible.

## v0.3.1 - 2016-07-19

### Fixed

  * The 'mem_limit' cgroup option is now correctly passed as part of the
    'host_config' when creating a new container.

## v0.3.0 - 2016-07-19

### Added

  * Implemented deterministic filesystem mapping for Docker volumes. The
    locations for the input data directories will always map to the same
    location in the Docker container. This is based on a creating a digest of
    the host directory path and using this as the directory name in the Docker
    container. This simplifies the processes of creating the Docker volume
    strings.

  * Added unit tests for each biobox type. This ensures that the biobox.py
    library should always be compatible for each biobox type.

## v0.2.1 - 2016-05-29

### Fixed

  * The library is now python 3 compatible.

## v0.2.0 - 2016-05-13

### Added

  * Added functions for checking whether the is running and what is the exit
    code. Added an additional function for collecting cgroup metrics from a
    running container.

## v0.1.0 - 2016-05-06

### Added

  * Initial release of project with code for creating biobox Docker containers
    with appropriately mounted volumes for inputs, outputs and the biobox.yaml
    file.
