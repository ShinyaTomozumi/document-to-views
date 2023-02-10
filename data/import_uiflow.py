from typing import List
from data.import_views_base import ImportViewsBase
from models.parameter_config import ParameterConfig
from models.temp_views import TempViews
from models.views import Views
from models.dialog_views import DialogViews
import re


class ImportUIFlow(ImportViewsBase):
    """
    UIFlow 形式で取り込んだViewデータの情報を管理する
    """
    temp_dialog_view_info: DialogViews
    temp_dialog_views: List[DialogViews]
    is_dialogs_read: bool
    is_dialog_desc_read: bool

    def __init__(self, parameter_config: ParameterConfig):
        """
        初期化処理
        :param parameter_config:
        """
        # 基底クラスの初期化
        super().__init__()

        # 各設定の初期化
        is_fast_line = True
        is_description_read = False
        temp_views = TempViews()
        self.temp_dialog_view_info = DialogViews()
        self.temp_dialog_views = []
        self.is_dialogs_read = False
        self.is_dialog_desc_read = False

        # テキストの読み込み
        with open(parameter_config.input_files_path, 'r') as f:
            for line_text in f:
                # 各行に対する処理を行う
                line_text = line_text.strip()

                # Dialog設定中に、特定の文字列以外となった場合は、一時的に保存しているDialog情報を設定する
                if self.is_dialogs_read and not line_text.lower().startswith('- '):
                    self.__set_dialog_views()

                # 読み込んだテキストが、Viewの定義の最初かどうかを判定する
                # 判定方法は「[]」で囲まれた文字列かどうかで判断
                result = re.search(r'\[(.*?)\]', line_text)
                if result:
                    # View の概要の定義の行を読み込んだ処理
                    print('Start view read: ' + result.group(1))

                    # Description状態を解除
                    is_description_read = False

                    # 以前に設定されていたView情報があれば、書き出し時のView情報に追加する。
                    if temp_views.summary != '' and not is_fast_line:
                        # Dialogの設定があれば、情報を追加する。
                        temp_views.dialogs = self.temp_dialog_views

                        # 保存した情報を、書き出し用のViewsに設定する
                        self.__set_self_views(temp_views)

                        # 一時保存のView情報を、初期化する。
                        temp_views = TempViews()
                        self.temp_dialog_view_info = DialogViews()

                    # Viewの概要を設定する
                    temp_views.summary = result.group(1)
                    is_fast_line = False

                else:
                    # 概要以外の情報を読み込んだ場合の処理
                    # 最初の文字列から、それぞれの情報に定義する
                    if line_text.lower().startswith('id:'):
                        # Id の設定
                        temp_views.id = self.__get_parameter_value(line_text)

                        # Description状態を解除
                        is_description_read = False

                    elif line_text.lower().startswith('title:'):
                        # Title の設定
                        temp_views.title = self.__get_parameter_value(line_text)

                        # Description状態を解除
                        is_description_read = False

                    elif line_text.lower().startswith('url:'):
                        # Url の設定
                        temp_views.url = self.__get_parameter_value(line_text)

                        # URLに、パスのパラメータが存在するか確認
                        url_path_params = re.findall("(?<=\{).+?(?=\})", temp_views.url)
                        if len(url_path_params) > 0:
                            # パスパラメータが存在する場合は、一時保存Viewに設定する
                            temp_views.path = url_path_params

                        # Description状態を解除
                        is_description_read = False

                    elif line_text.lower().startswith('desc:') or line_text.lower().startswith('description:'):
                        # Description の設定
                        temp_views.description = self.__get_parameter_value(line_text)

                        # Description状態を設定
                        is_description_read = True

                    elif line_text.lower().startswith('middleware:'):
                        # Middleware の設定
                        # Middleware は、複数設定されることをがあるため、カンマ区切りを配列にする
                        middleware_value = self.__get_parameter_value(line_text)
                        middlewares = middleware_value.split(',')
                        for middleware in middlewares:
                            temp_views.middleware.append(middleware)

                        # Description状態を解除
                        is_description_read = False

                    elif line_text.lower().startswith('query:'):
                        # Query の設定
                        # Query は、複数設定されることをがあるため、カンマ区切りを配列にする
                        query_value = self.__get_parameter_value(line_text)
                        queries = query_value.split(',')
                        for query in queries:
                            temp_views.query.append(query)

                        # Description状態を解除
                        is_description_read = False

                    elif line_text.lower().startswith('dialog:'):
                        # Dialog の設定
                        self.is_dialogs_read = True
                        self.temp_dialog_view_info.summary = self.__get_parameter_value(line_text)

                    elif line_text.lower().startswith('--'):
                        # 区切り文字列となった場合は、全ての状態を解除する
                        is_description_read = False

                    else:
                        # 上記以外は、現在読み込み中の状態によって、処理を変えていく
                        if is_description_read:
                            # Descriptionの読み込み中であれば、一時保存のDescriptionの後ろに文字列を追加する
                            temp_views.description += '\n' + self.__get_parameter_value(line_text)

                        elif self.is_dialogs_read:
                            # Dialogの設定中
                            if line_text.lower().startswith('- id:'):
                                # Dialogの、Idを設定する
                                self.temp_dialog_view_info.id = self.__get_parameter_value(line_text)

                            elif line_text.lower().startswith('- desc:') \
                                    or line_text.lower().startswith('- description:'):
                                # Dialogの、Descriptionを設定する
                                self.temp_dialog_view_info.description = self.__get_parameter_value(line_text)

                                # Dialogの、Description状態をTrueにする
                                self.is_dialog_desc_read = True
                            elif self.is_dialog_desc_read:
                                # ダイアログの、Descriptionを追加する
                                self.temp_dialog_view_info.description += self.__get_parameter_value(line_text)

            # 最後まで読み込んで、一時保存のView情報が存在していた場合は、書き出し用Viewに設定する
            if temp_views.summary != '':
                # Dialogの設定があれば、情報を追加する。
                temp_views.dialogs = self.temp_dialog_views
                self.__set_self_views(temp_views)

    def __set_self_views(self, temp_views: TempViews):
        """
        書き出し用のViewsを設定する
        :param temp_views:
        :return:
        """
        # viewの必須項目が設定されていない場合は、書き出し用のViewに反映しない
        if temp_views.id == '' or temp_views.title == '' or temp_views.description == '':
            return

        # 保存した情報を、書き出し用のViewsに設定する
        view_info = Views()
        view_info.id = temp_views.id
        view_info.summary = temp_views.summary
        view_info.title = temp_views.title
        view_info.url = temp_views.url
        view_info.description = temp_views.description
        self.views.append(view_info)

    def __set_dialog_views(self):
        """
        ダイアログ情報を設定する
        :return:
        """
        # Dialogの、概要が設定されていた場合は追加する。
        if self.temp_dialog_view_info.summary != '' \
                and self.temp_dialog_view_info.id != '' \
                and self.temp_dialog_view_info.description != '':
            # 書き出し用のDialog情報の追加して、一時保存用のDialog情報を初期化する
            self.temp_dialog_views.append(self.temp_dialog_view_info)
            self.temp_dialog_view_info = DialogViews()
            self.is_dialogs_read = False
            self.is_dialog_desc_read = False

    @staticmethod
    def __get_parameter_value(text: str):
        """
        「:」で区切り、後半の文字列を取得する
        :param text:
        :return:
        """
        spl_text = text.split(':')
        if len(spl_text) == 1:
            if ':' in text:
                return ''
            else:
                return text
        else:
            # 後半の文字列は、すべて取得する
            ret_string = ''
            for index in range(1, len(spl_text)):
                ret_string += spl_text[index]
            return ret_string.strip()
