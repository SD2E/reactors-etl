# ETL Components for the SD2 Program Data

This repository holds the source code and test material for developing ETL components to power data and metdata extraction, transformation, and loading for the DARPA SD2 program. These ETL components will be based on [TACC's Reactors service](docs/404.md), which brings the highly useful _functions-as-a-service_ concept popularized by the commercial cloud to the world of high-performance computing. 

If you want to jump right into a tutorial on creating a new Reactor go here: [Getting Started with Reactors](docs/404.md)

## reactors

This is where production SD2E Reactors will live. Our conventions are:
* Maintain URL-safe directory naming conventions
* The penultimate Dockerfile for a Reactor should be named `Dockerfile`
* We prefer to base off base images provided by the SD2E team
  * sd2e/reactor_alpine_36
  * sd2e/reactor_ubuntu_xenial
  * sd2e/reactor_centos_7
  * _more options are coming_
* Other files in various reactors directories (such as `package.yml`) are *very mutable* up till the first SD2E release in October (or TACC announces otherwise).

## templates

Templates for various assets needed to use and deploy to the TACC Reactors service can be found here. 

### reactors

Template directories for various forms of Reactor are here. We'll start with language-specific examples initially. 

### docker-images

Template directories for 

## build

Build scripts used by SD2E platform developers to build and deploy system-wide assets. 

## docs

Self-explanatory. Home of the guides, tutorials, etc. for contirbuting ETL-specific Reactors to SD2E platform.

