import pandas as pd
import os
import json

input_list = [
    "schneider_electric_herobanner",
    "schneider_electric_quicklinks",
    "schneider_electric_tiles",
    "schneider_electric_footer"
]

final_output = {}
content_model_df = pd.read_excel(
    r'C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\config.xlsx', 'CONTENT_MODEL')
component_dataframe = pd.read_excel(
    r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\config.xlsx", "CONTENTFUL_SUB_COMPONENTS", engine='openpyxl')


class Content_model_transform:

    @staticmethod
    def create_entries_json_from_json(entries_input):
        df = []
        dataframe = entries_input[
            ['Component Name' , 'Type of Element' , 'Field Value' , 'Tag' , 'Href' , 'Alt Text' , 'class name']]
        components = sorted(set(dataframe['Component Name'].unique()))
        for component in components:
            entries = {}
            df_final = {
                "properties": {
                    "cq:model": "/conf/Schneider Electric/settings/dam/cfm/models/"+uid ,
                    "name": component ,
                    "description": component ,
                    "elements": {}
                }
            }
            print(df_final)
            df_filtered = dataframe[(dataframe['Component Name'] == component)]
            for row in df_filtered.index:
                comp = component.rsplit("-" , 1)[0]
                type = dataframe.loc[row , "Type of Element"]
                index = component_dataframe.index[(component_dataframe['components'] == comp) & (
                        component_dataframe['src_component_name'] == type)].tolist()
                # print(index,comp,type)

                if len(index) <= 1:
                    # print(str(component_dataframe.loc[index[0] , "tar_component_name"]))
                    key = str(component_dataframe.loc[index[0] , "tar_component_name"])
                    entries = {
                        key: {
                            "title": str(component_dataframe.loc[index[0] , "fields"]),
                            "value": str(dataframe.loc[row , "Field Value"])
                        }
                    }
                    entries.update(entries)
                    df_final["properties"]["elements"].update(entries)
                else:
                    for i in index:
                        key = str(component_dataframe.loc[i , "tar_component_name"])
                        # print(key)
                        if "link" in key:
                            entries = {
                                key: {
                                    "title": str(component_dataframe.loc[i , "fields"]) ,
                                    "value": str(dataframe.loc[row , "Href"])
                                }
                            }
                        elif "field" or "label" in key:
                            entries = {
                                key: {
                                    "title": str(component_dataframe.loc[i , "fields"]) ,
                                    "value": str(dataframe.loc[row , "Field Value"])
                                }
                            }
                        entries.update(entries)
                        df_final["properties"]["elements"].update(entries)
            df.append(df_final)
        return df

for uid in input_list:
    out_file = os.path.join(
        r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\json_aem\\" + uid + "_output.json")
    data = pd.read_excel(
        r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\output\\" + uid + "_output.xlsx")
    entries = Content_model_transform.create_entries_json_from_json(data)
    final_output['Content_Fragment'] = entries
    f = open(os.path.join(out_file) , "w" , encoding='utf8')
    # f = open(os.path.join(out_file), "w")
    f.write(json.dumps(final_output , ensure_ascii=False))
    # f.write(json.dumps(final_output))
    f.close()