from bs4 import BeautifulSoup
import requests
import pandas as pd
import openpyxl


class HrefText:
    def __init__(self):
        self.file = "Новости Общества.xlsx"
        self.href_set = []
        self.values_list = []

    def read_hrefs(self):
        """
        Открывается файл созданный в parser.py и читаются ссылки в 5 колонке
        При необходимости и расположении ссылок в другой, поменять параметр name = row[i].value
        Где i - номер колонки, начиная с 0

        :return: 
        """
        workbook = openpyxl.load_workbook(self.file)
        sheet = workbook.worksheets[0]
        v = 0
        s = 0
        for row in sheet:
            if v != 0:
                name = row[4].value
                s += 1
                href = requests.get(name)
                if name != "":
                    if href.status_code == 200:
                        soup = BeautifulSoup(href.text, "html.parser")
                        text = soup.find_all("div", class_="article__text")
                        txt = [i.contents[0] for i in text]
                        self.values_list.append(txt)
                        self.href_set.append(name)
                        print(s)
                    else:
                        print("error")
                        self.href_set.append("error")
                else:
                    break
            v += 1

        df = pd.DataFrame({
                        "url": self.href_set,
                        "text": self.values_list,
                           }
                          )
        df.to_excel(r'news2.xlsx')


if __name__ == "__main__":
    start = HrefText()
    start.read_hrefs()
