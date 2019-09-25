# RapAPI
> The Tool can be use to Record and Replay API request for API testing without write script by human.

## Install
You should install [mitmproxy](https://mitmproxy.org/) at first, and then install `RapAPI` as follow:
```bash
pip install dist/RapAPI_0.1.x.whl
# or
pip install git+https://git.corpautohome.com/ad-qa/rapapi.git
```

## How To Use
### Write Plugin Script
```python
from mitmproxy import ctx, flowfilter

class Recorder:
    def __init__(self):
        api_filter = ctx.options.dumper_filter if ctx.options.dumper_filter else ''
        self.filter = flowfilter.parse(api_filter)
    
    def request(self, flow):
        if flowfilter.match(self.filter, flow):
            request = flow.request
            request.headers.add(b'flag', 'test')
            ctx.log.info(f"Request URL: {request.url}")
            
    def response(self, flow):
        if flowfilter.match(self.filter, flow):
            response = flow.response
            ctx.log.info(f"Response Code: {response.status_code}")
            
    def error(self, flow):
        print(f'HTTP Error With [{flow.response.reason}], and body: {flow.response.text}')        
    
addons = [
    Recorder()
]
```
### Start proxy service
```bash
rapapi.record -h
rapapi.record -s /path/to/recorder.py -p 8181 -u "https://vr.api.autohome.com.cn/api"
# or
mitmdump -s /path/to/recorder.py -k -p 8181 "~u ^https://vr.api.autohome.com.cn/api.+"
```
### Install HTTPS certificate
1. configure your target device with the correct proxy settings
1. start a browser on the device
1. visit the magic domain`https://mitm.it`
1. You should see something like this
![](https://docs.mitmproxy.org/stable/certinstall-webapp.png)

### Replay Request
1. add validate rule by manual
1. run replay script
1. save as TestCase with `flow_name`

### Supported Validate Rule
1. `exclude` key, with list of jsonpath likely string
1. `not_empty` key,  with list of jsonpath likely string
1. jsonpath string should like `data.result.status`

## TODO
1. snapshot incorrect under linux platform
1. support to add validate rule by UI
