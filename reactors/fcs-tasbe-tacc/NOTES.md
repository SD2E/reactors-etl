# Building FCS-TASBE for TACC's Agave runtime

## Build and share a container image

Bundle your code and whatever assets are required to run it in a Docker container. 

1. Try to avoid working in / (unless that's your intent)
2. Do ADD and COPY operations as late as possible as they invalidate the Docker cache on downstream layers
3. Import archive files from GitHub using tagged releases
4. Clean up your build directories when done
5. Put scripts and other assets in relatively standard places
6. Make the default ENTRYPOINT or CMD script competent to return usage/help information
7. Avoid changing USER inside the container
8. Try to set `/home` as `WORKDIR`

### Starting from scratch

If you don't have an existing container, please consider starting from:

1. `index.docker.io/sd2e/base:ubuntu16`
2. `index.docker.io/sd2e/python2:ubuntu16`

These are certain to be updated and improved, and more baseline images may be released as needed in the future. 

### Starting with an existing container

Follow the guidelines above on packaging strategy. As your application reaches maturity, you'll want to think about optimizing build order etc. to minimize container image size, but don't worry too much about it now. 

## Develop a working instantiation of your application

* Create a working directory `foo` under where you've been working  on your container build.
* Add that directory to `.dockerignore`
* Copy in our application template: `cp -R ../hello-container/template/* foo/` 
* Edit the CONTAINER_IMAGE value in `tester.sh`
* Edit the `container_exec` line to invoke your container image

```
DEBUG=1 container_exec ${CONTAINER_IMAGE} <command (relative to container /> <options-and-arguments-no-spaces>
```

Any value for DEBUG besides "empty" will cause container_exec to output `.container_exec.<pid>.log` and `.container_exec.<pid>.env` files as well as set verbose output in the shell when the docker command is set up. 


* Edit and run tester.sh until you get the expected behavior (You may get lucky right off the bat).

Presumably your code needs to work on one or more input files and accepts one or more parameters:

* Download a small sample file `bar.txt` (or files) into `foo`.
* Edit tester.sh so it calls your code and tells it to work on `bar.txt`. Here's an example

```shell
DEBUG=1 container_exec stegosarus:0.0.2 thagomize --target thag.txt --punctures 4
```

Now, make `tester.sh` parameterizable:

```shell

input1="thag.txt"
punct=4

DEBUG=1 container_exec stegosarus:0.0.2 thagomize --target ${input1} --punctures ${punct}
```

You're ready to turn your work on `tester.sh` into a `runner-template.sh`. Hold on... it may be complicated.


```shell
CONTAINER_IMAGE="index.docker.io/stegosarus:0.0.2"
source _util/container_exec.sh

container_exec stegosarus:0.0.2 thagomize --target ${input1} --punctures ${punct}
```

Basically, we took away the lines that set the values for `input1` and `punct` and added the hub location for the image (not mandatory, but prevents any ambiguity). All that's left now is to tell the Agave environment how to run this application. 



