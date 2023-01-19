import json
import os
import configparser
from contentful_management import Client
from datetime import datetime
import pandas as pd

metadata = configparser.ConfigParser()
metadata.read(
    r'C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\contentful_config.config')
input_list = [
    # "schneider_electric_herobanner",
    "schneider_electric_quicklinks",
    # "schneider_electric_tiles",
    # "schneider_electric_footer"
]


class ContentfulModelLoader:

    def __init__(self):
        self.env = metadata.get('client_secret', 'env')
        self.space_id = metadata.get('client_secret', 'space_id')
        self.token = metadata.get('client_secret', 'key')
        self.client = Client(self.token)
        self.output = []
        self.entries_final = {}

    def contentTypeNotExists(self, content_type_id):
        list = []
        content_models = self.client.content_types(
            self.space_id, self.env).all()
        for content_model in content_models:
            list.append(content_model.id)
        if content_type_id in list:
            return False
        else:
            return True

    def load_to_contentful(self, entries_data):
        error_log = []
        for entry in entries_data["Entries"]:
            try:
                new_entry = self.client.entries(self.space_id, self.env).create(
                    entry['entry_id'],
                    entry
                )
                new_entry.publish()
                print(entry['entry_id'], "uploaded")
            except Exception as e:
                print('skipped in entries ', e)
                error = [entry['content_type_id'], entry['entry_id'], e]
                error_log.append(error)
        df = pd.DataFrame.from_records(data=error_log, columns=[
                                       "model_id", "entry_id", "error_log"])
        df.to_excel("error_log123456.xlsx")

    def uploadContent(self, data, platform):
        error_log = []
        model_data = data.get('Content Model')
        for model in model_data:
            try:
                if self.contentTypeNotExists(model['name']):
                    new_content_type = self.client.content_types(self.space_id, self.env).create(
                        model['name'].lower(),
                        model
                    )
                    try:
                        new_content_type.save()
                    except Exception as e:
                        error = [platform, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), model['name'],
                                 "Not Saved", str(e)]
                        error_log.append(error)
            except Exception as e:
                print(e)
                error = [platform, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), model['name'], 'Not Inserted',
                         str(e)]
                error_log.append(error)
        print(error_log)


l = ContentfulModelLoader()
for i in input_list:
    input_file = os.path.join(
        r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\json_output", i+"_output.json")
    input_data = json.load(open(input_file))
    l.load_to_contentful(input_data)
