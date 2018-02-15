## SD2 App ETL Submission and Deployment

## LCMS .msf Example
Assumes you have a working, authenticated sd2e client. Abbreviated steps for this below.

TACC's documentation is also quite good if you want to try that out as well: [https://sd2e.github.io/api-user-guide/](https://sd2e.github.io/api-user-guide/)

	# Should only need to do all of this this once...
	curl -L https://raw.githubusercontent.com/sd2e/sd2e-cli/master/install/	install.sh | sh
	source ~/.bashrc
	tenants-init -t sd2e
	clients-create -S -N sd2e_client -D "My client used for interacting with SD2E"
	# Your secret and access key should now be here
	cat ~/.agave/current
	# Create and check authentication. If your secret and access keys are
	# working, you can re-start at this point to re-authenticate later
	# (it's cached)
	auth-tokens-create -S
	auth-check

Let's list some apps, passing -P to get all publically accessible apps:

	apps-list -P
	>
	lcms-0.1.0u4
	lcms-0.1.0u3
	hello-agave-hpc-0.1.0u1
	hello-agave-cli-0.1.0u1
	sailfish-0.10.1u2
	fcs-tasbe-0.1.0u2
	msf-0.1.0u3
	kallisto-0.43.1u3
	hello-container-0.1.0u1

Digging in. In general "command -h" will provide command help.

	apps-list -v msf-0.1.0u3

Lots of JSON. We'll want to focus on inputs and parameters.

	{
	  "id": "msf-0.1.0u3",
	  "name": "msf",
	  "icon": null,
	  "uuid": "1033233682410892825-242ac115-0001-005",
	  "parallelism": "SERIAL",
	  "defaultProcessorsPerNode": 1,
	  "defaultMemoryPerNode": 1,
	  "defaultNodeCount": 1,
	  "defaultMaxRunTime": "00:30:00",
	  "defaultQueue": null,
	  "version": "0.1.0",
	  "revision": 3,
	  "isPublic": true,
	  "helpURI": "https://sd2e.org/develop/",
	  "label": "MSF Parser",
	  "owner": "sd2eadm",
	  "shortDescription": "",
	  "longDescription": "",
	  "tags": [
	    "msf",
	    "docker://index.docker.io/sd2e/msf:latest"
	  ],
	  "ontology": [
	    "http://edamontology.org/topic_3520"
	  ],
	  "executionType": "HPC",
	  "executionSystem": "hpc-tacc-maverick",
	  "deploymentPath": "/.public-apps/msf-0.1.0u3.zip",
	  "deploymentSystem": "data-sd2e-projects-users",
	  "templatePath": "runner-template.sh",
	  "testPath": "tester.sh",
	  "checkpointable": false,
	  "lastModified": "2017-10-10T14:12:23.000-05:00",
	  "modules": [
	    "load tacc-singularity/2.3.1"
	  ],
	  "available": true,
	  "inputs": [
	    {
	      "id": "msfDataFile",
	      "value": {
	        "validator": null,
	        "visible": true,
	        "required": true,
	        "order": 0,
	        "enquote": false,
	        "default": "agave://data-sd2e-community/sample/msf/exp2801-04-ds731218.msf"
	      },
	      "details": {
	        "label": "MSF (Magellan storage file) file",
	        "description": null,
	        "argument": null,
	        "showArgument": false,
	        "repeatArgument": false
	      },
	      "semantics": {
	        "minCardinality": 1,
	        "maxCardinality": 1,
	        "ontology": [
	          "http://edamontology.org/format_3702"
	        ],
	        "fileTypes": []
	      }
	    }
	  ],
	  "parameters": [
	    {
	      "id": "outputFileName",
	      "value": {
	        "visible": true,
	        "required": false,
	        "type": "string",
	        "order": 0,
	        "enquote": false,
	        "default": "msf-output.csv",
	        "validator": ""
	      },
	      "details": {
	        "label": "Output file name",
	        "description": null,
	        "argument": null,
	        "showArgument": false,
	        "repeatArgument": false
	      },
	      "semantics": {
	        "minCardinality": 0,
	        "maxCardinality": 1,
	        "ontology": [
	          "http://edamontology.org/data_2536",
	          "http://edamontology.org/format_3752"
	        ]
	      }
	    }
	  ],
	  "outputs": [
	    {
	      "id": "analysisOutput",
	      "value": {
	        "validator": null,
	        "order": 0,
	        "default": "msf-output.csv"
	      },
	      "details": {
	        "label": "Comma-separated value from LCMS code",
	        "description": null
	      },
	      "semantics": {
	        "minCardinality": 1,
	        "maxCardinality": 1,
	        "ontology": [
	          "http://edamontology.org/format_3475",
	          "http://edamontology.org/data_2536"
	        ],
	        "fileTypes": []
	      }
	    }
	  ],
	  "_links": {
	    "self": {
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u3"
	    },
	    "executionSystem": {
	      "href": "https://api.sd2e.org/systems/v2/hpc-tacc-maverick"
	    },
	    "storageSystem": {
	      "href": "https://api.sd2e.org/systems/v2/data-sd2e-projects-users"
	    },
	    "history": {
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u3/history"
	    },
	    "metadata": {
	      "href": "https://api.sd2e.org/meta/v2/data/?q=%7B%22associationIds%22%3A%221033233682410892825-242ac115-0001-005%22%7D"
	    },
	    "owner": {
	      "href": "https://api.sd2e.org/profiles/v2/sd2eadm"
	    },
	    "permissions": {
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u3/pems"
	    }
	  }
	}

