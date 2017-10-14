# FCS-TASBE-TACC

Containerized, extensible FCS-TASBE parser packaged to promote seamless transition between local development and testing and deployment into production on TA4-provided services.

## Requirements

**Software and Accounts**

You need the following installed locally to develop/test this ETL code for Flow data. Ideally, you'll be developing in a UNIX-like environment as we make heavy use of Bash and UNIX file path conventions. 

* Docker 17.X.X-ce
* Python 2.7.10+
* Bash 3.2.57+
* Git 2.12+
* jq 1.5+
* A GitHub account
* A Docker Hub account
* An active SD2E account

**API Client**

You must have installed and configured the SD2-CLI, completing [all steps in the SD2E API user guide][1] up to **Authorize with the SD2E Tenant**

## Running an example analysis (local)

**Get some local data**

We include a simple local caching mechanism for holding data, which can pull files from SD2E resources or which you can populate yourself. Either copy test data yourself into `fcs-tasbe-tacc/test-data-cache` or populate test-data.tsv with file references and run suport/import-test-data.sh. 

**Edit the tester**

Edit `fcs-tasbe-0.2.0/tester.sh` to use data you've staged to the local cache directory. The key elements are here:

```
# inputData is a Flow experiment. It can either be a directpry or a zipped directory

export inputData="Q0-ProtStab-BioFab-Flow_29092017.zip"

# Normally, the fc.json is going to be inside <inputData> but if you're working on a revised one
# or need to override the included one, set its name here. Otherwise set to empty

export fcOverride="updated-fc.json"
# export fcOverride=

```

**Run the example**
Change into the `fcs-tasbe-0.2.0` directory. You should be able to just run `bash tester.sh`. The Docker image will be pulled if it doesn't exist locally, and the fc.py code will be run against data that is copied into this directory from `../test-data-cache`. You should see a plots and CSV output if all has gone according to plan. You can reset the directory to its original state by running `CLEAN=1 bash tester.sh`

## Running an example analysis @ SD2E using the SD2E CLI

```shell
% cd fcs-tasbe-tacc
# refresh your API token (run auth-tokens-create -S if you get an error)
% auth-tokens-refresh -S
# submit a job request to the public (production) fcs-tasbe application
% jobs-submit -F ../fcs-tasbe-0.2.0/tasbe-public-job.json -W
# You can watch your job run live. See the API docs for more.
```

## Running an example analysis @ SD2E in Jupyter

_Coming soon_

## Making changes

To change just the data that is processed:
1. Run `CLEAN=1 bash tester.sh` inside `fcs-tasbe-0.2.0`
2. If you need to import more data, edit `test-data.tsv`, then edit `fcs-tasbe-0.2.0/tester.sh` as above
3. That's it (or it should be)

To update code that lives inside `src/`
1. Make your changes
2. Run `bash ./build.sh`
3. If you have not changed the container name or version, you can now run the new container
```shell 
cd fcs-tasbe-0.2.0
bash tester.sh
```

To deploy to production
1. We will update this section soon

## References

[1]: http://sd2e.org/api-user-guide/
