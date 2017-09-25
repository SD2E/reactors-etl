# Publish container to cloud

## Define metadata and execution instructions

1. Create a template runner script and app.yml template using our scaffold
2. Define some inputs, parameters, and output names you want to use to parameterize it in app.yml
3. Begin defining the runtime, starting with the details of the container image (we'll add more about the host environment later)
4. 


## Test

The sd2e-cli ships with experimental support for testing your application locally. You can override almost any field in the app.yml with app.field dot notation parameters. This is accomplished by building a dynamic option handler based on the contents of app.yml (and its template). 

sd2e apps test --local --definition app.yml --app.runtime.template agave-runner.sh


## Behind the scenes

- Lint the YML files
- Lint the resulting JSON
- Validate the JSON using Rich's JSON schema
