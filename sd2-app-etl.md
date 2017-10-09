##SD2 App ETL Submission

Assumes you have a working, authenticated sd2e client. Abbreviated steps for this below.

TACC's documentation is also quite good if you want to try that out as well: [http://sd2e.org/api-user-guide/](http://sd2e.org/api-user-guide/)

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

Let's list some apps:

	apps-list
	>
	kallisto-0.43.1u2
	msf-0.1.0u2
	lcms-0.1.0u1
	fcs-tasbe-0.1.0u1
	sailfish-0.10.1u1

Digging in. In general "command -h" will provide command help.

	apps-list -v msf-0.1.0u2

Lots of JSON. We'll want to focus on inputs and parameters.

	{
	  "id": "msf-0.1.0u2",
	  "name": "msf",
	  "icon": null,
	  "uuid": "5176379387814744551-242ac115-0001-005",
	  "parallelism": "SERIAL",
	  "defaultProcessorsPerNode": 1,
	  "defaultMemoryPerNode": 1,
	  "defaultNodeCount": 1,
	  "defaultMaxRunTime": "00:30:00",
	  "defaultQueue": null,
	  "version": "0.1.0",
	  "revision": 2,
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
	  "deploymentPath": "${foundation.service.apps.default.public.dir}/msf-0.1.0u2.zip",
	  "deploymentSystem": "data-sd2e-projects-q0-sharing",
	  "templatePath": "runner-template.sh",
	  "testPath": "tester.sh",
	  "checkpointable": false,
	  "lastModified": "2017-10-04T18:18:08.000-05:00",
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
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u2"
	    },
	    "executionSystem": {
	      "href": "https://api.sd2e.org/systems/v2/hpc-tacc-maverick"
	    },
	    "storageSystem": {
	      "href": "https://api.sd2e.org/systems/v2/data-sd2e-projects-q0-sharing"
	    },
	    "history": {
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u2/history"
	    },
	    "metadata": {
	      "href": "https://api.sd2e.org/meta/v2/data/?q=%7B%22associationIds%22%3A%225176379387814744551-242ac115-0001-005%22%7D"
	    },
	    "owner": {
	      "href": "https://api.sd2e.org/profiles/v2/sd2eadm"
	    },
	    "permissions": {
	      "href": "https://api.sd2e.org/apps/v2/msf-0.1.0u2/pems"
	    }
	  }
	}

This creates a template input for running this app. Neat.

	jobs-template lcms-0.1.0u1 > lcms.json

	{
	  "name": "msf test-1507578206",
	  "appId": "msf-0.1.0u2",
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
	  "appId": "msf-0.1.0u2",
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

Success:

	coverage	description	protein_id	protein_score	sequence
	0	3.03030303	>YBR020W_W303 GAL1 gi|696449286|gb|JRIU01000067.1| 20629-22215 ORF Verified Galactokinase; phosphorylates alpha-D-galactose to alpha-D-galactose-1-phosphate in the first step of galactose catabolism; expression regulated by Gal4p; GAL1 has a paralog, GAL3, that arose from the whole genome duplication	14	0	MTKSHSEEVIVPEFNSSAKELPRPLAEKCPSIIKKFISAYDAKPDFVARSPGRVNLIGEHIDYCDFSVLPLAIDFDMLCAVKVLNEKNPSITLINADPKFAQRKFDLPLDGSYVTIDPSVSDWSNYFKCGLHVAHSFLKKLAPERFASAPLAGLQVFCEGDVPTGSGLSSSAAFICAVALAVVKANMGPGYHMSKQNLMRITVVAEHYVGVNNGGMDQAASVCGEEDHALYVEFKPQLKATPFKFPQLKNHEISFVIANTLVVSNKFETAPTNYNLRVVEVTTAANVLAATYGVVLLSGKEGSSTNKGNLRDFMNVYYARYHNISTPWNGDIESGIERLTKMLVLVEESLANKKQGFSVDDVAQSLNCSREEFTRDYLTTSPVRFQVLKLYQRAKHVYSESLRVLKAVKLMTTASFTADEDFFKQFGALMNESQASCDKLYECSCPEIDKICSIALSNGSYGSRLTGAGWGGCTVHLVPGGPNGNIEKVKEALANEFYKVKYPKITDAELENAIIVSKPALGSCLYEL

