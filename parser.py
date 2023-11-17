from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd


class NewsInformation:
    def __init__(self):
        self.date_list = []
        self.headers = {
            'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
            'like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        }
        self.news_page = 0
        self.url_archive = None
        self.data_list = []
        self.title_list = []
        self.url_list = []
        self.show_list = []
        self.tag_list = []

    def generate_datalist(self):
        """
        Данная функция генерирует лист с датами для дальнейшего поиска новостей.
        Данный скрипт выполняется медленно, так можно избежать частого запроса к сайту и блокировки соединения

        Если оперативная память компьютера не позволяет хранить много информации в массивах, то
        необходимо поменять start_date, end_date под более короткие периоды запроса.

        В конце функция сохраняет данные в xlsx файл

        :return: None
        """
        date_format = '%Y%m%d'
        step = datetime.timedelta(days=1)
        start_date = datetime.datetime.strptime("20230801", date_format)
        end_date = datetime.datetime.strptime("20231115", date_format)
        while start_date <= end_date:
            self.date_list.append(start_date.strftime(date_format))
            start_date += step

        for i in self.date_list:
            self.parsing_daily_news(i)
            print(i)

        df = pd.DataFrame({
                        "date": self.data_list,
                        "title": self.title_list,
                        "url": self.url_list,
                        "show": self.show_list,
                        "tags": self.tag_list
                           }
                          )
        df.to_excel(r'mydata0801.xlsx')

    def parsing_daily_news(self, data_day):
        """
        Данная функция парсит сайт. Для корректной работы необходимо проверить,что данные ссылки еще активны
        Try - Except перехватывает скрытые статьи, которые не парсятся в полном объеме и ломают нумерацию.

        :param data_day: day from function
        :return: None
        """
        try:
            for i in range(1, 30):
                number_page = i
                self.url_archive = f"https://ria.ru/{data_day}/?page={number_page}"
                page = requests.get(self.url_archive, headers=self.headers)
                response = page.status_code
                if response == 200:
                    soup = BeautifulSoup(page.text, "html.parser")
                    news = soup.find_all('a', class_="list-item__title color-font-hover-only")
                    shows = soup.find_all('div', class_="list-item__views-text")
                    tags = soup.find_all('div', class_="list-item__tags-list")

                    i_i = 0
                    for dd in news:
                        data = news[i_i]
                        title = data.contents[0]
                        href = data["href"]
                        show_int = shows[i_i]
                        show = show_int.contents[0]
                        tag = tags[i_i]
                        tags_1 = [i.contents[0] for i in tag.find_all("span", class_="list-tag__text")]
                        self.show_list.append(show)
                        self.tag_list.append(tags_1)
                        self.data_list.append(datetime.datetime.strptime(data_day, "%Y%m%d").date())
                        self.title_list.append(title)
                        self.url_list.append(href)
                        i_i += 1
                else:
                    pass
        except:
            pass


if __name__ == "__main__":
    start = NewsInformation()
    start.generate_datalist()
