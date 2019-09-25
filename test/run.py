import os
import unittest
import datetime
from subprocess import call
from pytestreport.api import make_report

from ATU.util.datetime import get_current_time_as_str
from ATU.message.sendmail import SendMail
from RapAPI.api import RunWithNormal


class TestVR618(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report_data = {
            "generator": "PyTestReport 0.1.4",
            "title": "VR618C端API接口测试",
            "description": "VR618C端API接口测试",
            "report_summary": {
                "start_time": get_current_time_as_str()
            }
        }
        cls.results = []
        cls.start_time = datetime.datetime.now()

    @classmethod
    def tearDownClass(cls):
        cls.end_time = datetime.datetime.now()
        report_summary = cls.report_data['report_summary']
        report_summary['duration'] = (cls.end_time - cls.start_time).total_seconds()
        report_summary['suite_count'] = len(cls.results)

        summary = cls.warp_results()
        report_summary['status'] = summary['status']
        cls.report_data['report_detail'] = summary['detail']

        report_name = '618_VR_API_Report.html'
        with open(report_name, 'wb') as fp:
            make_report(fp, cls.report_data)

        image_name = report_name.replace('.html', '.png')
        cls.make_image(report_name, image_name)

        send_mail = SendMail(to=["chenxiaowu@autohome.com.cn", "xujindou@autohome.com.cn",
                                 "wuhui@autohome.com.cn", "zhangxuexue@autohome.com.cn",
                                 "lixiangyu9418@autohome.com.cn"],
                             cc=["haodan@autohome.com.cn"])
        attaches = [(report_name, 'text', 'html', report_name, 1)]
        send_mail.send_as_image('618_VR_API_Report', image_name, attaches=attaches)

    @classmethod
    def make_image(cls, html, image):
        js = os.path.join(os.path.dirname(__file__), "capture.js")
        cmds = ["phantomjs", js, html, image, "1350px"]
        output = call(cmds)
        if output == 0: 
            print('make capture success!')
        else:
            print('make capture failed!')

    @classmethod
    def warp_results(cls):
        summary = {
            'status': {},
            'detail': {}
        }
        tests = []
        pass_count = fail_count = error_count = skip_count = 0
        i = 1
        for name, result in cls.results:
            sub_pass_count = sub_fail_count = sub_error_count = sub_skip_count = 0
            sub_detail = []
            j = 1
            for cell in result:
                if cell.status:
                    sub_pass_count += 1
                else:
                    sub_fail_count += 1
                sub_detail.append({
                        "has_output": True,
                        "tid": "%st%s.%s" % ('p' if cell.status else 'f', i, j),
                        "desc": cell.url,
                        "output": '\r\n'.join(cell.detail),
                        "status": "pass" if cell.status else "fail",
                        "status_code": 0 if cell.status else 1
                })
                j += 1

            test = {
                "summary": {
                    "desc": name,
                    "count": sub_pass_count + sub_fail_count,
                    "pass": sub_pass_count,
                    "fail": sub_fail_count,
                    "error": sub_error_count,
                    "skip": sub_skip_count,
                    "cid": f"c{i}",
                    "status": "pass" if sub_fail_count == 0 else "fail"
                },
                "detail": sub_detail
            }
            tests.append(test)
            i += 1

            pass_count += sub_pass_count
            fail_count += sub_fail_count
            error_count += sub_error_count
            skip_count += sub_skip_count

        summary['status'] = {
            'pass': pass_count,
            'fail': fail_count,
            'error': error_count,
            'skip': skip_count
        }
        summary['detail'] = {
            'tests': tests,
            'pass': pass_count,
            'fail': fail_count,
            'error': error_count,
            'skip': skip_count,
            'count': pass_count + fail_count + error_count + skip_count
        }
        return summary

    def test_vr_brand_outside(self):
        result = RunWithNormal.apply_flow('vr_brand_outside')
        self.results.append(('test_vr_brand_outside', result))

    def test_vr_brand_audi(self):
        result = RunWithNormal.apply_flow('vr_brand_audi')
        self.results.append(('test_vr_brand_audi', result))

    def test_vr_brand_bmw(self):
        result = RunWithNormal.apply_flow('vr_brand_bmw')
        self.results.append(('test_vr_brand_bmw', result))

    def test_vr_brand_benz(self):
        result = RunWithNormal.apply_flow('vr_brand_benz')
        self.results.append(('test_vr_brand_benz', result))

    def test_vr_theme_new_engine(self):
        result = RunWithNormal.apply_flow('vr_theme_new_engine')
        self.results.append(('vr_theme_new_engine', result))

    def test_vr_theme_station_new_engine(self):
        result = RunWithNormal.apply_flow('vr_theme_station_new_engine')
        self.results.append(('vr_theme_station_new_engine', result))


if __name__ == '__main__':
    unittest.main()
