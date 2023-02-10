import re
import os
import datetime
import shutil

from models.parameter_config import ParameterConfig
from data.import_views_base import ImportViewsBase
import lib.name_case_convert


class NextJs:
    """
    Next.js のソース作成クラス
    """
    _parameter_config: ParameterConfig
    _import_views: ImportViewsBase
    _template_dir: str
    _SOURCE_TYPE = 'next_js'

    def __init__(self, parameter_config: ParameterConfig, import_view_base: ImportViewsBase):
        """
        初期化
        :param parameter_config:
        :param import_view_base:
        """
        self._parameter_config = parameter_config
        # 出力先のフォルダの初期化設定
        if self._parameter_config.output_dir_path == '':
            self._parameter_config.output_dir_path = 'output_views_' + self._SOURCE_TYPE
        self._import_views = import_view_base

        # テンプレートソースのフォルダを指定する
        self._template_dir = os.path.dirname(__file__) + '/../template/' + self._SOURCE_TYPE

    def make(self):
        """
        ソースコードの作成
        :return:
        """
        # 既に作成したフォルダがあれば削除する
        if os.path.isdir(self._parameter_config.output_dir_path):
            shutil.rmtree(self._parameter_config.output_dir_path)

        # 「view」情報が無ければ、エラーメッセージを表示してエラーを返却する。
        if len(self._import_views.views) == 0:
            print('There was no "view" in the loaded document.')
            return

        # Pagesのソースコードを書き出す
        self.__make_pages()

    def __make_pages(self):
        """
        pagesの Viewを作成する
        :return:
        """
        # Viewごとに、pagesファイルを作成する
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # tsxファイルの、テンプレートソースコードを読み込む
            if view.url == '/':
                # URLがインデックスページの場合は、「index.tsx」を元にソースを作成する
                template_file = open(self._template_dir + '/pages/index.tsx', 'r')

                # ファイル名を設定する
                pages_name = 'index'

            else:
                # URLが他のページは、「pages.tsx」を元にソースを作成する
                template_file = open(self._template_dir + '/pages/Pages.tsx', 'r')

                # ファイル名を設定する
                pages_name = self.__get_pages_name(view.url)

            # 保存先のフォルダを作成する
            split_url = view.url.split('/')

            # 書き出し先の「pages」フォルダの、パスを設定する
            output_dirs = self._parameter_config.output_dir_path + '/pages'

            # パスが２階層以上の場合は、階層に合わせたフォルダを作成する
            if len(split_url) > 2:
                # 書き出し先が、２階層以下の場合
                # フォルダにパスパラメータとなるものがあるか、判断してパスを設定する。
                for index in range(len(split_url)-1):
                    path = split_url[index]
                    if path.startswith('_'):
                        path = '[' + path[1:] + ']'

                    output_dirs += '/' + path

                # フォルダの作成
                os.makedirs(output_dirs, exist_ok=True)
                # 書き出しファイルの初期化
                source_file = open(output_dirs + '/' + pages_name + '.tsx', 'w')

            else:
                # 書き出し先が「pages」フォルダの直下
                # フォルダの作成
                os.makedirs(output_dirs, exist_ok=True)
                # 書き出しファイルの初期化
                source_file = open(output_dirs + '/' + pages_name + '.tsx', 'w')

            # テンプレートファイルのソースコードを読み込み
            template_source = template_file.read()

            # ソースコードを設定する
            comment = view.description.replace('\n', '\n * ')
            template_source = template_source.replace('__comment__', comment)

            # バージョンに、現在時刻を設定する
            current_time = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
            template_source = template_source.replace('__version__', current_time)

            # view id を設定する
            view_id = lib.name_case_convert.snake_to_pascal(view.id)
            template_source = template_source.replace('__view_id__', view_id)

            # summary を設定する
            template_source = template_source.replace('__summary__', view.summary)

            # クエリ情報があれば、ソースコードに記述する
            temp_queries = []
            if len(view.path) > 0:
                temp_queries = view.path
            if len(view.query) > 0:
                temp_queries.extend(view.query)

            if len(temp_queries) > 0:
                # 通常のページViewの場合は、routerの箇所を削除する
                template_source = template_source.replace('__router__', '\nimport {useRouter} from \'next/router\';')
                get_path_parameter = '    const router = useRouter();\n'
                get_path_parameter += '    const {' + ", ".join(temp_queries) + '} = router.query;\n\n\n'
                get_path_parameter += '    // Execute processing when Query acquisition is complete.\n'
                get_path_parameter += '    useEffect(() => {\n'
                get_path_parameter += '        if (router.isReady) {\n\n        }\n'
                get_path_parameter += '    }, [router.query, router]);\n'
                template_source = template_source.replace('__get_path_parameters__', get_path_parameter)
            else:
                # 通常のページViewの場合は、routerの箇所を削除する
                template_source = template_source.replace('__router__', '')
                template_source = template_source.replace('__get_path_parameters__', '')

            # tsxファイルの書き出し
            source_file.write(template_source)
            source_file.close()

    @staticmethod
    def __get_pages_name(id_name: str) -> str:
        """
        Pagesのファイル名を返却する
        :return:
        """
        # URLを分割して、最後のパスをファイル名とする
        split_url = id_name.split('/')
        url = split_url[-1]

        # パスの先頭が、パラメータを指定する「_」の場合には、Next.jsのクエリ取得用のファイル名に変更する
        if url.startswith('_'):
            # 先頭の文字列の「_」を削り、前後を「[]」で囲う
            url = '[' + url[1:] + ']'
        return url