This creates a template input for running this app. Neat.

	jobs-template msf-0.1.0u3 > msf.json

	{
	  "name": "msf test-1507578206",
	  "appId": "msf-0.1.0u3",
	  "archive": true,
	  "inputs": {
	    "msfDataFile": "agave://data-sd2e-community/sample/msf/exp2801-04-ds731218.msf"
	  },
	  "parameter": {
	  }
	}

That input can figure out agave paths that look like agave://**system**/**path**

What systems do we have?

	systems-list
	>
	data-sd2e-projects-q0-sharing
	hpc-tacc-jetstream
	data-sd2e-app-assets
	data-tacc-work-mweston
	hpc-tacc-maverick-mweston
	data-sd2e-community
	hpc-tacc-maverick
	cli-tacc-maverick
	data-sd2e-projects-q0-ingest
	data-sd2e-projects-q0-examples
	cli-tacc-wrangler

**data-sd2e-projects-q0-ingest** looks promising. So, for our S3 bucket:

	s3://sd2e-q0-ta3-ingest/uploads/sd2.ginkgo.upload/yeastgates/proteomics/

We can substitute:

	agave://data-sd2e-community/sample/msf/exp2801-04-ds731218.msf

	with

	agave://data-sd2e-projects-q0-ingest/uploads/sd2.ginkgo.upload/yeastgates/proteomics/exp3818/exp3818-4-ds1190884.msf

The name in the JSON is going to be ***really*** important. We need to use this to bind a TACC *job identifier* (with its inputs and outputs) to the JSON job submission.

Edit msf.json, modifying the name to something ***unique*** and with the desired input AND output.

	{
	  "name": "msf-test-exp3818-4-ds1190884",
	  "appId": "msf-0.1.0u3",
	  "archive": false,
	  "inputs": {
	    "msfDataFile": "agave://data-sd2e-projects-q0-ingest/uploads/sd2.ginkgo.upload/yeastgates/proteomics/exp3818/exp3818-4-ds1190884.msf"
     },
     "parameters": {
       "outputFileName": "exp3818-4-ds1190884.csv"
     }
	}

**archive** controls whether the job's output persists. For now, leave this off. In the future, we may want to leave this on to persist job runs.

By convention, I am setting the name, input, and output to align. Convention here may vary (consult the -v args)

Submit job:

	jobs-submit -F msf.json
	>
	Successfully submitted job 7321434283412558311-242ac11b-0001-007

