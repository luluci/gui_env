import logging
from .kazoeciao_config import config as kc_config
from .kazoeciao import kazoeciao as kc

logging.basicConfig(format='%(filename)s(%(lineno)d): %(message)s')

# かぞえチャオ設定管理クラスを作成
kazoeciao_config = kc_config()
# かぞえチャオ実行管理クラスを作成
kazoeciao = kc()
kazoeciao.init(kazoeciao_config)
