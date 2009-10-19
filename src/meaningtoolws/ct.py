# -*- coding: utf-8 -*-

# Copyright (c) 2009, Popego Corporation <contact [at] meaningtool [dot] com>
# All rights reserved.
#
# This file is part of the Meaningtool Web Services Python Client project
#
# See the COPYING file distributed with this project for its licensing terms.

"""
Meaningtool Category Tree REST API v0.1 client

Official documentation for the REST API v0.1 can be found at
http://www.meaningtool.com/developers/docs/api/rest/v0.1
"""

import re
import urllib
import urllib2

try:
    import json
except ImportError:
    import simplejson as json

from scoring_exceptions import BaseMeaningtoolError, InvalidParameter, InvalidUrl


MT_BASE_URL = u"http://ws.meaningtool.com/0.1"

_re_url = re.compile(ur"^https?://.+$")


class Result(object):
    """ Represents the response of meaningtool.
    """

    def __init__(self, status_errcode, status_message, data):
        """ Creates the result.
        The `data` will change takeing into account the additionals
        parameters when called to the API.

        :parameters:
            status_errcode: str
                the status of the response.
            status_message: str
                the message of the response.
            data: dict()
                the data of the response.
        """
        super(Result, self).__init__()
        self.status_errcode = status_errcode
        self.status_message = status_message
        self.data = data

    def __repr__(self):
        return u"<%s - %s>" % (self.__class__.__name__, self.status_message)