Now, in case we didn't see the above, or want to query for our job based on the name in the JSON:

	jobs-search name=msf-test-exp3818-4-ds1190884
	>
	7321434283412558311-242ac11b-0001-007 SUBMITTING

This also prints job status. Repeat this until we're done...

	7321434283412558311-242ac11b-0001-007 RUNNING
	7321434283412558311-242ac11b-0001-007 FINISHED

Query for outputs from the job:

	jobs-output-list 7321434283412558311-242ac11b-0001-007
	>
	.agave.archive
	.agave.log
	_util
	agave-runner.sh
	app.json
	exp3818-4-ds1190884.csv
	exp3818-4-ds1190884.msf
	job-public.json
	job.json
	localtest
	msf-test-exp3818-4-ds1190884-7321434283412558311-242ac11b-0001-007.err
	msf-test-exp3818-4-ds1190884-7321434283412558311-242ac11b-0001-007.out
	msf-test-exp3818-4-ds1190884.ipcexe
	runner-template.sh
	tester.sh

Looks like we got a CSV! Let's grab it.

	jobs-output-get 7321434283412558311-242ac11b-0001-007 exp3818-4-ds1190884.csv

Sample rows from exp3818-4-ds1190884.csv:

| coverage    | description                                                                                                                                                                                                                                                                                                                                                                            | protein_id | protein_score | sequence                  |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|---------------|---------------------------|
| 3.03030303  | >YBR020W_W303 GAL1 gi 696449286 gb JRIU01000067.1 20629-22215 ORF Verified Galactokinase; phosphorylates alpha-D-galactose to alpha-D-galactose-1-phosphate in the first step of galactose catabolism; expression regulated by Gal4p; GAL1 has a paralog, GAL3, that arose from the whole genome duplication                                                                          | 14         | 0             | MTKSHSEEVIVPEFNSSAKELPRPL... |
| 3.846153846 | >YDR009W_W303 GAL3 gi 696449403 gb JRIU01000037.1 234276-235838 ORF Verified Transcriptional regulator; involved in activation of the GAL genes in response to galactose; forms a complex with Gal80p to relieve Gal80p inhibition of Gal4p; binds galactose and ATP but does not have galactokinase activity; GAL3 has a paralog, GAL1, that arose from the whole genome duplication | 15         | 0             | MNTNVPIFSSPVRDLPRSFEQKHH...  |

## LCMS .mzML Example

	{
	  "name": "lcms-test-exp3781-21-ds1179583",
	  "appId": "lcms-0.1.0u4",
	  "archive": false,
	  "inputs": {
	    "lcmsDataFile": "agave://data-sd2e-projects-q0-ingest/uploads/sd2.ginkgo.upload/yeastgates/proteomics/exp3781/exp3781-21-ds1179583-t0-Pos.mzML"
	  },
	  "parameters": {
	    "outputFileName":"exp3781-21-ds1179583.csv"
	  }
	}

Sample rows from exp3781-21-ds1179583.csv:

| highest observed m/z | ms level | total ion current | lowest observed m/z | filename                        | controllerType | controllerNumber | scan | base peak intensity | base peak m/z |
|----------------------|----------|-------------------|---------------------|---------------------------------|----------------|------------------|------|---------------------|---------------|
| 2020.198353          | 1        | 14836067          | 346.5168475         | exp3781-21-ds1179583-t0-Pos.raw | 0              | 1                | 1    | 5210976             | 371.1021293   |
| 2020.194876          | 1        | 14772954          | 346.5162506         | exp3781-21-ds1179583-t0-Pos.raw | 0              | 1                | 2    | 5289835             | 371.1014135   |
| 2020.195116          | 1        | 15221287          | 346.5163528         | exp3781-21-ds1179583-t0-Pos.raw | 0              | 1                | 3    | 5467094             | 371.1014796   |

## LCMS .fasta Example

	jobs-template lcms-0.1.0u4 > lcms.json

	{
	  "name": "lcms-test-ec-K12",
	  "appId": "lcms-0.1.0u4",
	  "archive": false,
	  "inputs": {
	    "lcmsDataFile": "agave://data-sd2e-community/sample/lcms/ec_K12.fasta"
	  },
	  "parameters": {
	    "outputFileName":"ec_K12.csv"
	  }
	}

