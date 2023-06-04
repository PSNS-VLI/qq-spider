import json
import time
from log import Log
from agent import XlsxAgent
from spider import Spider, Page
from calculator import TextCalculator as TC
from selector import *
from settings import *

def main():
    def filtering_data(page: Page, se: str, log: Log = None) -> list:
        L = log or Log(LOG_SAVE_PATH, 'filtering_data.log')
        _data = []
        for p in PLATFORMS:
            title = page.locate_element(c_t(se, p))
            anchor = page.locate_element(c_a(se, p))
            if len(title) > 0:
                for i in range(len(title)):
                    _data.append({'title': title[i], 'anchor': anchor[i],
                        'tag': p})

            if se == Page.BING:
                # Bing First
                title = page.locate_element(c_t_f(se, p))
                anchor = page.locate_element(c_a_f(se, p))
                if len(title) > 0:
                    for i in range(len(title)):
                        _data.append({'title': title[i], 'anchor': anchor[i],
                            'tag': p})
            L.i(f'Platform {p} crawls {len(_data)} pieces of data.')
        if se == Page.BING:
            # Bing Map Card
            title = page.locate_element(BING_MAP_CARD_TITLE)
            address = page.locate_element(BING_MAP_CARD_ADDRESS)
            if len(title) > 0:
                for i in range(len(title)):
                    _data.append({'title': title[i], 'address': address[i],
                        'tag': 'BingMapCard'})
                L.i(f'Bing Map Card find {len(title)} pieces of data.')
            # Bing Map Card Second situation
            title = page.locate_element(BING_MAP_CARD_SECOND_TITLE)
            address = page.locate_element(BING_MAP_CARD_SECOND_ADDRESS)
            if len(title) > 0:
                for i in range(len(title)):
                    _data.append({'title': title[i], 'address': address[i],
                        'tag': 'BingMapCardSecond'})
                L.i(f'Bing Map Card Second find {len(title)} pieces of data.')
        L.i(f'{company} totally find {len(title)} pieces of data.')
        return _data

    def extract_data(data: list, log: Log = None, spider: Spider = None) -> list:
        L = log or Log(LOG_SAVE_PATH)
        spider = spider or Spider(FIREFOX_PATH)
        result = []
        total_num = len(data)
        for index, item in enumerate(data):
            possible = []
            for se in SEARCH_ENGINE_LIST:
                possible += item.get(se, [])
            company = item['company']
            L.i(f'Extracting section {index+1}/{total_num} data.')
            try:
                _d = {}
                if len(possible) == 0:
                    L.i(f'Data not found. Number [{index+1}] [{company}]')
                    _d = {
                        'en': company,
                        'zh': '',
                        'address': ''
                    }
                elif len(possible) == 1:
                    L.i(f'Only one number. Number [{index+1}] named [{company}].')
                    _d = {
                        'en': company,
                        'zh': possible[0]['title'],
                        'address': item.get('address', '')
                    }
                else:
                    L.i('Multiple matched value. ' + \
                        f'Number [{index+1}] named [{company}].')
                    possible =  TC.sort_dict_by_similar(possible, 'title')
                    # L.i(f'Possible value {possible}.')
                    obj = possible[0]['item']
                    p = obj['tag']
                    if p in ('TYC', 'QXB', 'AQC', 'QCC'):
                        L.i(f'Platform {p} find [{company}]')
                        Spider.random_delay(f'EXTRACT AT {p}',
                            SPIDERING_RANDOM_DELAY)
                        page = spider.search(target = obj['anchor'])
                        title = page.locate_element(p_d_t(p))
                        address = page.locate_element(p_d_a(p))
                        if len(title) > 0:
                            L.i('The optimum value. ' + \
                                f'[{title[0]}].')
                            _d = {
                                'en': company,
                                'zh': title[0],
                                'address': address[0] if len(address) > 0 else ''
                            }
                        else:
                            L.i(f'Platform {p} frbidden.')
                            _d = {
                                'en': company,
                                'zh': obj['title'],
                                'address': address[0] if len(address) > 0 else ''
                            }
                    elif p in ('BingMapCardSecond', 'BingMapCard'):
                        L.i(f'Bing Map find [{company}].')
                        _d = {
                            'en': company,
                            'zh': obj['title'],
                            'address': obj.get('address', '')
                        }
                    else:
                        L.w('The program went into an unexpected branch.')
                        _d = {
                            'en': company,
                            'zh': obj['title'],
                            'address': ''
                        }
                result.append(_d)
            except Exception as error:
                L.e(error)
                L.e('An exception occurs during data extracting. ' + \
                    f'The extracted data total {len(result)} is returned.')
                L.e(f'Exceptions may occur in \n {data[len(result)]}.')
                result.append({'en': company, 'zh': '', 'address': ''})
                Spider.random_delay('ERROR DELAY', SPIDERING_RANDOM_DELAY)
                continue
        return result

    def storage_data(data, file_name):
    
        _path = f'{TEMP_JSON_PATH}{time.strftime("%Y-%m-%d@%H-%M@")}{file_name}'
        with open(_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False))
            
        return _path

    def read_data(_path):
        with open(_path, 'r', encoding='utf-8') as f:
            return json.loads(f.read())

    # initial excel agent
    L = Log(LOG_SAVE_PATH)
    agent = XlsxAgent(EXCEL_FILE_PATH)
    L.i('File agent have loaded.')
    agent.set_scope(EXCEL_START_ROW, EXCEL_START_COL, EXCEL_END_ROW,
        EXCEL_END_COL)
    excel_data = agent.read_data_with_head()
    table = excel_data.get('data', [])
    table_head = excel_data.get('head', [])
    del excel_data
    pre_data = []
    error_data = []
    L.i('Spider loading...')
    spider = Spider(FIREFOX_PATH)
    L.i('Spider have loaded.')
    total_num = len(table)
    L.i(f'Total current tasks: {total_num}')

    L.i('About to start task.')
    for i in range(total_num):
        try:
            if i != 0:
                Spider.random_delay(
                    f'company: [{company}] / PROGRESS: {i+1}/{total_num}',
                    SPIDERING_RANDOM_DELAY)
            item = {}
            company = table[i][0]
            item['company'] = company
            for se in SEARCH_ENGINE_LIST:
                try:
                    L.i('Spidering data: ' + \
                        f'number [{i+1}] form [{se}] named [{company}].')
                    item[se] = filtering_data(
                        spider.search(company, search_engine = se),
                        se, L)
                    if se == Page.BING:
                        Spider.random_delay(f'PAGE DELAY', PER_PAGE_RANDOM_DELAY)
                except Exception as error:
                    L.e(error)
                    L.e(f'Spidering {se} error')
                    item[se] = []
                    continue
            pre_data.append(item)
        except Exception as error:
            L.e(error)
            _path = storage_data({'data': pre_data, 'table': table},
                'pre_data.json')
            L.e('An exception occurs during data crawling. ' + \
                f'The crawled data total [{len(pre_data)}] is saved in [{_path}].')
            L.w('The faulty data has been recorded.')
            error_data.append({'index': i, 'company': company})
            L.w(f'We are going to fill out the data with [{company}].')
            _item = {
                'BING': item.get('BING', []),
                'BAIDU': item.get('BAIDU', []),
                'company': company
            }
            pre_data.append(_item)
            L.w('Program will continue.')
            continue

    # save error_data
    _path = storage_data({'data': error_data}, 'error_data.json')
    L.w(f'Error data saved at {_path}')

    # save pre_data
    _path = storage_data({'data': pre_data, 'table': table}, 'pre_data.json')
    L.i(f'Crude data saved at {_path}')

    # finally handle
    L.i('Ready to extract data from pre_data.')
    finally_data = extract_data(pre_data, L, spider)
    _path = storage_data({'data': finally_data}, 'finally_data.json')
    L.i(f'The data have been extracted and saved in [{_path}].')

    # release memory
    del spider
    del pre_data
    del error_data

    # save data
    L.i('Ready save data. Please wait...')
    for index, row in enumerate(table):
        title = finally_data[index].get('zh', '')
        address = finally_data[index].get('address', '')
        row.insert(0, title)
        # TODO Address
        row.insert(2, address) 
    table_head.insert(0, '企业中文名称')
    table_head.insert(2, '企业中文地址')
    table.insert(0, table_head)
    agent.save_as(table, output_path = EXCEL_SAVE_PATH,
        factory = lambda cell: XlsxAgent.bg_color_factory(cell) 
        if cell.value == '' else None)
    L.i(f'Excel saved at {EXCEL_SAVE_PATH}.')

    return None

main()
