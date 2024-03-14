# trustification-files-upload
This tool is intended to upload SBOM or CSAF/VEX files of .json type to the Trustification application remote server. \
The way to use it is pretty simple - Just insert the following data after running the command 'python3 main.py': \
**path** - Enter the files' path from which you like to upload the files from \
**url** - Enter the remote Trustificaion server URL where you want your files to be uploaded to \
**url_suffix** - Enter the URL suffix according to the file type you want to upload (i.e. /api/v1/sbom or /api/v1/vex) \
**Bearer token** - The bearer token to use for authorization in front of the remote server. \
