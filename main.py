# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cmd
import random
import os
import pycurl
import json
from io import BytesIO
from urllib.parse import urlparse


class TcUpload(cmd.Cmd):
    def create_url_and_curl(self, path, url, url_suffix, token):
        buffer = BytesIO()
        curl = pycurl.Curl()
        files_folder = path
        files_in_folder = os.listdir(files_folder)
        upload_url = url
        file_count = len(
            [name for name in os.listdir(files_folder) if os.path.isfile(os.path.join(files_folder, name))])
        print("Starting upload...")
        for i in range(file_count):
            file_id = random.randint(0, 1000000)
            suffix = url_suffix + "?id=" + str(file_id)
            all_url = upload_url + suffix
        #    curl.setopt(pycurl.WRITEDATA, buffer)
        #    curl.setopt(pycurl.POST, 1)
        #    curl.setopt(pycurl.HTTPHEADER, ["Authentication: Bearer " + token])
            curl.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
            curl.setopt(pycurl.HTTPHEADER, ["Authorization: Bearer " + token])
            x = "Authorization: Bearer " + token + "'"
            curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json'])
            curl.setopt(pycurl.URL, all_url)
            curl.perform()
            curl.setopt(pycurl.HTTPPOST, [('fileupload', (pycurl.FORM_FILE, files_in_folder[i]))])
            y = print('Status: %d' % curl.getinfo(pycurl.RESPONSE_CODE))
            if (y == 200) or (y == 201):
                print("Succeeded to upload file")
            else:
                print("Failed to upload file")
            curl.reset()
            i += 1
        curl.close()


if __name__ == '__main__':

    print("***Welcome to Trustification file uploader tool!***")
    path = input("Please enter the path to upload your SBOM or CSAF files from: ")  # Enter the files' path
    url = input("Please enter the server URL to upload the files to: ")   # Enter the remote server URL to upload files
    url_suffix = input("Please enter the URL suffix for your upload i.e. /api/v1/sbom or /api/v1/vex: ") # Enter suffix
    token = input("Please enter the bearer token: ")  # Enter the bearer token of Trustification api server
    TcUpload().create_url_and_curl(path, url, url_suffix, token)

