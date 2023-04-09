import requests


class Spider:
    def __init__(self, url):
        self.url = url

    def get_html(self):
        response = requests.get(self.url)
        return response.text

    def parse_html(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # TODO: 解析 HTML 页面，获取需要的数据
        return data

    def save_data(self, data):
        # TODO: 存储数据
        pass

    def run(self):
        html = self.get_html()
        data = self.parse_html(html)
        self.save_data(data)
