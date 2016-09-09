# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## v0.4.3 - 2016-09-09

### Fixed

  * Enable networking on all biobox docker images by default to solve problem
    of occaisonal network outages on stats collection as outlined in
    [docker/docker-py#1195][issue-1195].

[issue-1195]: https://github.com/docker/docker-py/issues/1195

## v0.4.2 - 2016-09-08

### Fixed

  * Fixed bug where cgroup data was sampled at 1 second intervals instead of
    the interval specified by the function argument.

## v0.4.0 - 2016-08-15

### Changed

  * The function `create_container` now requires a dictionary of volumes to
    mount when creating a container. This dictionary requires the output
    directory, and optionally the metadata directory. The metadata directory is
    used to store logs by biobox images if mounted.

  * The function `prepare_volumes` accepts an optional metadata_directory host
    path argument. This is mounted into the container at `/bbx/metadata` if
    provided.

## v0.3.3 - 2016-07-27

### Changed

  * Switched to use the ruamel.yaml python library instead of PyYAML as this
    appears to cause less problems with using python 3.

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
