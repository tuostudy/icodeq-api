# coding:utf-8

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        _html = f.read()
    return _html


def index_html(url_list):
    html = read_file('./api/movie/main.html')
    html = html.replace('{0}', url_list[0])
    html = html.replace('{1}', url_list[1])
    html = html.replace('{2}', url_list[2])
    return html.encode('utf-8')


data = index_html(['41.html', '42.html', '43.html']).decode('utf-8')

print(data)