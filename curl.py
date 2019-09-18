#!/usr/bin/python
# -*- coding: utf-8 -*-
import pycurl
from six import BytesIO


def request(uri,
            proxy_host=None,
            port=None,
            ssl_verify=False,
            verbose=False,
            headers={},
            method = "GET",
            user_agent=None
            ):
    curl_buffer = BytesIO()
    ch = pycurl.Curl()
    if proxy_host is not None and port is not None:
        ch.setopt(pycurl.PROXY, proxy_host)
        ch.setopt(pycurl.PROXYPORT, port)

    ch.setopt(pycurl.BUFFERSIZE, 12000000)
    ch.setopt(pycurl.URL, uri)
    ch.setopt(pycurl.CUSTOMREQUEST, method)
    if user_agent is None:
        ch.setopt(pycurl.USERAGENT,
                  'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
    else:
        ch.setopt(pycurl.USERAGENT, user_agent)
    ch.setopt(pycurl.WRITEFUNCTION, curl_buffer.write)
    ch.setopt(pycurl.FOLLOWLOCATION, True)
    # ch.setopt(pycurl.HEADER, True)
    if len(headers) > 0:
        ch.setopt(pycurl.HTTPHEADER, [k + ': ' + v for k, v in headers.items()])
    ch.setopt(pycurl.REFERER, "https://www.google.com")
    ch.setopt(pycurl.CONNECTTIMEOUT, 5000)
    ch.setopt(pycurl.TIMEOUT, 20000)
    ch.setopt(pycurl.VERBOSE, verbose)
    if ssl_verify:
        ch.setopt(pycurl.SSL_VERIFYPEER, 1)
        ch.setopt(pycurl.SSL_VERIFYHOST, 2)
        ch.setopt(pycurl.CAINFO, "cacert-2018-06-20.pem")
    ch.setopt(pycurl.COOKIEFILE, "")
    ch.setopt(pycurl.COOKIEJAR, "")
    try:
        ch.perform()
        res_code = ch.getinfo(pycurl.RESPONSE_CODE)
        resp = curl_buffer.getvalue()
        header_len = ch.getinfo(pycurl.HEADER_SIZE)
        header = resp[0: header_len]
        body = resp[header_len:]
        return {"header": header, "body": body, "res_code": res_code}
    except Exception as e:
        return {"header": "", "body": "", "res_code": 400}
