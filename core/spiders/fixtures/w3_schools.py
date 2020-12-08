from core.items import CoreDataItem


def w3_schools():
    url = 'https://www.w3schools.com/html/html_tables.asp'

    with open('core/spiders/fixtures/html_tables.asp', 'rb') as f:
        html = f.read()

    expected_output = [
        CoreDataItem(
            relation=[
                [
                    "Company",
                    "Contact",
                    "Country"
                ],
                [
                    "Alfreds Futterkiste",
                    "Maria Anders",
                    "Germany"
                ],
                [
                    "Centro comercial Moctezuma",
                    "Francisco Chang",
                    "Mexico"
                ],
                [
                    "Ernst Handel",
                    "Roland Mendel",
                    "Austria"
                ],
                [
                    "Island Trading",
                    "Helen Bennett",
                    "UK"
                ],
                [
                    "Laughing Bacchus Winecellars",
                    "Yoshi Tannamuri",
                    "Canada"
                ],
                [
                    "Magazzini Alimentari Riuniti",
                    "Giovanni Rovelli",
                    "Italy"
                ]
            ],
            headers=[
                "Company",
                "Contact",
                "Country",
            ],
            hasHeader=True,
            headerPosition="FIRST_ROW",
            tableNum=1,
            tableType="RELATION",
            termSet=[
                "html",
                "table",
                "td",
                "learn",
                "reference",
                "css",
                "to",
                "0",
                "if",
                "border",
                "document",
                "d",
                "certificate",
                "example",
                "use",
                "xml",
                "1",
                "define",
                "getelementbyid",
                "c",
                "style",
                "cell",
                "var",
                "exercise",
                "tr",
                "color",
                "function",
                "pathname",
                "and",
                "tutorial",
                "x",
                "javascript",
                "php",
                "quiz",
                "be",
                "cc",
                "mypage",
                "degree",
                "txt",
                "tag",
                "display",
                "th",
                "attribute",
                "try",
                "width",
                "span",
                "substr",
                "xhttp",
                "b",
                "web",
                "sql",
                "python",
                "bootstrap",
                "element",
                "googletag",
                "add",
                "property",
                "window",
                "w3",
                "jquery",
                "list",
                "caption",
                "top",
                "pos",
                "txt2",
                "359",
                "log",
                "div",
                "foldername",
                "mp",
                "java",
                "row",
                "100",
                "collapse",
                "99",
                "stroke",
                "setattribute",
                "logindrawcircle",
                "26",
                "35",
                "24",
                "more",
                "svg",
                "4",
                "background",
                "form",
                "gpt",
                "ad",
                "column",
                "text",
                "align",
                "one",
                "content",
                "none",
                "y",
                "typ",
                "rect",
                "w3school",
                "examples",
                "cmd"
            ],
            title="",
            pageTitle="HTML Tables",
            url=url,
            timestamp="FAKE",
            markup="<table id=\"customers\">\r\n  <tr>\r\n    <th>Company</th>\r\n    <th>Contact</th>\r\n    <th>Country</th>\r\n  </tr>\r\n  <tr>\r\n    <td>Alfreds Futterkiste</td>\r\n    <td>Maria Anders</td>\r\n    <td>Germany</td>\r\n  </tr>\r\n  <tr>\r\n    <td>Centro comercial Moctezuma</td>\r\n    <td>Francisco Chang</td>\r\n    <td>Mexico</td>\r\n  </tr>\r\n  <tr>\r\n    <td>Ernst Handel</td>\r\n    <td>Roland Mendel</td>\r\n    <td>Austria</td>\r\n  </tr>\r\n  <tr>\r\n    <td>Island Trading</td>\r\n    <td>Helen Bennett</td>\r\n    <td>UK</td>\r\n  </tr>\r\n  <tr>\r\n    <td>Laughing Bacchus Winecellars</td>\r\n    <td>Yoshi Tannamuri</td>\r\n    <td>Canada</td>\r\n  </tr>\r\n  <tr>\r\n    <td>Magazzini Alimentari Riuniti</td>\r\n    <td>Giovanni Rovelli</td>\r\n    <td>Italy</td>\r\n  </tr>\r\n</table>",
            textBeforeTable="",
            textAfterTable="",
            s3Link="",
            recordOffset=0,
            recordEndOffset=0,
            language="en",
            nbColumns=3,
            nbRows=7,
            tableOrientation="VERTICAL",
        ),
        CoreDataItem(
            relation=[
                [
                    "Tag",
                    "Description"
                ],
                [
                    "<table>",
                    "Defines a table"
                ],
                [
                    "<th>",
                    "Defines a header cell in a table"
                ],
                [
                    "<tr>",
                    "Defines a row in a table"
                ],
                [
                    "<td>",
                    "Defines a cell in a table"
                ],
                [
                    "<caption>",
                    "Defines a table caption"
                ],
                [
                    "<colgroup>",
                    "Specifies a group of one or more columns in a table for formatting"
                ],
                [
                    "<col>",
                    "Specifies column properties for each column within a <colgroup> element"
                ],
                [
                    "<thead>",
                    "Groups the header content in a table"
                ],
                [
                    "<tbody>",
                    "Groups the body content in a table"
                ],
                [
                    "<tfoot>",
                    "Groups the footer content in a table"
                ]
            ],
            headers=[
                "Tag",
                "Description",
            ],
            hasHeader=True,
            headerPosition="FIRST_ROW",
            tableNum=2,
            tableType="RELATION",
            termSet=[
                "html",
                "table",
                "td",
                "learn",
                "reference",
                "css",
                "to",
                "0",
                "if",
                "border",
                "document",
                "d",
                "certificate",
                "example",
                "use",
                "xml",
                "1",
                "define",
                "getelementbyid",
                "c",
                "style",
                "cell",
                "var",
                "exercise",
                "tr",
                "color",
                "function",
                "pathname",
                "and",
                "tutorial",
                "x",
                "javascript",
                "php",
                "quiz",
                "be",
                "cc",
                "mypage",
                "degree",
                "txt",
                "tag",
                "display",
                "th",
                "attribute",
                "try",
                "width",
                "span",
                "substr",
                "xhttp",
                "b",
                "web",
                "sql",
                "python",
                "bootstrap",
                "element",
                "googletag",
                "add",
                "property",
                "window",
                "w3",
                "jquery",
                "list",
                "caption",
                "top",
                "pos",
                "txt2",
                "359",
                "log",
                "div",
                "foldername",
                "mp",
                "java",
                "row",
                "100",
                "collapse",
                "99",
                "stroke",
                "setattribute",
                "logindrawcircle",
                "26",
                "35",
                "24",
                "more",
                "svg",
                "4",
                "background",
                "form",
                "gpt",
                "ad",
                "column",
                "text",
                "align",
                "one",
                "content",
                "none",
                "y",
                "typ",
                "rect",
                "w3school",
                "examples",
                "cmd"
            ],
            title="",
            pageTitle="HTML Tables",
            url=url,
            timestamp="FAKE",
            markup="<table class=\"w3-table-all notranslate\">\r\n<tr>\r\n<th>Tag</th>\r\n<th>Description</th>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_table.asp\">&lt;table&gt;</a></td>\r\n<td>Defines a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_th.asp\">&lt;th&gt;</a></td>\r\n<td>Defines a header cell in a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_tr.asp\">&lt;tr&gt;</a></td>\r\n<td>Defines a row in a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_td.asp\">&lt;td&gt;</a></td>\r\n<td>Defines a cell in a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_caption.asp\">&lt;caption&gt;</a></td>\r\n<td>Defines a table caption</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_colgroup.asp\">&lt;colgroup&gt;</a></td>\r\n<td>Specifies a group of one or more columns in a table for formatting</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_col.asp\">&lt;col&gt;</a></td>\r\n<td>Specifies column properties for each column within a &lt;colgroup&gt; element</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_thead.asp\">&lt;thead&gt;</a></td>\r\n<td>Groups the header content in a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_tbody.asp\">&lt;tbody&gt;</a></td>\r\n<td>Groups the body content in a table</td>\r\n</tr>\r\n<tr>\r\n<td><a href=\"/tags/tag_tfoot.asp\">&lt;tfoot&gt;</a></td>\r\n<td>Groups the footer content in a table</td>\r\n</tr>\r\n</table>",
            textBeforeTable="HTML Table Tags",
            textAfterTable="For a complete list of all available HTML tags, visit our HTML Tag Reference.",
            s3Link="",
            recordOffset=0,
            recordEndOffset=0,
            language="en",
            nbColumns=2,
            nbRows=11,
            tableOrientation="VERTICAL",
        ),
    ]

    return (url, html, expected_output)
