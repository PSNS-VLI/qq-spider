# BING
BING_RESULT_TITLE = '//li[@class="b_algo"]//h2/a[@target="_blank"]'
BING_RESULT_TITLE_FIRST = '//li[@class="b_algo b_vtl_deeplinks"]//h2/a[@target="_blank"]'
BING_RESULT_FIRST_PREFIX = '//li[@class="b_algo b_vtl_deeplinks"]//h2/a[contains(@href, "'
BING_RESULT_PREFIX = '//li[@class="b_algo"]//h2/a[contains(@href, "'

BING_MAP_CARD = '//div[@class="lgb_cnt"]'
BING_MAP_CARD_TITLE = '//div[@class="lgb_cnt"]//h2/a[@target="_blank"]'
BING_MAP_CARD_ADDRESS = '//div[@class="lgb_cnt"]//div[@class="b_factrow"]//a[@target="_blank"]'

BING_MAP_CARD_SECOND_TITLE = '//span[@class="lc_content"]/h2'
BING_MAP_CARD_SECOND_ADDRESS = '//span[@class="lc_content"]/div[@class="b_factrow"]'

# BAIDU
BAIDU_RESULT_TITLE = '//h3[@class="c-title t t tts-title"]/a'
BAIDU_RESULT_PREFIX = '//h3[@class="c-title t t tts-title"]/a[contains(., "'

RESULT_SUFFIX = '")]'

TYC_DOMAIN = 'tianyancha.com'
TYC_ALIAS = '天眼查'

QXB_DOMAIN = 'qixin.com'
QXB_ALIAS = '启信宝'

QCC_DOMAIN = 'qcc.com'
QCC_ALIAS = '企查查'

AQC_DOMAIN = 'aiqicha.baidu.com'
AQC_ALIAS = '爱企查'

SEARCH_ENGINE = ('BING', 'BAIDU')
PLATFORMS = ('TYC', 'QXB', 'QCC', 'AQC')

# 1 TYC DETAIL_AVAILIABLE
bing_result_tyc_title_first = f'{BING_RESULT_FIRST_PREFIX}{TYC_DOMAIN}{RESULT_SUFFIX}'
bing_result_tyc_title = f'{BING_RESULT_PREFIX}{TYC_DOMAIN}{RESULT_SUFFIX}'
bing_result_tyc_title_first_anchor = f'{bing_result_tyc_title_first}/@href'
bing_result_tyc_title_anchor = f'{bing_result_tyc_title}/@href'

baidu_result_tyc_title = f'{BAIDU_RESULT_PREFIX}{TYC_ALIAS}{RESULT_SUFFIX}'
baidu_result_tyc_title_anchor = f'{baidu_result_tyc_title}/@href'


tyc_search_result_company_name = '//div[@class="index_list-wrap___axcs"]/div[@class="index_search-box__7YVh6"][1]//a[@class="index_alink__zcia5 link-click"]/span'
tyc_search_result_company_address = '//div[@class="index_list-wrap___axcs"]/div[@class="index_search-box__7YVh6"][1]//div[@class="index_contact-row__iYUn6 index_line-row__R3mCi"][2]/div[@class="index_contact-col__7AboU"]/span[2]'

tyc_detail_company_name = '//h1[@class="index_company-name__LqKlo"]'
tyc_detail_company_address = '//span[@class="index_detail-address__ZmaTI"]'

# 2 QXB DETAIL_AVAILIBLE
bing_result_qxb_title_first = f'{BING_RESULT_FIRST_PREFIX}{QXB_DOMAIN}{RESULT_SUFFIX}'
bing_result_qxb_title = f'{BING_RESULT_FIRST_PREFIX}{QXB_DOMAIN}{RESULT_SUFFIX}'
bing_result_qxb_title_first_anchor = f'{bing_result_qxb_title_first}/@href'
bing_result_qxb_title_anchor = f'{bing_result_qxb_title}/@href'

baidu_result_qxb_title = f'{BAIDU_RESULT_PREFIX}{QXB_ALIAS}{RESULT_SUFFIX}'
baidu_result_qxb_title_anchor = f'{baidu_result_tyc_title}/@href'

qxb_detail_company_name = '//h1[@class="d-inline-block f-20 f-bold m-v-0 m-r-10"]'
qxb_detail_company_address = '//span[@class="hover-link cursor-pointer m-r-10"]'

