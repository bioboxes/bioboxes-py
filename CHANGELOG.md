# Change Log

All notable changes to this project will be documented in this file. This
project adheres to [Semantic Versioning](http://semver.org/).

## v0.3.0 - 2016-08-15

### Changed

  * The function `create_container` now requires a dictionary of volumes to
    mount when creating a container. This dictionary requires the output
    directory, and optionally the metadata directory. The metadata directory is
    used to store logs by biobox images if mounted.

  * The function `prepare_volumes` accepts an optional metadata_directory host
    path argument. This is mounted into the container at `/bbx/metadata` if
    provided.

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
