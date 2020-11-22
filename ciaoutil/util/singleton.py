class Singleton(object):
	_instances = {}

	def __new__(cls):
		if cls not in cls._instances:
			cls._instances[cls] = object.__new__(cls)
		return cls._instances[cls]


"""
Test
"""
if __name__ == "__main__":
	class single1(Singleton):
		def __init__(self):
			self.x = 1
	
	class single2(Singleton):
		def __init__(self):
			self.x = 2
			self.y = "test"

	test1_1 = single1()
	test1_1.x = 10
	test1_2 = single1()
	test1_2.x = 20

	test2_1 = single2()
	test2_1.x = 30
	test2_1.y = "hoge"
	test2_2 = single2()
	test2_2.x = 40
	test2_2.y = "fuga"

	print(test1_1)
	print(test1_2)
	print(test1_1.x)
	print(test1_2.x)
	print(test2_1)
	print(test2_2)
	print(test2_1.x)
	print(test2_1.y)
	print(test2_2.x)
	print(test2_2.y)
