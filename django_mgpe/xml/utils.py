#coding:utf8
from django.utils.html import strip_tags
from pytils import translit
from xml.sax.saxutils import XMLGenerator
import StringIO
import xml.dom.minidom


def prepare_comment(comment):
    comment = unicode(strip_tags(comment))
    comment = translit.translify(comment)
    return comment


def get_check_result_as_xml(status, comment=None):
    out = StringIO.StringIO("")
    g = XMLGenerator(out, encoding='UTF-8')
    g.startDocument()
    g.startElement("response", {})
    g.startElement("result", {})
    g.characters(status)
    g.endElement("result")
    if comment:
        g.startElement("comment", {})
        g.characters(comment)
        g.endElement("comment")
    g.endElement("response")
    g.endDocument()
    return out.getvalue()


def get_update_result_as_xml(status, txn_id, prv_txn, sum, comment=None):
    out = StringIO.StringIO("")
    g = XMLGenerator(out, encoding='UTF-8')
    g.startDocument()
    g.startElement("response", {})
    g.startElement("mgpe_txn_id", {})
    g.characters(txn_id)
    g.endElement("mgpe_txn_id")
    g.startElement("txn_id", {})
    g.characters(txn_id)
    g.endElement("txn_id")
    g.startElement("prv_txn", {})
    g.characters(prv_txn)
    g.endElement("prv_txn")
    g.startElement("sum", {})
    g.characters(sum)
    g.endElement("sum")
    g.startElement("result", {})
    g.characters(status)
    g.endElement("result")
    if comment:
        g.startElement("comment", {})
        g.characters(comment)
        g.endElement("comment")
    g.endElement("response")
    g.endDocument()
    return out.getvalue()


def get_status_from_xml(text):
    dom = xml.dom.minidom.parseString(text)
    dom.normalize()
    responseNode = dom.getElementsByTagName("response")[0]
    statusNode = responseNode.getElementsByTagName("result")[0]
    textNode = statusNode.childNodes[0]
    status = textNode.nodeValue
    return status

