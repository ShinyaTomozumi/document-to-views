#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import library
import sys
import os
from classes import class_laravel


# Main function
if __name__ == '__main__':
    """Main Function
    """

    # Show console log
    print('Start yaml to view files...')

    # パラメータを受け取る
    args = sys.argv

    # 引数の初期化
    input_file_path = ''
    output_file_path = ''
    project_type = ''
    author_name = ''
    copyright_name = ''

    # パラメータの数をチェックする（最低4つは必要)
    if len(args) < 4:
        print('No parameter / 必須パラメータを設定してください。')
        exit()

    # 受け取ったパラメータを引数に設定する。
    i = 0
    for arg in args:
        # 言語タイプを設定する
        if arg == '-t':
            if (i + 1) < len(args):
                project_type = args[i + 1]
        # ファイルのパスを取得する
        if arg == '-i':
            if (i + 1) < len(args):
                input_file_path = args[i + 1]
        # 出力先のパスを取得する
        if arg == '-o':
            if (i + 1) < len(args):
                output_file_path = args[i + 1]
        i += 1

    # ファイルタイプが設定されていない場合はエラーを返却する
    if project_type == '':
        print('Set the language (-t).')
        exit()

    # ファイルのパスが設定されていない場合はエラーを返却する
    if input_file_path == '':
        print('Set the file path (-i).')
        exit()

    # ファイルが存在しない場合はエラーを返却する
    if not os.path.isfile(input_file_path):
        print(f'The specified file does not exist. {input_file_path}')
        exit()

    # ファイルの拡張子が「yaml」もしくは「yml」以外の場合はエラーを返却する
    if not input_file_path.endswith('yaml') and not input_file_path.endswith('yml'):
        print('The specified file is not a "yaml" or "yml" file.')
        exit()

    # プロジェクトタイプによって作成するファイルを変更する
    if project_type == 'laravel':
        # Laravel のViewファイルを作成する
        class_laravel.create_laravel_files(input_file_path, output_file_path)

    print('Finish yaml to views...')
