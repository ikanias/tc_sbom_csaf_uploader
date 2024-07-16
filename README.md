# tc_sbom_csaf_uploader
------------------------
This tool works under the Trustification project (https://github.com/trustification/trustification).
This tool is intended to upload SBOM or CSAF/VEX files of .json type to the Trustification application remote server. \
The way to use it is pretty simple - Just insert the following data after running the command 'python3 main.py': \
**path** - Enter the files' path from which you like to upload the files from \
**url** - Enter the remote Trustificaion server URL where you want your files to be uploaded to \
**url_suffix** - Enter the URL suffix according to the file type you want to upload (i.e. /api/v1/sbom or /api/v1/vex) \
**Bearer token** - The bearer token to use for authorization in front of the remote server. 


tc_sbom_csaf_uploader with automatic token used for AWS cognito
----------------------------------------------------------------
This option reffers to project: https://github.com/ctron/oidc-cli/tree/main

If you do not wish to use a bearer token from the application's UI which expires every 5 minutes, you can use the tc_sbom_csaf_uploader version which uses the oidc_cli tool.
This tool retrieves a token from AWS cognito server and then inserts it to the uploader to use. 
This allows you to upload a lot of files at once for a large amount of time, without worrying that the token will expire. 
In order to use this feature, just select the branch: 'automatic_token'.

To use the tool you need to retrieve the following from the AWS cognito server:

The cognito server URL (i.e. https://example.com/realm)
The App client name
The walker Client ID
The walker Client secret
And to all of these you just add the regular data you used to add in the basic version of the tool:
**path** - Enter the files' path from which you like to upload the files from 
**url** - Enter the remote Trustificaion server URL where you want your files to be uploaded to 
**url_suffix** - Enter the URL suffix according to the file type you want to upload (i.e. /api/v1/sbom or /api/v1/vex) 


tc_sbom_csaf_uploader with automatic token used for non-AWS IDP
----------------------------------------------------------------
This option reffers to project: https://github.com/ctron/oidc-cli/tree/main

This option uses the --root-certificate option of the OIDC CLI tool in order to use a token from a trusted anchor CA for a TPA installation without AWS resources.
In this case, a Cognito idp is not available. This option allows you to use the Keycloak idp using a trusted anchor CA (i.e. tls.crt file).
To do this you need to insert the following data:
idp_url - Enter the idp URL (i.e. Keycloak) with the user pool id
client_name - Enter the name for the token you will use
client_id - Enter the walker client ID from the cognito console
client_secret - Enter the client secret of the walker displayed in your non-AWS idp (i.e. Keycloack idp) console 
path - Enter the SBOM/CSAF files' path from which you want to upload the files from
upload_url - Enter the remote server URL to upload the files to (https://vex-tpa-cluster.net)
url_suffix - Enter suffix according to the files you want to upload. If you want to upload SBOM files then enter /api/v1/sbom, if you want to upload CSAF files enter /api/v1/vex
certificate_path - Enter the trusted anchor certificate you have for the site (i.e. tls.crt file you created according to the instructions here: https://github.com/trustification/trustification/blob/main/docs/modules/admin/pages/cluster-install.adoc)

