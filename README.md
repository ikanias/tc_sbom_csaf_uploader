# tc_sbom_csaf_uploader
------------------------
This tool works under the Trustification project (https://github.com/trustification/trustification) and the Exhort project (https://github.com/RHEcosystemAppEng/exhort)

This tool is intended to upload SBOM or CSAF/VEX files of .json type to the Trustification application remote server. \
The way to use it is pretty simple - Just insert the following data after running the command 'python3 main.py': \
**path** - Enter the files' path from which you like to upload the files from \
**url** - Enter the remote Trustificaion server URL where you want your files to be uploaded to \
**url_suffix** - Enter the URL suffix according to the file type you want to upload (i.e. /api/v1/sbom or /api/v1/vex) \
**Bearer token** - The bearer token to use for authorization in front of the remote server. 

tc_sbom_csaf_uploader with automatic token
-------------------------------------------
This option reffers to project: https://github.com/ctron/oidc-cli/tree/main

If you do not wish to use a bearer token from the application's UI which expires every 5 minutes, you can use the tc_sbom_csaf_uploader
version which uses the oidc_cli tool. This tool retrieves a token from AWS cognito and then insert it to the uploader to use.
This allows you to upload a lot of files at once for a large amount of time, without worrying that the token will expire.
I order to use this feature, just select the branch: 'automatic_token'.
In order to do that you need to retrieve the following from the AWS cognito server:
1. The cognito server URL (i.e. https://example.com/realm)
2. The App client name 
3. The walker Client ID
4. The walker Client secret
And to tall of these you just adding the regular data you added in the basic version of the tool (Folder to upload the files from,
remote server to upload the files to etc...)

