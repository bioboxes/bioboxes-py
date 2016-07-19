# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## v0.3.0 - 2016-07-19

### Added

  * Implemented deterministic filesytem mapping for Docker volumes. The
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
