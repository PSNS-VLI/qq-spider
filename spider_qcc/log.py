import time

class Log:
	def __init__(self, log_path: str, log_name: str = None):
		self.path = log_path
		self.name = \
		f'{log_path}{log_name or time.strftime("%Y%m%d_%H%M.log")}'
		self.__file = open(self.name, 'a', encoding = 'utf-8')

	def __del__(self):
		self.__file.close()

	def v(self, text):
		self.__write_to_file(self.__generate_text(f'VERBOSE: {text}'))

	def d(self, text):
		self.__write_to_file(self.__generate_text(f'DEBUG: {text}'))
	
	def i(self, text):
		self.__write_to_file(self.__generate_text(f'INFO: {text}'))

	def w(self, text):
		self.__write_to_file(self.__generate_text(f'WARNING: {text}'))

	def e(self, text):
		self.__write_to_file(self.__generate_text(f'ERROR: {text}'))

	def __generate_text(self, text):
		t = f'{self.__get_time()}{text}'
		print(t, flush = True)
		return t

	def __write_to_file(self, text):
			self.__file.write(f'{text}\n')

	def __get_time(self):
		return time.strftime('[%Y-%m-%d@%H:%M:%S]')

if __name__ == '__main__':
	L = Log('data/log/', 'test.log')
	L.v('Hello')
	L.d('Hello')
	L.i('Hello')
	L.w('Hello')
	L.e('Hello')
