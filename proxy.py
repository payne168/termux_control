from miproxy.proxy import AsyncMitmProxy, ProxyHandler


class MitmProxyHandler(ProxyHandler):
    def mitm_request(self, data):
        print('>> %s' % repr(data[:100]))
        return data

    def mitm_response(self, data):
        print('<< %s' % repr(data[:100]))
        return data


if __name__ == '__main__':
    proxy = None
    if not argv[1:]:
        proxy = AsyncMitmProxy(RequestHandlerClass=MitmProxyHandler)
    else:
        proxy = AsyncMitmProxy(RequestHandlerClass=MitmProxyHandler, ca_file=argv[1])
    try:
        proxy.serve_forever()
    except KeyboardInterrupt:
        proxy.server_close()
