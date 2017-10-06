# Provisioning test data

1. Edit `test-data.tsv` to suit your needs
2. Run `./import-test-data.sh`. A copy of the files and directories specified will be downloaded to `test-data-cache`
3. Run `stage-test-data.sh <app-directory> <override-localtest>`
4. Change into `<app-directory>`. Edit `tester.sh` if needed to refer to a specific file or files in `localtest`. Run your tests!
5. To deploy, run `./clean-test-data.sh <app-directory>` then run `./deploy.sh <app-directory>`

## Source management

The application's local `.gitignore` has been updated to ignore the contents of `test-data-cache` and `<app-directory>/localtest`. If you change any of the default paths, you will need to update the `.gitignore` as well. 

