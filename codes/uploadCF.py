import requests
from requests.auth import HTTPBasicAuth
import json
import os

input_list = [
    "schneider_electric_herobanner",
    "schneider_electric_quicklinks",
    "schneider_electric_tiles",
    "schneider_electric_footer"
]
headers = {'Content-Type': 'application/json'}


class ContentFragmentModelLoader:

    @staticmethod
    def load_to_aem(data_json, uid):
        for data in data_json["Content_Fragment"]:

            contentFragmentPath = "http://localhost:4502/api/assets/schneider-electric/content-fragments/" + \
                uid+"/"+data["properties"]["name"]
            response = requests.post(
                contentFragmentPath, json=data, headers=headers, auth=HTTPBasicAuth('admin', 'admin'))
            print(response)
            if response.status_code == 200 or response.status_code == 201:
                print("Content fragment created successfully.")
            else:
                print("Error creating content fragment.")
                
for i in input_list:
    input_file = os.path.join(
        r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\json_aem", i+"_output.json")
    input_data = json.load(open(input_file))
    ContentFragmentModelLoader.load_to_aem(input_data, i)
