import os
import re
import pathlib
from enum import Enum, auto
import logging
from .util.singleton import Singleton


class config(Singleton):
	"""
	かぞえチャオ設定管理クラス

	Usage:

		(1)かぞえチャオ実行ファイルのパスを指定
		(2)かぞえチャオ設定ファイル読み込み
			設定値が有効であれば自動実行可能となる
			ただし、スクリプト側の設定値は(3)を実行するまで反映されない点に注意
		(3)かぞえチャオ自動実行有効化
	"""

	def __init__(self):
		# かぞえチャオ 制御フラグ
		self._autorun_enabled = False
		# かぞえチャオ ファイル名
		self.file_exe = "kazoeciao.exe"
		self.file_autorun = "autorun.cas"
		self.file_system = "ciaosyst.dat"
		self.dir_result = "./result"
		# かぞえチャオ 各種パス情報
		self.core = {
			"[CIAOEXE]":"",
			"[CIAOPATH]": "",
			"[AFTPATH]": "",
			"[BFRPATH]": "",
			"[RSLPATH]":"",
		}
		# システムオプション
		# http://ciao-ware.c.ooco.jp/ft_sysdt.html
		self.ciaosyst = {
			"[DELIMIT]":[3],
			"[LCNTKND]":[1],
			"[NONEFLG]":[1],
			"[CMPNOFLG]":[0],
			"[MULTFLG]":[0],
			"[DLNONFLG]":{0},
			"[SUBFFLG]":[0],
			"[FOLDCLR]":[0],
			"[DELCFLG]":[0],
			"[USECFLG]":[1],
			"[BDELCFLG]":[0],
			"[CMTMLFLG]": [0],
			"[EOFFLG]": [1],
			"[MDCNTFLG]": [1],
			"[MENUICON]": [1],
			"[MDCUTMAX]": [0],
			"[NEXTLCHK]": [1],
			"[MDCUTFLG]": [1],
			"[MDCMPFLG]": [0],
			"[PREPROCT]": [0],
			"[VIEWCLS]": [0],
			"[CMTCOUNT]": [0],
			"[EXTFILE]": [],
			"[FLDSVFLG]":[0],
			"[AUTOEXEC]": [],
			"[SCHMODE]": [1],
			"[CGSTRFLG]":[0],
		}
		# 自動実行オプション
		# http://ciao-ware.c.ooco.jp/ft_casdt.html
		self.autorun = {
			"[AFTPATH]": [],
			"[BFRPATH]": [],
			"[EXEMODE]": [1],
			"[RSLMODE]": [0],
			"[RSLPATH]": [],
			"[RSLNAME]": ["ciao_rslt"],
			"[MSGMODE]": None,
			"[SCHMODE]": None,
			"[SCHPATH]": None,
			"[SCHSLCT]": None,
			"[RSLSLCT]": None,
			"[COCOPATH]": None,
			"[COCOAUTO]": None,
			"[COCOSLCT]": None,
			"[SYSPATH]": None
		}

	def is_enable(self) -> bool:
		return self._autorun_enabled

	def ciao_path(self, path:str) -> bool:
		# 指定されたパスが存在しなければ異常終了
		p = pathlib.Path(path)
		if not p.exists():
			self.core["[CIAOPATH]"] = ""
			return False
		if p.is_file():
			path = str(p.parent)
			logging.warning("[CIAOPATH]にファイルが指定されてるけど、ディレクトリを指定してね")
		self.core["[CIAOPATH]"] = path
		# かぞえチャオ実行ファイルもチェックしておく
		if not pathlib.Path(path + "/" + self.file_exe).exists():
			self.core["[CIAOEXE]"] = ""
			return True
		self.core["[CIAOEXE]"] = path + "/" + self.file_exe
		return True



	def load_config(self):
		self.load_config_system()
		self.load_config_autorun()

	def load_config_system(self):
		"""
		システムオプションを読み込む。
		読み込むときは既存設定はすべて破棄してから開始する。
		"""
		# システムオプションファイルのパスを作成
		config_path = self.get_config_system_path()
		# ファイル存在チェック
		if config_path.exists():
			self.ciaosyst = {}
			self.load_config_impl(config_path, self.ciaosyst)
		# 設定ファイルの設定が有効であれば自動実行可能とする
		self.check_autorun_enabled()

	def load_config_autorun(self):
		"""
		自動実行オプションを読み込む。
		読み込むときは既存設定はすべて破棄してから開始する。
		"""
		# 自動実行オプションファイルのパスを作成
		config_path = self.get_config_autorun_path()
		# ファイル存在チェック
		if config_path.exists():
			self.autorun = {}
			self.load_config_impl(config_path, self.autorun)
		# 設定ファイルの設定が有効であれば自動実行可能とする
		self.check_autorun_enabled()

	def load_config_impl(self, path:pathlib.Path, config_dict:dict):
		"""
		設定ファイル読み込み(共通処理)
		"""
		"""
		Record定義, 解析状態
		[KEY]
		VALUE
		"""
		class Record(Enum):
			KEY = auto()
			VALUE = auto()
		class AnalyzeState(Enum):
			INIT = auto()
			KEY = auto()
			VALUE = auto()
		# ファイルから全行読み込む
		lines = None
		with open(path) as f:
			lines = f.readlines()
		# dictに取り込む
		state = AnalyzeState.INIT
		record = None
		key = None
		values = []
		for line in lines:
			# 読み込んだ文字列のRecordタイプ判定
			line = ''.join(line.splitlines())
			if re.search('^\[.+\]$', line):
				record = Record.KEY
			else:
				record = Record.VALUE
			# 状態管理
			if state == AnalyzeState.INIT:
				if record == Record.KEY:
					# 初期状態からKEYを検出して解析開始
					key = line
					values = []
					state = AnalyzeState.KEY
				else:
					# 初期状態からVALUEが出現するのは不正
					logging.error('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
					raise Exception('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)

			elif state == AnalyzeState.KEY:
				if record == Record.VALUE:
					# VALUEを取得
					if line != "":
						values.append(line)
					state = AnalyzeState.VALUE
				else:
					# KEYが連続で出現するのは不正
					logging.error('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
					raise Exception('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
			elif state == AnalyzeState.VALUE:
				if record == Record.KEY:
					# 次のkeyが出現したらこれまでの出現分を登録
					config_dict[key] = values
					# 次の解析を開始
					key = line
					values = []
					state = AnalyzeState.KEY
				elif record == Record.VALUE:
					# valueの連続出現は受け付ける
					if line != "":
						values.append(line)
					state = AnalyzeState.VALUE
				else:
					# 不正データ出現
					logging.error('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
					raise Exception('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
			else:
				# 不正データ出現
				logging.error('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)
				raise Exception('設定ファイル読み込みエラー, ファイルが壊れてるよ: ' + path)

	def check_autorun_enabled(self):
		"""
		かぞえチャオ設定ファイルの内容で自動実行が可能かチェックする
		"""
		autorun_enabled = True
		# かぞえチャオフォルダが設定されていなければNG
		if self.core["[CIAOPATH]"] == "" or self.core["[CIAOEXE]"] == "":
			autorun_enabled = False
		# [AUTOEXEC]の設定が本スクリプト準拠でなければNG
		if not self.check_config_autoexec_path():
			autorun_enabled = False
		# [BFRPATH],[AFTPATH],[RSLPATH]が未設定or存在しなければNG
		if not self.check_config_autorun_path("[BFRPATH]"):
			autorun_enabled = False
		if not self.check_config_autorun_path("[AFTPATH]"):
			autorun_enabled = False
		if not self.check_config_autorun_path("[RSLPATH]"):
			autorun_enabled = False
		# 判定結果に応じて設定調整
		if autorun_enabled:
			self._autorun_enabled = True
		else:
			self._autorun_enabled = False

	def check_config_autoexec_path(self) -> bool:
		check = False
		if self.ciaosyst["[AUTOEXEC]"]:
			config_path = pathlib.Path(self.ciaosyst["[AUTOEXEC]"][0])
			core_path = pathlib.Path(self.core["[CIAOPATH]"] + "/" + self.file_autorun)
			if config_path == core_path:
				check = True
		return check

	def check_config_autorun_path(self, key: str) -> bool:
		check = True
		# 設定ファイルの内容が有効かどうかをチェックする
		if not self.autorun[key]:
			check = False
		else:
			path = self.autorun[key][0]
			# 未設定はNG
			if path == "":
				check = False
			else:
				# 設定されたパスが存在しなければNG
				if not pathlib.Path(path).exists():
					check = False
		return check



	def compare_path(self, before_path: str, after_path: str) -> bool:
		check = True
		# check before
		if self.check_compare_path(before_path):
			self.core["[BFRPATH]"] = before_path
		else:
			self.core["[BFRPATH]"] = ""
			check = False
		# check after
		if self.check_compare_path(after_path):
			self.core["[AFTPATH]"] = after_path
		else:
			self.core["[AFTPATH]"] = ""
			check = False

	def check_compare_path(self, path: str) -> bool:
		check = True
		# 設定ファイルの内容が有効かどうかをチェックする
		# 未設定はNG
		if path == "":
			check = False
		else:
			# 設定されたパスが存在しなければNG
			if not pathlib.Path(path).exists():
				check = False
		return check

	def result_path(self, path: str) -> None:
		self.dir_result = path

	def enable_autoexec(self) -> bool:
		"""
		オプションを書き換えて自動実行を有効にする。
		パスのチェックも実施する。
		"""
		# 解析結果フォルダチェック
		self.path_check_result()
		# 存在チェック済みのため、空文字列でなければ設定有効
		if self.core["[CIAOEXE]"] == "" or self.core["[CIAOPATH]"] == "" or self.core["[AFTPATH]"] == "" or self.core["[BFRPATH]"] == "":
			self._autorun_enabled = False
			return False
		# 自動実行オプション
		self.ciaosyst["[AUTOEXEC]"] = [self.core["[CIAOPATH]"] + "/" + self.file_autorun]
		self.autorun["[BFRPATH]"] = [self.core["[BFRPATH]"]]
		self.autorun["[AFTPATH]"] = [self.core["[AFTPATH]"]]
		self.autorun["[RSLPATH]"] = [self.core["[RSLPATH]"]]
		# 設定ファイル更新
		self.save_config_system()
		self.save_config_autorun()
		self._autorun_enabled = True
		return True

	def path_check_result(self) -> bool:
		result_path = pathlib.Path(self.dir_result)
		# 相対パスであれば [CIAOPATH] を起点に絶対パスへ変換
		if not result_path.is_absolute():
			result_path = pathlib.Path(
				self.core["[CIAOPATH]"] + self.dir_result).resolve()
		# ディレクトリ存在チェック
		if not result_path.exists():
			result_path.mkdir()
		# パスを記憶
		self.core["[RSLPATH]"] = str(result_path)
		return True

	def save_config_system(self):
		"""
		システムオプションをファイルへ書き出す。
		"""
		# システムオプションファイルのパスを作成
		config_path = self.get_config_system_path()
		# ファイル書き出し
		self.save_config_impl(config_path, self.ciaosyst)

	def save_config_autorun(self):
		"""
		自動実行オプションをファイルへ書き出す。
		"""
		# 自動実行オプションファイルのパスを作成
		config_path = self.get_config_autorun_path()
		# ファイル書き出し
		self.save_config_impl(config_path, self.autorun)

	def save_config_impl(self, path: pathlib.Path, config_dict: dict):
		with path.open(mode='w') as fs:
			for key in config_dict:
				# valueが空でないときファイルへ書き出す
				# valueが None または [] でないとき、という判定ができてる
				if config_dict[key]:
					fs.write(key)
					fs.write('\n')
					for value in config_dict[key]:
						fs.write(str(value))
						fs.write('\n')


	def get_config_system_path(self) -> pathlib.Path:
		return pathlib.Path(self.core["[CIAOPATH]"] + "/" + self.file_system)

	def get_config_autorun_path(self) -> pathlib.Path:
		return pathlib.Path(self.core["[CIAOPATH]"] + "/" + self.file_autorun)

	def get_result_path(self) -> pathlib.Path:
		"""
		解析結果フォルダへのパスを返す

		自動実行可能状態でなければNoneを返す
		"""
		result_path = None
		# 自動実行可能であればself.autorunがセットされている
		if self.autorun["[RSLPATH]"][0] != "":
			result_path = pathlib.Path(self.autorun["[RSLPATH]"][0])
		return result_path

	def get_ciaoexe_path(self) -> str:
		return self.core["[CIAOEXE]"]
