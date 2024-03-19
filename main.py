import cmd
import random
import os
import subprocess





class TcUpload(cmd.Cmd):
    def create_url_and_curl(self, path, url, url_suffix, token):
        files_folder = path
        files_in_folder = os.listdir(files_folder)
        file_count = len(
            [name for name in os.listdir(files_folder) if os.path.isfile(os.path.join(files_folder, name))])
        print("Starting upload...")
        for i in range(file_count):
            file_id = random.randint(0, 1000000)
            suffix = url_suffix + "?id=" + str(file_id)
            all_url = url + suffix
            command = 'curl --header ' + "'Authorization: Bearer " + str(token) + "'" \
                      + ' --location ' + str(all_url) \
                      + ' --upload-file ' + '"{' + str(path + files_in_folder[i]) + '}"' \
                      + ' --header ' + "'Content-Type: application/json" + "'"\
                      + ' --header ' + "'Accept: application/json" + "'"
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = subprocess.check_output(['bash', '-c', command])
            print(output)
            i += 1


if __name__ == '__main__':

    print("***Welcome to Trustification file uploader tool!***")
    path = input("Please enter the path to upload your SBOM or CSAF files from: ")  # Enter the files' path
    url = input("Please enter the server URL to upload the files to: ")   # Enter the remote server URL to upload files
    url_suffix = input("Please enter the URL suffix for your upload i.e. /api/v1/sbom or /api/v1/vex: ") # Enter suffix
    token = input("Please enter the bearer token: ")  # Enter the bearer token of Trustification api server
    TcUpload().create_url_and_curl(path, url, url_suffix, token)
