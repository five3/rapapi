import json
import jsonpath

class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')

        return json.JSONEncoder.default(self, obj)


def reset_jsonpath_value(obj, jsonp, value):
    arr = jsonp.split('.')
    loop_obj = obj
    loop_str = ['obj']

    try:
        for node in arr:
            loop_obj = loop_obj.get(node)
            if not loop_obj:
                print('Get JSON Node Fail')
                return obj
            loop_str.append(f'["{node}"]')

        eval_str = '%s="%s"' % (''.join(loop_str), value)
        exec(eval_str)
    except Exception as e:
        print(f'Exception In [reset_jsonpath_value] {e}')

    return obj


def is_node_empty(obj, jsonp):
    return not jsonpath.jsonpath(obj, f'$.{jsonp}')


if __name__ == '__main__':
    obj = {
        "status_code" : 200,
        "reason" : "",
        "headers" : {
            "Server" : "192.48",
            "Date" : "Mon, 03 Jun 2019 06:50:31 GMT",
            "Content-Type" : "application/json;charset=UTF-8",
            "Transfer-Encoding" : "chunked",
            "Connection" : "keep-alive",
            "X-Application-Context" : "ar-zuul-internet:test:8041",
            "Access-Control-Allow-Credentials" : "true",
            "Access-Control-Expose-Headers" : "Set-Cookie",
            "Content-Encoding" : "gzip"
        },
        "content" : { "$binary" : "eyJyZXR1cm5Db2RlIjowLCJyZXR1cm5Nc2ciOiJPSyIsInJlc3VsdCI6bnVsbH0=", "$type" : "00" },
        "text" : "{\"returnCode\":0,\"returnMsg\":\"OK\",\"result\":null}"
    }
    # reset_jsonpath_value(obj, "headers.Date", '')
    reset_jsonpath_value(obj, "content.result.pageView", '')

    print(obj)
