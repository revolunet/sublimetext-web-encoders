# -*- encoding: UTF-8 -*-

import sublime, sublime_plugin
import base64
import urllib


class WebCodec(object):
    """ Simple naive interface for codecs """
    def encode(self, data):
        return data

    def decode(self, data):
        return data


class UrlCodec(WebCodec):
    """ url encode/decoder """
    def encode(self, data):
        return urllib.quote(data)

    def decode(self, data):
        return urllib.unquote(data)


class Base64Codec(WebCodec):
    """ base64 encode/decoder """
    def encode(self, data):
        return base64.b64encode(data)

    def decode(self, data):
        return base64.b64decode(data)


class HtmlCodec(WebCodec):
    """ html encode/decoder """
    CODES = [
        ['&', '&amp;'],
        ['<', '&lt;'],
        ['>', '&gt;'],
        ['"', '&quot;'],
    ]

    def encode(self, data):
        for from_, to in self.CODES:
            data = data.replace(from_, to)
        return data

    def decode(self, data):
        for from_, to in self.CODES:
            data = data.replace(to, from_)
        return data


WEB_CODECS = {
    'url': UrlCodec(),
    'base64': Base64Codec(),
    'html': HtmlCodec()
}


class WebEncodersCommand(sublime_plugin.TextCommand):
    """ encode/decode selectedtext for the web"""

    def run(self, edit, mode='encode', codec='url'):
        if not codec in WEB_CODECS:
            raise Exception('codec %s not implemented' % codec)
        regions = self.view.sel()
        encoding = self.view.encoding()
        if encoding == 'Undefined':
            encoding = 'UTF-8'
        elif encoding == 'Western (Windows 1252)':
            encoding = 'windows-1252'
        for region in regions:
            data = (self.view.substr(region).encode(encoding))
            replaced = getattr(WEB_CODECS[codec], mode)(data).decode(encoding)
            self.view.replace(edit, region, replaced)