# 3 QCC DETAIL_FORBIDDEN
bing_result_qcc_title_first =  f'{BING_RESULT_FIRST_PREFIX}{QCC_DOMAIN}{RESULT_SUFFIX}'
bing_result_qcc_title = f'{BING_RESULT_PREFIX}{QCC_DOMAIN}{RESULT_SUFFIX}'
bing_result_qcc_title_first_anchor = f'{bing_result_qcc_title_first}/@href'
bing_result_qcc_title_anchor = f'{bing_result_qcc_title}/@href'

baidu_result_qcc_title = f'{BAIDU_RESULT_PREFIX}{QCC_ALIAS}{RESULT_SUFFIX}'
baidu_result_qcc_title_anchor = f'{baidu_result_qcc_title}/@href'

qcc_detail_company_name = '//h1[@class="copy-value"]'
qcc_detail_company_address = '//a[@class="texta"]/span[@class="copy-value"]'

# 4 AQC
bing_result_aqc_title_first =  f'{BING_RESULT_FIRST_PREFIX}{AQC_DOMAIN}{RESULT_SUFFIX}'
bing_result_aqc_title = f'{BING_RESULT_PREFIX}{AQC_DOMAIN}{RESULT_SUFFIX}'
bing_result_aqc_title_first_anchor = f'{bing_result_aqc_title_first}/@href'
bing_result_aqc_title_anchor = f'{bing_result_aqc_title}/@href'

baidu_result_aqc_title = f'{BAIDU_RESULT_PREFIX}{AQC_ALIAS}{RESULT_SUFFIX}'
baidu_result_aqc_title_anchor = f'{baidu_result_aqc_title}/@href'

aqc_detail_company_name = '//h1[@class="name"]'
aqc_detail_company_address = '//span[@class="child-addr-poptip"]'

def __init():
	_global = globals()

	def __generate_selector():
		for p in PLATFORMS:
			for se in SEARCH_ENGINE:
				if se == 'BING':
					TAG = eval(f'{p.upper()}_DOMAIN')
					_global[f'{se}_RESULT_{p}_TITLE_FIRST'.upper()] = \
					f'{BING_RESULT_FIRST_PREFIX}{TAG}{RESULT_SUFFIX}'
					_global[f'{se}_RESULT_{p}_TITLE'.upper()] = \
					f'{BING_RESULT_PREFIX}{TAG}{RESULT_SUFFIX}'
				elif se == 'BAIDU':
					TAG = eval(f'{p.upper()}_ALIAS')
					_global[f'{se}_RESULT_{p}_TITLE'.upper()] = \
					f'{BAIDU_RESULT_PREFIX}{TAG}{RESULT_SUFFIX}'
				else:
					continue
		return None

	def __generate_anchor(c_t, c_t_f):
		for p in PLATFORMS:
			for se in SEARCH_ENGINE:
				_global[f'{se}_RESULT_{p}_TITLE_ANCHOR'.upper()] = \
				f'{c_t(se, p)}/@href'
				if se == 'BING':
					_global[f'{se}_RESULT_{p}_TITLE_FIRST_ANCHOR'.upper()] = \
					f'{c_t_f(se, p)}/@href'
		return None

	__generate_selector()

	def capture_title_without(se, p):
		return capture_title(se, p).replace('//text()', '')

	def capture_title_first_without(se, p):
		return capture_title_first(se, p).replace('//text()', '')

	def capture_title(se, p):
		return eval(f'{se.upper()}_RESULT_{p.upper()}_TITLE')

	def capture_title_first(se, p):
		return eval(f'{se.upper()}_RESULT_{p.upper()}_TITLE_FIRST')

	__generate_anchor(capture_title_without, capture_title_first_without)

	def capture_anchor(se, p):
		return eval(f'{se.upper()}_RESULT_{p.upper()}_TITLE_ANCHOR')

	def capture_anchor_first(se, p):
		return eval(f'{se.upper()}_RESULT_{p.upper()}_TITLE_FIRST_ANCHOR')

	def platform_detail_title(p):
		return eval(f'{p.lower()}_detail_company_name')

	def platform_detail_address(p):
		return eval(f'{p.lower()}_detail_company_address')

	_global['c_t'] = capture_title
	_global['c_t_f'] = capture_title_first
	_global['c_a'] = capture_anchor
	_global['c_a_f'] = capture_anchor_first
	_global['p_d_t'] = platform_detail_title
	_global['p_d_a'] = platform_detail_address

__init()

if __name__ == '__main__':
	# print(aqc_detail_compony_name)
	print(c_t('BAIDU', 'AQC'))
