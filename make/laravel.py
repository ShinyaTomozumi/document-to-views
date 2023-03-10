import re
import os
import datetime
import shutil

from models.parameter_config import ParameterConfig
from data.import_views_base import ImportViewsBase


class Laravel:
    """
    Laravelのソース作成クラス
    """
    _parameter_config: ParameterConfig
    _import_views: ImportViewsBase
    _template_dir: str
    _SOURCE_TYPE = 'laravel'

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

        # Controllerファイルの作成
        self.__make_controller()

        # routeファイルの作成
        self.__make_route()

        # bladeファイルの作成
        self.__make_blade()

        # TypeScriptファイルの作成
        self.__make_type_script()

        # SCSSファイルの作成
        self.__make_scss()

    def __make_controller(self):
        """
        Controllerファイルの作成
        :return:
        """
        # ViewごとにControllerファイルを作成する
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # ファイル名を設定する
            controller_name = self.__get_controller_name(view.id)

            # 保存先のフォルダを作成する
            output_dirs = self._parameter_config.output_dir_path + '/app/Http/Controllers'
            os.makedirs(output_dirs, exist_ok=True)

            # ViewControllers.phpファイルの初期化
            source_file = open(output_dirs + '/' + controller_name + '.php', 'w')

            # Controllerのテンプレートソースコードを読み込む
            template_file = open(self._template_dir + '/php/ViewController.php', 'r')
            template_source = template_file.read()

            # ソースコードを設定する
            comment = view.description.replace('\n', '\n * ')
            template_source = template_source.replace('__comment__', comment)

            # バージョンに現在時刻を設定する
            current_time = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
            template_source = template_source.replace('__version__', current_time)

            # Controller名を設定する
            template_source = template_source.replace('__controller_name__', controller_name)

            # view id を設定する
            template_source = template_source.replace('__view_id__', view.id.upper())

            # bladeファイル名を設定する
            template_source = template_source.replace('__blade_name__', view.id)

            # copyrightを設定する
            if self._import_views.copyright == '':
                template_source = template_source.replace('__copyright__', '')
            else:
                template_source = template_source.replace('__copyright__', '\n * @copyright ' + self._import_views.copyright)

            # authorを設定する
            if self._import_views.author == '':
                template_source = template_source.replace('__author__', '')
            else:
                template_source = template_source.replace('__author__', '\n * @author ' + self._import_views.author)

            # パラメータを設定する
            if len(view.path) > 0:
                str_parameter = ''
                controller_comments = ''
                # パスの設定に必要な文字列を作成する
                for params in view.path:
                    str_parameter += ', string $' + params
                    controller_comments += '\n     * @param string $' + params

                # パラメータを設定する
                template_source = template_source.replace('__paths__', str_parameter)
                template_source = template_source.replace('__comment_params__', controller_comments)
            else:
                # パラメータが存在しない場合はテンプレートの文字列を消去する
                template_source = template_source.replace('__paths__', '')
                template_source = template_source.replace('__comment_params__', '')

            # ViewControllers.phpファイルにソースコードを書き込む
            source_file.write(template_source)
            source_file.close()

    def __make_route(self):
        """
        route.phpファイルの作成
        :return:
        """
        # 保存先のフォルダを作成する
        output_dirs = self._parameter_config.output_dir_path + '/routes'
        os.makedirs(output_dirs, exist_ok=True)

        # routeファイルを書き込みモードで初期化
        source_file = open(output_dirs + '/web.php', 'w')

        # routeのテンプレートソースコードを読み込む
        controller_file = open(self._template_dir + '/php/routes.php', 'r')
        template_source = controller_file.read()

        # 製作者、及びコピーライトを設定
        author_name = ''
        copyright_name = ''
        if self._import_views.copyright != '':
            copyright_name = '\n * @copyright ' + self._import_views.copyright
        if self._import_views.author != '':
            author_name = '\n * @author ' + self._import_views.author

        # ソースコードを作成する
        current_time = datetime.datetime.now().strftime('%Y_%m_%d_%H%M%S')
        template_source = template_source.replace('__copyright__', copyright_name)
        template_source = template_source.replace('__author__', author_name)
        template_source = template_source.replace('__version__', current_time)

        # 各Viewごとの、「route.php」ファイルのソースコードを作成する
        route_path_source = ''
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # ソースコードを作成する
            controller_name = self.__get_controller_name(view.id)
            view_id = view.id.upper()
            comment = view.description.replace('\n', '\n * ')

            # URLは、UiFlowで記述した場合に、先頭が「_」で定義された場合はパラメータ受け取り用に変換する
            url = ''
            split_url = view.url.split('/')
            for i in range(1, len(split_url)):
                urls = split_url[i]
                if urls.startswith('_'):
                    urls = '{' + urls[1:] + '}'
                url += '/' + urls

            # 書き込むURLを、定義する
            route_path_source += '/**\n' \
                                 ' * GET Views\n' \
                                 ' * {}\n' \
                                 ' * ViewID: {}\n' \
                                 ' */\n'.format(comment, view_id)
            # Middlewareが設定されているかどうかで、ソースコードを切り分ける
            if len(view.middleware) > 0:
                middlewares = ','.join(view.middleware)
                middlewares = '\'' + middlewares.replace(',', '\',\'') + '\''
                route_path_source += 'Route::GET(\'{}\', [\n' \
                                     '    \'middleware\' => [{}],\n' \
                                     '    \'uses\' => \'App\\Http\\Controllers\\{}@view\'\n' \
                                     ']);\n\n'.format(url, middlewares, controller_name)
            else:
                route_path_source += 'Route::GET(\'{}\', \'App\\Http\\Controllers\\{}@view\');' \
                                     '\n\n'.format(url, controller_name)

        # ソースコードの作成
        template_source = template_source.replace('__source_code__', route_path_source)

        # 「route.php」ファイルに、ソースコードを書き込む
        source_file.write(template_source)
        source_file.close()

    def __make_blade(self):
        """
        「blade.php」ファイルを作成する
        :return:
        """
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # bladeファイルの、ファイル名を設定する
            blade_file_name = view.id + '.blade'

            # bladeファイルの、保存先のフォルダを作成する
            output_dirs = self._parameter_config.output_dir_path + '/resources/views'
            os.makedirs(output_dirs, exist_ok=True)

            # 「blade.php」ファイルの初期化
            source_file = open(output_dirs + '/' + blade_file_name + '.php', 'w')

            # bladeファイルの、テンプレートソースコードを読み込む
            blade_file = open(self._template_dir + '/php/Blade.php', 'r')
            template_source = blade_file.read()

            # ソースコードを設定する
            comment = view.description.replace('\n', '\n * ')
            template_source = template_source.replace('__comment__', comment)

            # copyrightを設定する
            if self._import_views.copyright == '':
                template_source = template_source.replace('__copyright__', '')
            else:
                template_source = template_source.replace('__copyright__', '\n * @copyright ' + self._import_views.copyright)

            # authorを設定する
            if self._import_views.author == '':
                template_source = template_source.replace('__author__', '')
            else:
                template_source = template_source.replace('__author__', '\n * @author ' + self._import_views.author)

            # viewのID を設定する
            template_source = template_source.replace('__view_id__', view.id.upper())

            # タイトル を設定する
            template_source = template_source.replace('__title__', view.title)

            # 「blade.php」ファイルを、ソースコードを書き込む
            source_file.write(template_source)
            source_file.close()

    def __make_type_script(self):
        """
        TypeScriptファイルの、ソースコードテンプレート作成する
        :return:
        """
        # 保存先のフォルダを作成する
        output_dirs = self._parameter_config.output_dir_path + '/resources/ts'
        os.makedirs(output_dirs, exist_ok=True)

        # Viewsファイルの保存先のフォルダを作成する
        output_dirs_views = output_dirs + '/view'
        os.makedirs(output_dirs_views, exist_ok=True)

        # app.tsファイルを作成する
        source_file = open(output_dirs + '/app.ts', 'w')

        # TypeScriptのappファイルのテンプレートソースコードを読み込む
        ts_app_template = open(self._template_dir + '/ts/app.ts', 'r')
        app_template_source = ts_app_template.read()

        # app.tsに書き出すRequireファイルとDefaultのコード
        source_imports = ''
        source_default = ''

        # viewごとのtsファイルを作成する
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # ファイル名を設定する
            ts_view_file_name = view.id.lower()

            # viewごとのTsファイルを作成する
            source_file_views = open(output_dirs_views + '/' + ts_view_file_name + '.ts', 'w')

            # TS viewファイルのテンプレートソースコードを読み込む
            template_file = open(self._template_dir + '/ts/view.ts', 'r')
            template_source = template_file.read()

            # ソースコードを設定する
            comment = view.description.replace('\n', '\n * ')
            template_source = template_source.replace('__comment__', comment)

            # view id を設定する
            template_source = template_source.replace('__view_id__', view.id.upper())

            # タイトルを設定する
            template_source = template_source.replace('__title__', view.title)

            # app.tsに記載するソースコードを設定する
            camel_name = re.sub("_(.)", lambda x: x.group(1).upper(), view.id.capitalize())
            source_imports += 'const view{} = require(\'./view/{}\');\n'.format(camel_name, view.id)
            source_default += '\n    if (document.getElementById(\'{}\') != null) {{\n' \
                              '        view{}.default();\n' \
                              '    }}\n'.format(view.id.upper(), camel_name)

            # blade.phpファイルにソースコードを書き込む
            source_file_views.write(template_source)
            source_file_views.close()

        # viewごとのrequireを定義を書き込む
        app_template_source = app_template_source.replace('__require__', source_imports)

        # view ごとのDefaultの定義を書き込む
        app_template_source = app_template_source.replace('__view_default__', source_default)

        # app.tsファイルにソースコードを書き込む
        source_file.write(app_template_source)
        source_file.close()

    def __make_scss(self):
        """
        SCSSファイルを作成する
        :return:
        """
        # 保存先のフォルダを作成する
        output_dirs = self._parameter_config.output_dir_path + '/resources/scss'
        os.makedirs(output_dirs, exist_ok=True)

        # Viewsファイルの保存先のフォルダを作成する
        output_dirs_views = output_dirs + '/view'
        os.makedirs(output_dirs_views, exist_ok=True)

        # app.scssファイルを作成する
        source_file = open(output_dirs + '/app.scss', 'w')

        # SCSSのappファイルのテンプレートソースコードを読み込む
        scss_app_template = open(self._template_dir + '/scss/app.scss', 'r')
        app_template_source = scss_app_template.read()

        # app.scssに書き出すImportコード
        source_views = ''

        # viewごとのscssファイルを作成する
        for view in self._import_views.views:
            # URLが設定されていない場合は、次の処理を行う
            if view.url == '':
                continue

            # ファイル名を設定する
            view_file_name = view.id.lower()

            # viewごとのscssファイルを作成する
            source_file_views = open(output_dirs_views + '/_' + view_file_name + '.scss', 'w')

            # scss viewファイルのテンプレートソースコードを読み込む
            template_file = open(self._template_dir + '/scss/view.scss', 'r')
            template_source = template_file.read()

            # view id を設定する
            template_source = template_source.replace('__view_id__', view.id.upper())

            # コメントを設定する
            comment = view.description.replace('\n', '\n /// ')
            template_source = template_source.replace('__comment__', comment)

            # app.scssに記載するソースコードを設定する
            source_views += '@import "view/{}";\n'.format(view.id.lower())

            # blade.phpファイルにソースコードを書き込む
            source_file_views.write(template_source)
            source_file_views.close()

        # importのソースコードを書き込む
        app_template_source = app_template_source.replace('__import__', source_views)

        # app.tsファイルにソースコードを書き込む
        source_file.write(app_template_source)
        source_file.close()

    @staticmethod
    def __get_controller_name(id_name: str) -> str:
        """
        Controller名を取得する
        :return:
        """
        camel_name = re.sub("_(.)", lambda x: x.group(1).upper(), id_name.capitalize())
        return 'View' + camel_name + 'Controller'
