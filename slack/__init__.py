import urllib
import urllib2


SLACK_API_URL = 'https://slack.com/api/{METHOD}'
REQUEST_TIMEOUT = 10


__all__ = ['Chat', 'Files']


class Request(object):
    def __init__(self, token, channel, timeout):
        self._slack_api_url = SLACK_API_URL
        self._token = token
        self._channel = channel

        self._timeout = timeout

    def _request(self, url, values):
        values['token'] = self._token
        data = urllib.urlencode(values)
        req = urllib2.Request(url=url, data=data)
        f = urllib2.urlopen(req, timeout=self._timeout)

        return f


class Chat(Request):
    def __init__(self, token, channel, timeout):
        super(Chat, self).__init__(token, channel, timeout)

    def post_message(self, text):
        url = self._slack_api_url.format(METHOD='chat.postMessage')
        values = {'channel': self._channel, 'text': text}
        response = self._request(url, values)

        return response


class Files(Request):
    def __init__(self, token, channel, timeout):
        super(Files, self).__init__(token, channel, timeout)

    def upload_file(self, filename):
        url = self._slack_api_url.format(METHOD='files.upload')
        content = self._get_content(filename)
        values = {'channel': self._channel, 'filename': filename, 'content': content}
        response = self._request(url, values)

        return response

    def _get_content(self, filename):
        with open(filename) as f:
            content = f.read()

        return content


class Slack(object):
    def __init__(self, token, channel, timeout=REQUEST_TIMEOUT):

        self._token = token
        self._channel = channel

        self.chat = Chat(token, channel, timeout)
        self.files = Files(token, channel, timeout)





