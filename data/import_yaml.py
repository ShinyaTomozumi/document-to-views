from typing import List, Type
from models.yaml_views import YamlViews
from models.parameter_config import ParameterConfig
import yaml
import re


class ImportYaml:
    """
    Yamlで取り込んだデータのクラス
    """
    version: str
    copyright: str
    author: str
    description: str
    views: List[YamlViews]

    def __init__(self, parameter_config: ParameterConfig):
        """
        初期化処理
        :param parameter_config:
        """
        # 初期化
        self.views = []

        # yamlファイルの読み込み
        with open(parameter_config.input_files_path, 'r') as yml:
            yaml_info = yaml.safe_load(yml)

        # yamlの情報を設定する
        self.version = yaml_info['version']
        self.description = yaml_info['description']
        if 'copyright' in yaml_info:
            self.copyright = yaml_info['copyright']
        if 'author' in yaml_info:
            self.author = yaml_info['author']

        # Viewのデータ情報を設定する
        views = yaml_info['views']

        for key, view in views.items():
            # キーが存在しない場合はエラーを表示してcontinue
            if not key:
                print('Parameter is none: ' + key)
                continue

            # viewsの必須パラメータチェック
            require_parameters = ['title', 'url', 'description']
            require_flg = True
            for parameter in require_parameters:
                if parameter not in view:
                    print('Not set parameters: {}: '.format(parameter) + key)
                    require_flg = False
            if not require_flg:
                # 必須パラメータが存在しない場合はcontinue
                continue

            # View データを設定する
            yaml_views = YamlViews()
            yaml_views.id = key
            yaml_views.title = view['title']
            yaml_views.url = view['url']
            yaml_views.description = view['description']
            if 'middleware' in view:
                yaml_views.middleware = view['middleware']

            # URLにパスパラメータの設定確認
            url_path_params = re.findall("(?<=\{).+?(?=\})", yaml_views.url)
            if len(url_path_params) > 0:
                # パスパラメータが存在する場合は設定する
                yaml_views.path = url_path_params

            # queryの設定
            if 'query' in view:
                yaml_views.middleware = view['query']

            # Add views
            self.views.append(yaml_views)
