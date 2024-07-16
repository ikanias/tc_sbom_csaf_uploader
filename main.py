import cmd
import random
import os
import subprocess
import time





class TcUpload(cmd.Cmd):
    global token
    def install_oidc(self, cognito_url, client_name, client_id, client_secret, certificate_path):
        print('Checking if OIDC CLI is installed. If not it will be installed...')
        files_folder = certificate_path
        files_in_folder = os.listdir(files_folder)
        if 'tls.crt' in files_in_folder:
            print(files_folder + 'tls.crt')
            cert_tls_path = files_folder + 'tls.crt'
        else:
            print('tls.crt was not found in the selected folder. Please make sure you enter a folder where the file resides in.')
        command = 'cargo install oidc-cli'
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output1 = subprocess.check_output(['bash', '-c', command], text=True)
        print(output1)
        command = 'oidc create confidential ' + '--issuer ' + cognito_url + ' --client-id ' + client_id + ' --client-secret ' + client_secret + " " + client_name + ' --root-certificate ' + cert_tls_path
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output2 = subprocess.check_output(['bash', '-c', command], text=True)
        print(output2)
        command = 'oidc token ' + client_name
        subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output3 = str(subprocess.check_output(['bash', '-c', command], text=True)).rstrip()
        TcUpload.token = str(output3)
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
                command = 'curl -k --header ' + "'Authorization: Bearer " + str(TcUpload.token) + "'" \
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

    print("***Welcome to Trustification file uploader tool using non AWS infrastructure!***")
    cognito_url = input("Please enter your idp server issuer url(i.e. https://foo.bar/user_pool_id) from the idp console: ") # Enter the cognito URL with the user pool id
    client_name = input("Please enter your token client name(Please make sure it is a unique one): ") # Enter the name for the token you will use
    client_id = input("Please enter your backend (walker) client ID from the idp console: ") # Enter the walker client ID from the cognito console
    client_secret = input("Please enter the backend (walker) client secret from the idp console: ") # Enter the client secret under the walker in your AWS cognito console
    path = input("Please enter the path to upload your SBOM or CSAF files from: ")  # Enter the files' path
    upload_url = input("Please enter the server URL to upload the files to: ")   # Enter the remote server URL to upload files
    url_suffix = input("Please enter the URL suffix for your upload i.e. /api/v1/sbom or /api/v1/vex: ") # Enter suffix
    certificate_path = input("Please insert the folder of your custom certificate which you created for your site (i.e. trusted anchor): ") # Enter the certificate/trusted anchor certificate you have for the site
    TcUpload().install_oidc(cognito_url, client_name, client_id, client_secret, certificate_path)
    TcUpload().create_url_and_curl(path, upload_url, url_suffix,client_name)

