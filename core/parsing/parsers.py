from typing import Dict
from datetime import datetime
from abc import ABC, abstractmethod
from core.parsing import utils
from core.items import CoreTableItem
from core.parsing.exceptions import InvalidTableException


class TableParser(ABC):
    '''
    Abstract base class that should be defined for different types of tables that require parsing.

    See core.parsing.utils.get_parser_from_url
    '''
    @classmethod
    @abstractmethod
    def normalize_table(cls, table) -> Dict:
        raise Exception(
            f'{cls.__class__.__name__}.normalize_table is not defined')

    @classmethod
    def get_tables(cls, response):
        return response.css('table')

    @classmethod
    def parse_table(cls, table, **meta) -> CoreTableItem:
        try:
            return CoreTableItem(
                table=cls.normalize_table(table),
                timestamp=datetime.now().isoformat(),
                **meta
            )
        except InvalidTableException:
            # TODO: keep track of how often this happens
            pass


class WikitableParser(TableParser):
    __TABLE_CLASS = "wikitable"

    @classmethod
    def normalize_table(cls, table):
        all_rows = table.css('tr')
        headers_per_row = map(lambda x: x.css('th').getall(), all_rows)
        header_values, header_index = cls.__find_header_row(headers_per_row)

        header_values = list(
            map(utils.parse_inner_text_from_html, header_values))
        rows_after_headers = all_rows[header_index+1:]
        rows_with_cleaned_cells = [map(utils.parse_inner_text_from_html, row.css(
            'td').extract()) for row in rows_after_headers if row != '']

        if len(rows_with_cleaned_cells) < 2 or len(header_values) < 2:
            raise InvalidTableException()

        return utils.compose_normalized_table(
            header_values, rows_with_cleaned_cells)

    @classmethod
    def __find_header_row(cls, rows):
        header_values, header_index = None, -1
        for index, headers in enumerate(rows):
            if len(headers) != 0:
                header_values = headers
                header_index = index
        if header_values is None:
            raise InvalidTableException('No headers found on wikitable')

        return header_values, header_index

    @classmethod
    def get_tables(cls, response):
        return response.css(f'table.{WikitableParser.__TABLE_CLASS}')


class WellFormattedTableParser(TableParser):
    @classmethod
    def normalize_table(cls, table):
        header_columns = table.css('tr th')
        header_values = list(
            map(utils.parse_inner_text_from_html, header_columns.getall()))
        body_rows = [
            [utils.parse_inner_text_from_html(x)
             for x in row.css('td').getall()]
            for row in table.css('tr')
        ]
        return utils.compose_normalized_table(header_values, body_rows)
