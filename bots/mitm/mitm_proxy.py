import mitmproxy.http
from mitmproxy import ctx


class Mitmccb:
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host == "ibsbjstar.ccb.com.cn":
            ctx.log.info("catch search word: %s" % flow.request)
            return

    def response(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.host == "ibsbjstar.ccb.com.cn":
            ctx.log.info("catch response word: %s" % flow.response.get_text())
            return


addons = [
    Mitmccb()
]