class Client(object):
    """ Interface to use the Meaningtool API.
    """

    # Has the posibles codes that the call to the api may return.
    POSIBLE_HTTP_CODES = [400, 401, 403, 404, 409, 500]

    def __init__(self, api_key, tree_key, base_url=MT_BASE_URL):
        """ Creates the client:

        :parameters:
            api_key: str
                the api key of the user.
            tree_key: str
                the tree key of the category tree to use.
            base_url: str
                the url to use.
        """
        self.api_key = api_key
        self.tree_key = tree_key
        self._base_url = u"%s/%s" % (base_url, tree_key)
        
    def __repr__(self):
        return u"<%s - tree_key: %s>" % (self.__class__.__name__, self.tree_key)

    def _req_base(self, method, url, data, headers):
        if method == "GET":
            req = urllib2.Request(u"%s?%s" % (url, urllib.urlencode(data)))
        elif method == "POST":
            req = urllib2.Request(url, urllib.urlencode(data))
        else:
            raise ValueError(u"HTTP Method '%s' not supported" % method)

        req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
        req.add_header("Accept-Charset", "UTF-8")
        for k,v in headers:
            req.add_header(k, v)


            
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            if e.code not in self.POSIBLE_HTTP_CODES:
                raise BaseMeaningtoolError("There was an error while getting the data.")
            resp = e
        s = resp.read()
        return s

    def _req_json(self, method, url, data, headers):
        url += u'.json'
        headers.append(("Accept", "application/json"))
        return self._req_base(method, url, data, headers)

    def _parse_result_base(self, result_dict):
        status = result_dict["status"]
        status_errcode = result_dict["errcode"]
        status_message = result_dict["message"]
        data = result_dict["data"]
        if status == "ok":
            return Result(status_errcode, status_message, data)
        else:
            raise BaseMeaningtoolError.from_code(status_errcode)

    def _parse_result_json(self, raw):
        if raw == 'bad api key':    ## XXX: Workaround. The Invalid API key error response doesn't return a valid json response.
            raw = '{"status": "error", "message": "Invalid API key", "data": {}, "errcode": "UserKeyInvalid"}'
        return self._parse_result_base(json.loads(raw, encoding="utf8"))

    # default request/parse methods
    _req = _req_json
    _parse_result = _parse_result_json

    def get_categories(self, source, input, url_hint=None, additionals=None, content_language=None):
        """ Gets the categories for the input.

        :parameters:
            source: str
                the specified source (text, url, html)
            input: str
                the data or url to categorize.
            url_hint: str
                used when the source is text or html, and is the url
                from where the `input` was taken.
            additionals: list(str)
                a list with the additionals keys (top-terms, classifiers, 
                classifiers-top-terms)
            content_language: str
                the language of the input.

        :returns:
            a `Result` whose "data" is the dictionary of the json response.

        :exceptions:
            `ResponseError`: if there is an error while categorizing the text.
            `UnknownExceptionCodeError`: if the response had an error but it
                doesn't has a kwown code.
            `MeaningtoolError`: if there is any kind of problem while 
                getting the conection to meaningtool.
        """
        self._validate_parameters(source, input, url_hint, additionals, content_language)

        url = u"%s/categories" % self._base_url
        data = {}
        headers = []

        data["source"] = source.encode("utf8")
        data["input"] = input.encode("utf8")
        data["api_key"] = self.api_key            

        if url_hint:
            data["url_hint"] = url_hint.encode("utf8")

        if additionals:
            additionals = u",".join(set(additionals))
            data["additionals"] = additionals.encode("utf8")

        if content_language:
            content_language = content_language[:2].lower()
            headers.append(("Content-Language", content_language.encode("ascii")))

        # Even if POST, it's idempotent as GET.
        return self._parse_result(self._req("GET", url, data, headers))

    def get_tags(self, source, input, url_hint=None, content_language=None):
        """ Gets the categories for the input.

        :parameters:
            source: str
                the specified source (text, url, html)
            input: str
                the data or url to categorize.
            url_hint: str
                used when the source is text or html, and is the url
                from where the `input` was taken.
            content_language: str
                the language of the input (it should be a 2 char value: en,
                    es, pt...)

        :returns:
            a `Result` whose "data" is the dictionary of the json response.

        :exceptions:
            `ResponseError`: if there is an error while categorizing the text.
            `UnknownExceptionCodeError`: if the response had an error but it
                doesn't has a kwown code.
            `MeaningtoolError`: if there is any kind of problem while 
                getting the conection to meaningtool.
            `ValueError`: if the `content_language` isn't valid.
        """
        self._validate_parameters(source, input, url_hint, content_language)

        url = u"%s/tags" % self._base_url
        data = {}
        headers = []

        data["source"] = source.encode("utf8")
        data["input"] = input.encode("utf8")
        data["api_key"] = self.api_key

        if url_hint:
            self._validate_url(url_hint)
            data["url_hint"] = url_hint.encode("utf8")

        if content_language:
            content_language = content_language[:2].lower()
            headers.append(("Content-Language", content_language.encode("ascii")))

        # Even if POST, it's idempotent as GET.
        return self._parse_result(self._req("POST", url, data, headers))

    def _validate_url(self, url):
        """ Validates that the url has a url format.

        :parameters:
            url: str
                the url to validate.

        :exceptions:
            `InvalidUrl`: if the url isn't valid.
        """
        if not _re_url.match(url):
            raise InvalidUrl(url)

    def _validate_parameters(self, source, input, url_hint, content_language, \
                                        additionals=None):
        """ Validates that the values used for the API are valid.
        The valid values are the ones that are on the documentation.

        :parameters:
            source: str
                indicates the type of the input
            input: str
                the data to categorize.
            url_hint: str
                the url from where the data was taken
            content_language: str
                the language of the input.

        :exceptions:
            `InvalidParameter`: if a parameter has an invalid value.
            `InvalidUrl`: if the input (when the source is url) or the url_hint
                aren't valid urls.
        """
        if not source in ["text", "url", "html"]:
            raise InvalidParameter("The 'source' is invalid")
        if source == "url":
            self._validate_url(input)
        if url_hint:
            self._validate_url(url_hint)
        if content_language and not len(content_language) == 2:
            raise InvalidParameter("The 'content_language' should be 2 chars")
        if additionals:
            for value in additionals:
                if value not in \
                    ["top-terms", "classifiers", "classifiers-top-terms"]:
                    raise InvalidParameter("The 'additionals' is invalid")
                
