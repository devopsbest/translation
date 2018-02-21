import langid
import numpy as np
import pandas as pd
import requests

LANGUAGES = ['ar', 'de', 'en', 'es', 'fr', 'it', 'ja-JP', 'ko-KR', 'pt-BR', 'ru', 'th', 'tr-TR', 'zh-cn', 'zh-HK',
             'zh-TW']
ID = ['699126', '699124', '669751', '647306', '697256', '647306']
host = "qa"
url = "http://{}.englishtown.com/services/school/query?q=blurb!{}&c=culturecode={}"

list_obj = []


class Translate():
    def get_translated_string(self, blurb_id, language_code):
        response = requests.post(url.format(host, blurb_id, language_code))
        value = (response.json())[0]['translation'].strip()
        # print(value)
        return value

    def check_language(self, target, language):
        lineTuple = langid.classify(target)  # 调用langid来对该行进行语言检测
        if "-" in language:
            language = language.split("-")[0]
        if lineTuple[0] != language:
            return False
        else:
            return True


def main():
    translate = Translate()
    translated = (translate.get_translated_string(x, y) for x in ID for y in LANGUAGES)

    translated_list = np.array(list(translated)).reshape(len(ID), len(LANGUAGES))

    translated_dataframe = pd.DataFrame(translated_list, index=ID, columns=LANGUAGES)

    check_dataframe = translated_dataframe.copy()

    for ix, row in check_dataframe.iterrows():
        for col_name in check_dataframe.columns:
            # print("\n")
            # print (row[col_name])
            if not translate.check_language(row[col_name], col_name):
                list_obj.append(ix + ":" + col_name)

    print(list_obj)
    writer = pd.ExcelWriter('check_translated_blurbs.xlsx')
    check_dataframe.to_excel(writer, 'not_translated')


if __name__ == "__main__":
    main()
