from ciaoutil import *

kazoeciao_config.ciao_path("D:/home/Tools/kazoeciao158")
kazoeciao_config.load_config_system()
kazoeciao_config.load_config_autorun()

if True:
	kazoeciao_config.compare_path(
		"D:/home/Python/python_sandbox/test/kazoeciao_cmp_test/before",
		"D:/home/Python/python_sandbox/test/kazoeciao_cmp_test/after")
	kazoeciao_config.enable_autoexec()

file = kazoeciao.exec()
print("End.")