Sample rows from ec_K12.csv:

| GeneInfo ID | Accession   | Description                                                        | Sequence                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|-------------|-------------|--------------------------------------------------------------------|---------------|
| gi:16127996 | NP_414543.1 | aspartokinase I, homoserine dehydrogenase I [Escherichia coli K12] | MRVLKFGGTSVANAER... |
| gi:16127997 | NP_414544.1 | homoserine kinase [Escherichia coli K12]                           | MVKVYAPASSANMSVG....                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| gi:16127998 | NP_414545.1 | threonine synthase [Escherichia coli K12]                          | MKLYNLKDHNEQVSFA...                                                                                                                                                                                                                                                                                                                                                                                                        |

## App Deployment

The lcms and msf apps currently support the ability to deploy private versions of these apps. Upon successful testing, a TACC admin can promote the private app to a public one, making it available for all users.

To begin, select an app to modify and deploy:

[lcms](https://github.com/SD2E/reactors-etl/tree/master/reactors/lcms)

[msf](https://github.com/SD2E/reactors-etl/tree/master/reactors/msf)

As an example, we will be updating and deploying the "lcms" app.

[1] Edit the VERSION file located in the lcms-0.1.0 directory.

This file contains the tag of the docker image that will be built, pushed, tested, and executed for the lcms app. Change the current content of that VERSION file, latest, to a named tag you want to test with. This change affects the relevant scripts:

	build.sh
	push.sh
	<lcms-0.1.0>tester.sh
	<lcms-0.1.0>runner-template.sh
	
which will substitute latest with whatever is in your VERSION file. Pick a name that is unique and meaningful, e.g. username-feature, where you're substituting username with your TACC account username. We'll be using **"mweston-fix-import"** for this example for our VERSION information.

[2] We need to modify the name in the app.json file in the app-0.1.0 directory from its current value:

	"name": "lcms",

This is the **name** of the app that will show up in apps-list. Note this can be different from the docker tag that is built! The docker tag is already on the lcms image, so we include "lcms" here to help fully identify this app.
	
	"name": "lcms-mweston-fix-import",
 
[3]
 
	"executionSystem": "hpc-tacc-maverick",

Needs to be changed to your private maverick system:

	"executionSystem": "hpc-tacc-maverick-mweston",

[4]

	"deploymentPath": "sd2eadm/apps/lcms-0.1.0",
	
Needs to change to look exactly like the following. We're going to be loading the app from our personal workspace, not the sd2eadm user.

	"deploymentPath": "mweston/apps/lcms-0.1.0",

[5]

	"tags": ["lcms", "docker://index.docker.io/sd2e/lcms:latest"],
	
Change this to the tag you edited into the VERSION file. This tells the app to use your custom docker image.

	"tags": ["lcms", "docker://index.docker.io/sd2e/lcms:mweston-fix-import"],

Next, we can deploy our app!

	./deploy.sh lcms-0.1.0 

If all goes well, check to see if the app shows in your list of private apps. Note that deployment requires docker.io push permissions to the SD2E organization.

	apps-list -Q

To test your app, run:

	jobs-submit -F yourapp.json
	
Where yourapp.json references your new, private app, e.g.

	{
	  "name": "lcms-mweston-test-1",
	  "appId": "lcms-mweston-fix-import", <--- here
	  "archive": false,
	  "inputs": {
	    "lcmsDataFile": "agave://data-sd2e-community/sample/lcms/ec_K12.fasta"
	  },
	  "parameters": {
	    "outputFileName":"ec_K12.csv"
	  }
	}
	
If the app runs and produces the desired output, contact TACC staff and ask them to promote your app. Currently, users cannot globally publish private apps. 

However, the process is very quick from the TACC side. They can also disable previous versions of an app, or leave those up, allowing users to choose which version they want to run against. 