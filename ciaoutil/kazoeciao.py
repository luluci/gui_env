"""
かぞえチャオ ユーティリティ
"""
import subprocess
from time import sleep
import pathlib
from .kazoeciao_config import config as kazoeciao_config
from .util.singleton import Singleton

class kazoeciao(Singleton):
	def __init__(self):
		self._config = None
		self._result_dir_files = {}
		self._result_file = None

	def init(self, config: kazoeciao_config):
		self._config = config

	def exec(self) -> str:
		"""
		かぞえチャオを実行する。
		自動実行オプションにて起動し、解析結果ファイルへのパスを返す。
		"""
		# 設定が有効かチェック
		if not self._config.is_enable():
			return None
		# 解析結果フォルダをチェックしておく
		if not self.precheck_result_dir():
			return None
		# かぞえチャオ実行
		if not self.run_process():
			return None
		# 解析結果ファイルを抽出
		if not self.check_result_dir():
			return None
		# 解析結果ファイルのパスを返す
		return self._result_file

	def result_file(self) -> str:
		return self._result_file

	def precheck_result_dir(self) -> bool:
		"""
		かぞえチャオ実行前に解析結果フォルダの中身をチェックしておく
		"""
		# 解析結果フォルダパスを取得
		result_path = self._config.get_result_path()
		if not result_path or not result_path.exists() or not result_path.is_dir():
			# パス未設定、フォルダが存在しない、フォルダでないときはエラー
			return False
		# フォルダ内のファイル一覧を取得
		for indir_path in result_path.iterdir():
			self._result_dir_files[str(indir_path)] = 1
		return True

	def run_process(self) -> bool:
		# かぞえチャオ実行コマンド作成
		cmd = self._config.get_ciaoexe_path()
		# 実行開始
		# 意味はないけどとりあえず非同期で開始、直後で待つ
		proc = subprocess.Popen(cmd)
		result = proc.communicate()
#		while not proc.poll():
#			sleep(1)
#		# return code取得
#		rc = proc.poll()
#		if rc == 0:
#			return True
#		else:
#			return False
		return True

	def check_result_dir(self):
		"""
		かぞえチャオ実行後の解析結果フォルダの中身をチェックして、
		その差分から解析結果ファイルを取得する。
		"""
		# 解析結果フォルダパスを取得
		result_path = self._config.get_result_path()
		if not result_path or not result_path.exists() or not result_path.is_dir():
			# パス未設定、フォルダが存在しない、フォルダでないときはエラー
			return False
		# 解析前ファイル一覧に存在しないファイルを抽出
		result_file = []
		for indir_path in result_path.iterdir():
			if not str(indir_path) in self._result_dir_files:
				result_file.append(str(indir_path))
		self._result_dir_files = {}
		# 抽出したファイルをチェック
		if len(result_file) == 1:
			self._result_file = result_file[0]
			return True
		else:
			return False
