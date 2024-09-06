import mistletoe
from mistletoe.block_token import BlockToken, Heading, Paragraph, SetextHeading, HtmlBlock
from mistletoe.markdown_renderer import MarkdownRenderer
from mistletoe.span_token import InlineCode, RawText, SpanToken
from TrayAlertTableRow import TrayAlertTableRow
from bs4 import BeautifulSoup
import parser


# html_doc = """<html><head><title>Test</title></head>
#               <body><h1>Header</h1><p>This is a paragraph.</p></body></html>"""
#
# soup = BeautifulSoup(html_doc, 'html.parser')
#
#
#
# print("Title:", title)
# print("Header:", header)
# print("Paragraph:", paragraph)
def update_text(token: SpanToken, content):
    """Update the text contents of a span token and its children.
    `InlineCode` tokens are left unchanged."""
    if isinstance(token, RawText):
        content.append(token.content)
        # soup = BeautifulSoup(token.content, 'html.parser')
        # title = soup.title.string


# header = soup.h1.string
#         if soup.p
#         print(soup.title)
# token.content = token.content.replace("mistletoe", "The Amazing mistletoe")

# if not isinstance(token, InlineCode) and hasattr(token, "children"):
#     for child in token.children:
#         update_text(child)


def update_block(token: BlockToken, content):
    """Update the text contents of paragraphs and headings within this block,
    and recursively within its children."""
    # print(token.children)
    if isinstance(token, (HtmlBlock)):
        for child in token.children:
            update_text(child, content)

    for child in token.children:
        if isinstance(child, BlockToken):
            update_block(child, content)


def find_existed_row_in_alerts(existed_alerts, new_alert):
    for alert in existed_alerts:
        id_ = new_alert['solution_instance_id']
        # print(f'{alert.solution_instance_id} == {id_}')
        if alert.solution_instance_id == new_alert['solution_instance_id'] \
                and alert.workflow == new_alert['workflow_title']:
            return alert
    return None


def method_name():
    alerts = parser.get_ites()
    print(len(alerts))
    count = 0
    for alert in alerts:
        existed_row = find_existed_row_in_alerts(existed_alerts, alert)
        if existed_row is None:
            count += 1
            print(alert)
    print(count)


def normalize_string(string):
    return string.strip().replace('\n', '')


with open("content.md", "r") as fin:
    with MarkdownRenderer() as renderer:
        document = mistletoe.Document(fin)
        # print(document.children.children)
        content = []
        update_block(document, content)
        html_content = "".join(content)
        # print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table')
        trs = table.find_all('tr')
        trs_ = trs[1:]
        element = 61
        # print(trs_[element])
        existed_alerts = []
        for tr in trs_:
            find_all = tr.find_all('td')
            row = TrayAlertTableRow(**{'workflow': normalize_string(find_all[0].text),
                                       'message': normalize_string(find_all[1].text),
                                       'solution_instance_id': find_all[2].text.strip(), 'customer': find_all[4],
                                       'reason': normalize_string(find_all[3].text),
                                       'action_item': find_all[5]})
            existed_alerts.append(row)
            # print(row.message)

        method_name()
