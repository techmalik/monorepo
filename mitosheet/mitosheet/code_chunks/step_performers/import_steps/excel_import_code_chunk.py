#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.

from typing import List

from mitosheet.code_chunks.code_chunk import CodeChunk


class ExcelImportCodeChunk(CodeChunk):

    def transpile(self) -> List[str]:
        file_name = self.get_param('file_name')
        sheet_names = self.get_param('sheet_names')
        has_headers = self.get_param('has_headers')
        skiprows = self.get_param('skiprows')

        read_excel_params = {
            'sheet_name': sheet_names,
            'skiprows': skiprows
        }

        # Get rid of the headers if it doesn't have them
        if not has_headers:
            read_excel_params['header'] = None

        read_excel_line = f'sheet_df_dictonary = pd.read_excel(\'{file_name}\', engine=\'openpyxl\''
        for key, value in read_excel_params.items():
            read_excel_line += f', {key}={value}'
        read_excel_line += ')'

        df_definitions = []
        for index, sheet_name in enumerate(sheet_names):
            adjusted_index = len(self.post_state.df_names) - len(sheet_names) + index
            df_definitions.append(
                f'{self.post_state.df_names[adjusted_index]} = sheet_df_dictonary[\'{sheet_name}\']'
            )

        return [
            'import pandas as pd',
            read_excel_line
        ] + df_definitions
