from bs4 import BeautifulSoup


# this function is for the validation checking
def test_valid(string):
    if string in ['', ',', ' ', ';', ':']:
        return False
    return True


# get the content from the table, style1 page. tag name list should be specified
def page_with_table(table, tag_name_list = ['Genres', 'Director', 'Starring', 'MPAA rating']):
    dic = {}
    for tr in table.find_all("tr"):
        tagName = tr.th.string.strip()
#         if tagName in tag_name_list:
        items = []
        for td in tr.find_all("td"):
            for item in td.children:
                if item.string == None:
                    continue
                content = item.string.strip()
                if test_valid(content):
                    items.append(content)
        dic[tagName] = items
    return dic


# get the content from the li, style2 page. tag name list should be specified
def page_with_li(li_list, tag_name_list = ['Language', 'Region', 'Rated', 'Studio', 'DVD Release Date', 'ASIN']):
    processed_list = []
    dic = {}
    for li_item in li_list:
        str_list = li_item.find_all(text=True)
        valid_list = []
        for str_item in str_list:
            if test_valid(str_item.strip()):
                valid_list.append(str_item.strip())
        processed_list.append(valid_list)
    for li_item in processed_list:
        key = li_item[0]
#         if key not in tag_name_list:
#             continue
        li_item.pop(0)
        value = li_item
        dic[key] = value
    return dic


def parser(page_content):
    content = BeautifulSoup(page_content, "lxml")

    # style 1 page
    style1_class = content.find(id="dv-center-features")
    if style1_class != None:
        table = style1_class.find('table')
        dict_content = page_with_table(table)
        img_class = content.find(class_='dp-meta-icon-container')
        dict_content['img'] = img_class.img['src']
        title = content.find(id='aiv-content-title')
        dict_content['title'] = title.text.strip()
        other_format = content.find(class_='dv-cross-linking-other-formats')
        if other_format != None:
            dict_content['other-format'] = other_format.text

    # style 2 page
    style2_class = content.find(id="detail-bullets")
    if style2_class != None:
        ul = style2_class.find('ul')
        li_generator = ul.find_all('li', limit=20)
        dict_content = page_with_li(li_generator)
        img_class = content.find(class_='imgTagWrapper')
        dict_content['img'] = img_class.img['src']
        title = content.find(id='productTitle')
        dict_content['title'] = title.text.strip()
        other_format = content.find(id='tmmSwatches')
        if other_format != None:
            dict_content['other-format'] = other_format.text

    # imdb
    imdb = content.find(class_='imdb-rating')
    if imdb != None:
        score = imdb.strong.text
        dict_content['imdb'] = score

    return dict_content