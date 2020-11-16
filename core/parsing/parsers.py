from abc import ABC, abstractmethod
from typing import Dict, List

from core.parsing import utils
from core.items import CoreTableItem
from core.parsing.exceptions import InvalidTableException


class TableParser(ABC):
    """
    Abstract base class that should be defined for different types of tables that require parsing.

    See core.parsing.utils.get_parser_from_url
    """

    @classmethod
    @abstractmethod
    def normalize_table(cls, table) -> Dict:
        raise Exception(
            f'{cls.__class__.__name__}.normalize_table is not defined')

    @classmethod
    def get_table_title(cls, table) -> str:
        return table.css('caption').get()

    @classmethod
    def get_tables(cls, response):
        tables = response.css('table')
        for t in tables:
            # remove tables inside forms
            # how TODO with scrapy selectors?

            # skip over tables with subtables
            if t.css('table table'):
                continue

            yield t

    @classmethod
    @abstractmethod
    def parse_table(cls, table) -> CoreTableItem:
        raise Exception(
            f'{cls.__class__.__name__}.parse_table is not defined')


class WikitableParser(TableParser):
    __TABLE_CLASS = "wikitable"

    @classmethod
    def normalize_table(cls, table):
        all_rows = table.css('tr')
        header_values, header_index = cls.__find_header_row(all_rows)
        if header_index != 0:
            raise InvalidTableException('Only header in first row supported')

        header_values = list(
            map(utils.parse_inner_text_from_html, header_values))
        rows_with_cleaned_cells = [map(utils.parse_inner_text_from_html, row.css(
            'td').extract()) for row in all_rows if row != '']

        if len(rows_with_cleaned_cells) < 2 or len(header_values) < 2:
            raise InvalidTableException()

        # return utils.compose_normalized_table(
        #     header_values, rows_with_cleaned_cells)
        return rows_with_cleaned_cells

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

    @classmethod
    def parse_table(cls, table) -> CoreTableItem:
        try:
            header_values, _ = cls.__find_header_row(table)
            return CoreTableItem(
                table=cls.normalize_table(table),
                title=cls.get_table_title(table),
                markup=table.get(),
                header_position="FIRST_ROW", # TODO: hardcoded
                headers=header_values,
                table_type="relation", # TODO: hardcoded
            )
        except InvalidTableException:
            # TODO: keep track of how often this happens
            pass


class WellFormattedTableParser(TableParser):
    @classmethod
    def normalize_table(cls, table):
	# eliminate tables with "rowspan" or "colspan"
        if table.css('td[colspan]').getall() \
           or table.css('th[colspan]').getall() \
           or table.css('td[rowspan]').getall() \
           or table.css('td[rowspan]').getall():
            raise InvalidTableException('Tables with colspan / rowspan not supported')

        # extract header
        header_values = cls.__get_headers_values(table)
        if not header_values:
            # tables without headers are almost useless for automated processing,
            # just drop them here
            raise InvalidTableException('No headers found in table')

        # extract body
        body_rows = [
            [utils.parse_inner_text_from_html(x)
             for x in row.css('td').getall()]
            for row in table.css('tr')
        ]

        # combine header and body into one relation
        relation = [header_values] + body_rows
        # basic sanity check for body, will raise on error
        utils.validate_body_cell_layout(relation)

        # return utils.compose_normalized_table(header_values, body_rows)
        return relation

    @classmethod
    def __get_headers_values(cls, table) -> List[str]:
        header_columns = table.css('tr th')
        header_values = list(
            map(utils.parse_inner_text_from_html, header_columns.getall()))
        return header_values

    @classmethod
    def parse_table(cls, table) -> CoreTableItem:
        try:
            return CoreTableItem(
                table=cls.normalize_table(table),
                title=cls.get_table_title(table),
                markup=table.get(),
                header_position="FIRST_ROW", # TODO: hardcoded
                table_type="relation", # TODO: hardcoded
                headers=cls.__get_headers_values(table),
            )
        except InvalidTableException:
            # TODO: keep track of how often this happens
            pass
