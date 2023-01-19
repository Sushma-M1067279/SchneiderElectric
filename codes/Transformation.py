import os
import pandas as pd
from XLPainter import XlPainter

uid = [
    "schneider_electric"
    # "schneider_electric_herobanner",
    # "schneider_electric_quicklinks",
    # "schneider_electric_tiles",
    # "schneider_electric_footer"
]

config_file = r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\config_files\config.xlsx"
MAPPING = pd.read_excel(config_file, "MAPPING")


class cta_transform:

    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            for ind in TH[(TH['Type of Element'] != 'hyperlink')].index:
                TH.drop(ind, inplace=True)
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class hero_banner_transform:

    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            for ind in TH[(TH['class name'] != 'se-font-title3-2 se-rich-text') & (TH['Type of Element'] != 'hyperlink') & (TH['class name'] != 'se-font-text3-0 sdl-banner-full-image-carousel_description se-rich-text')].index:
                TH.drop(ind, inplace=True)
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class header_transform:
    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class short_description_transform:

    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class footer_links_transform:

    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            # TH[(TH['Tag'] == 'div') & (TH['class name'] != 'article-content ')]
            for ind in TH[(TH['Type of Element'] != 'hyperlink') & (TH["class name"] != "title-container")].index:
                TH.drop(ind, inplace=True)
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class tiles_transform:

    def apply(self, df1, components):
        final_df = pd.DataFrame()
        for comp in components:
            TH = df1[df1['Component Name'] == comp]
            for ind in TH[(TH['Type of Element'] != 'image') & (TH['Type of Element'] != 'Heading') &
                          (TH['Type of Element'] != 'hyperlink') & (TH["class name"] != "se-rich-text")].index:
                TH.drop(ind, inplace=True)
            final_df = final_df.append(TH, ignore_index=True)
        return final_df


class Transformation():

    def __init__(self):
        self.component_dataframe = pd.read_excel(config_file, "AEM_COMPONENTS")
        self.component_mapping = pd.read_excel(
            config_file, "COMPONENT_MAPPING")
        self.required_component = pd.read_excel(
            config_file, "AEM_SUB_COMPONENTS")

    def get_class(self, comp):
        print(comp)
        comp_index = self.component_mapping.index[self.component_mapping['src_component_name'] == comp].tolist()[
            0]
        class_name = (
            self.component_mapping.loc[comp_index, 'component_transformation'])
        print(class_name)
        module = __import__('Transformation')
        class_handle = getattr(module, class_name)
        return class_handle()

    @staticmethod
    def pre_processing(data):
        for ind in data[(data['Field Value'] == ' ') & (data['Alt Text'] == ' ') & (data['Href'] == ' ')].index:
            data.drop(ind, inplace=True)
        return data

    @staticmethod
    def remove_duplicates(data):
        data.drop_duplicates(
            subset=["Field Value", "Component Name", "Tag", 'Type of Element'], keep='first', inplace=True)
        return data

    def get_comps(self, comp):
        comp_index = self.required_component.index[self.required_component['components'] == comp + "_fields"].tolist()[
            0]
        comp_list = (
            self.required_component.loc[comp_index, 'sub_components']).split(",")
        return comp_list

    def execute(self, uid, srcfile, out_file):
        df = pd.read_excel(srcfile)
        painter = XlPainter()
        df_final = pd.DataFrame()
        df.dropna(subset=["Field Value"])
        df.fillna(' ', inplace=True)
        df = self.remove_duplicates(df)
        dataframe = df[
            ['Component Name', 'Type of Element', 'Field Value', 'Tag', 'Href', 'Alt Text', 'class name']]
        df1 = Transformation.pre_processing(dataframe)
        comp_index = self.component_dataframe.index[self.component_dataframe['id'] == uid].tolist()[
            0]
        components = (
            self.component_dataframe.loc[comp_index, 'components']).split(',')
        for comp in components:
            component_class = self.get_class(comp)
            comp_list = self.get_comps(comp)
            print(comp_list)
            df2 = component_class.apply(df1, comp_list)
            df_final = df_final.append(df2, ignore_index=True)

        painter.write_DF(df=df_final, sheet_name='data',
                         col_widths=[20, 20, 70, 10, 20, 20, 20],
                         header=True, index=False, outfile=out_file)


if __name__ == "__main__":
    s = Transformation()
    for u in uid:
        srcfile = os.path.join(
            r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\input", u + ".xlsx")
        out_file = os.path.join(
            r"C:\Users\M1067279\PycharmProjects\SchneiderElectric\output", u + "_output.xlsx")
        s.execute(u, srcfile, out_file)
