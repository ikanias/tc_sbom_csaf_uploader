import cmd
import random
import os
import subprocess
import time



class TcUpload(cmd.Cmd):
    global token
    def install_oidc(self, cognito_url, client_name, client_id, client_secret):
        print('Checking if OIDC CLI is installed. If not it will be installed...')
        command = 'cargo install oidc-cli'
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = subprocess.check_output(['bash', '-c', command], text=True)
        print(output)
        command = 'oidc create confidential ' + '--issuer ' + cognito_url + ' --client-id ' + client_id + ' --client-secret ' + client_secret + " " + client_name
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = subprocess.check_output(['bash', '-c', command], text=True)
        print(output)
        command = 'oidc token ' + client_name
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = str(subprocess.check_output(['bash', '-c', command], text=True)).rstrip()
        TcUpload.token = str(output)
        print("Your token is: " + TcUpload.token)
        time.sleep(3)

    def create_url_and_curl(self, path, upload_url, url_suffix, client_name):
        files_folder = path
        files_in_folder = os.listdir(files_folder)
        file_count = len(
            [name for name in os.listdir(files_folder) if os.path.isfile(os.path.join(files_folder, name))])
        print("Starting upload...")
        for i in range(file_count):
            file_id = random.randint(0, 1000000)
            suffix = url_suffix + "?id=" + str(file_id)
            all_url = upload_url + suffix
            if (files_in_folder[i].endswith('.json')) or (files_in_folder[i].endswith('.bz2')):
                command = 'curl --header ' + "'Authorization: Bearer " + str(TcUpload.token) + "'" \
                          + ' --location ' + str(all_url) \
                          + ' --upload-file ' + '"{' + str(path + files_in_folder[i]) + '}"' \
                          + ' --header ' + "'Content-Type: application/json" + "'"\
                          + ' --header ' + "'Accept: application/json" + "'"
                subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = subprocess.check_output(['bash', '-c', command], text=True)
                print(output)
                i += 1
            else:
                bad_files = str(files_in_folder[i])
                print('Error: The file you are trying to upload called ' + "'" + bad_files + "'" + ' is not of .json type. Please upload only .json files')
                i += 1
        command = 'oidc delete ' + client_name
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = subprocess.check_output(['bash', '-c', command], text=True)
        print(output)



if __name__ == '__main__':

    print("***Welcome to Trustification file uploader tool on AWS cloud!***")
    cognito_url = input("Please enter your AWS cognito issuer url(i.e. https://foo.bar/user_pool_id) from the AWS cognito console: ") # Enter the cognito URL with the user pool id
    client_name = input("Please enter your token client name(Please make sure it is a unique one): ") # Enter the name for the token you will use
    client_id = input("Please enter your backend (walker) client ID from the AWS cognito console: ") # Enter the walker client ID from the cognito console
    client_secret = input("Please enter the backend (walker) client secret from the AWS cognito console: ") # Enter the client secret under the walker in your AWS cognito console
    path = input("Please enter the path to upload your SBOM or CSAF files from: ")  # Enter the files' path
    upload_url = input("Please enter the server URL to upload the files to: ")   # Enter the remote server URL to upload files
    url_suffix = input("Please enter the URL suffix for your upload i.e. /api/v1/sbom or /api/v1/vex: ") # Enter suffix
    TcUpload().install_oidc(cognito_url, client_name, client_id, client_secret)
    TcUpload().create_url_and_curl(path, upload_url, url_suffix,client_name )

