from mitmproxy import ctx, flowfilter

from RapAPI.mongotuil import mongo_util
from RapAPI.constants import *
"""
mitmdump -s recorder.py -k -p 8181 "~u ^https://www.baidu.com/api.+"
"""


class Recorder:
    def __init__(self):
        self.request_no = 0
        self.response_no = 0

        config = mongo_util.get_config()
        self.max_record_num = config.get('max_record_num', 100)
        self.auto_flush = config.get('auto_flush', False)
        self.record_status = config.get('record_status', '')
        self.exclude_url_prefix = config.get('exclude_url_prefix', [])
        self.index = 0

        api_filter = ctx.options.dumper_filter if ctx.options.dumper_filter else API_FILTER[BusinessName.VR]
        self.filter = flowfilter.parse(api_filter)

    def request(self, flow):
        self.request_no += 1
        ctx.log.info(f"Requests had send: {self.request_no}")

        config = mongo_util.get_config()
        flow.record_status = config.get('record_status')

        if flowfilter.match(self.filter, flow) and flow.record_status == RecordStatus.START:
            if self.index == 0:
                mongo_util.clear_record()

            if self.index == self.max_record_num:
                if self.auto_flush:
                    mongo_util.clear_record()
                    self.index = 0
                else:
                    raise IndexError(f"max_record_num is {self.max_record_num}")

            flow.request.headers.add(b'request_no', str(self.request_no))

    def response(self, flow):
        self.response_no += 1
        ctx.log.info(f"Response had received: {self.response_no}")
        ctx.log.info(f"capture url: {flow.request.url}")

        if flowfilter.match(self.filter, flow) and flow.record_status == RecordStatus.START:
            for exclude in self.exclude_url_prefix:
                if exclude and exclude in flow.request.url:
                    ctx.log.info(f"skip for exclude: {exclude}")
                    return

            ctx.log.info(f"recording: {flow.request.url}")
            """
            Content Need Save as below:
                method, url, header, content 
            """
            request = flow.request
            headers = dict(request.headers)
            request_no = int(headers.pop('request_no'))
            request_data = {
                'method': request.method,
                'url': request.url,
                'headers': headers,
                'content': request.content,
                'text': request.text
            }

            """
            Content Need Save as below:
                status_code, reason, headers, content
            """
            response = flow.response
            response_no = self.response_no
            response_data = {
                'status_code': response.status_code,
                'reason': response.reason,
                'headers': dict(response.headers),
                'content': response.content,
                'text': response.text
            }

            mongo_util.save_record({'request_no': request_no, 'request_data': request_data,
                                    'response_no': response_no, 'response_data': response_data})
            self.index += 1
        elif flow.record_status == RecordStatus.STOP and self.index > 0:
            self.index = 0

    def error(self, flow):
        """
            An HTTP error has occurred, e.g. invalid server responses, or
            interrupted connections. This is distinct from a valid server HTTP
            error response, which is simply a response with an HTTP error code.
        """
        print(f'HTTP Error With {flow.response}')

        
addons = [
    Recorder()
]
