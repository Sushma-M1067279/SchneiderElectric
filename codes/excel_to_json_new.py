import pandas as pd
import os
import json

uid = "schneider_electric_footer"
final_output = {}
out_file = os.path.join(
    r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\json output\schneider_electric_footer_output.json")
content_model_df = pd.read_excel(
    r'C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\config.xlsx', 'CONTENT_MODEL')
component_dataframe = pd.read_excel(
    r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\config.xlsx", "CONTENTFUL_SUB_COMPONENTS", engine='openpyxl')


class Content_model_transform:
    def create_entries_json_from_json(self , entries_input):
        df = []
        dataframe = entries_input[
            ['Component Name' , 'Type of Element' , 'Field Value' , 'Tag' , 'Href' , 'Alt Text' , 'class name']]
        components = sorted(set(dataframe['Component Name'].unique()))
        for component in components:
            entries = {}
            df_final = {"content_type_id": uid , "entry_id": component , "fields": {
            }}
            df_filtered = dataframe[(dataframe['Component Name'] == component)]
            for row in df_filtered.index:
                comp = component.rsplit("-" , 1)[0]
                type = dataframe.loc[row , "Type of Element"]
                index = component_dataframe.index[(component_dataframe['components'] == comp) & (
                        component_dataframe['src_component_name'] == type)].tolist()
                print(index,comp,type)
                if len(index) <= 1:
                    print(str(component_dataframe.loc[index[0] , "tar_component_name"]))
                    key = str(component_dataframe.loc[index[0] , "tar_component_name"])
                    entries = {
                        key: {
                            "en-US": str(dataframe.loc[row , "Field Value"])
                        }
                    }
                    entries.update(entries)
                    df_final["fields"].update(entries)
                else:
                    for i in index:
                        key = str(component_dataframe.loc[i , "tar_component_name"])
                        print(key)
                        if "link" in key:
                            entries = {
                                key: {
                                    "en-US": str(dataframe.loc[row , "Href"])
                                }
                            }
                        elif "field" or "label" in key:
                            entries = {
                                key: {
                                    "en-US": str(dataframe.loc[row , "Field Value"])
                                }
                            }
                        entries.update(entries)
                        df_final["fields"].update(entries)
            df.append(df_final)
        return df


s = Content_model_transform()
data = pd.read_excel(
    r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\output\schneider_electric_footer_output.xlsx")
entries = s.create_entries_json_from_json(data)
final_output['Entries'] = entries
f = open(os.path.join(out_file), "w", encoding='utf8')
# f = open(os.path.join(out_file), "w")
f.write(json.dumps(final_output, ensure_ascii=False))
# f.write(json.dumps(final_output))
f.close()
