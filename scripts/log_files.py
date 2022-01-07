# Logs
# /access.log        {status=206}    {type="application/octet-stream"}    {root_only}
# /error.log         {status=206}    {type="application/octet-stream"}    {root_only}
# /log/access.log    {status=206}    {type="application/octet-stream"}    {root_only}
# /log/error.log     {status=206}    {type="application/octet-stream"}    {root_only}
# /log/log.log       {status=206}    {type="application/octet-stream"}    {root_only}
# /logs/error.log    {status=206}    {type="application/octet-stream"}    {root_only}
# /logs/access.log   {status=206}    {type="application/octet-stream"}    {root_only}
# /errors.log        {status=206}    {type="application/octet-stream"}    {root_only}
# /debug.log         {status=206}    {type="application/octet-stream"}    {root_only}
# /db.log            {status=206}    {type="application/octet-stream"}    {root_only}

# /log.txt                {status=200}    {type="text/plain"}
# /log.tar.gz             {status=206}    {type="application/octet-stream"}    {root_only}
# /log.rar                {status=206}    {type="application/octet-stream"}    {root_only}
# /log.zip                {status=206}    {type="application/octet-stream"}    {root_only}
# /log.tgz                {status=206}    {type="application/octet-stream"}    {root_only}
# /log.tar.bz2            {status=206}    {type="application/octet-stream"}    {root_only}
# /log.7z                 {status=206}    {type="application/octet-stream"}    {root_only}

from lib.common import save_script_result


def do_check(self, url):
    if url == '/' and self.conn_pool:
        folders = ['']
        for log_folder in ['log', 'logs', '_log', '_logs', 'accesslog', 'errorlog']:
            status, headers, html_doc = self.http_request('/' + log_folder)

            if status in (301, 302):
                location = headers.get('location', '')
                if location.startswith(self.base_url + '/' + log_folder + '/') or \
                        location.startswith('/' + log_folder + '/'):
                    folders.append(log_folder)
                    self.enqueue(log_folder)
                    self.crawl('/' + log_folder + '/')

            if status == 206 and self._404_status != 206:
                save_script_result(self, status, self.base_url + '/' + log_folder, '',
                                   'Log File Found')

        url_lst = ['access.log', 'www.log', 'error.log', 'log.log', 'sql.log',
                   'errors.log', 'debug.log', 'db.log', 'install.log',
                   'server.log', 'sqlnet.log', 'WS_FTP.log', 'database.log', 'data.log', 'app.log',
                   'log.tar.gz', 'log.rar', 'log.zip',
                   'log.tgz', 'log.tar.bz2', 'log.7z']

        for log_folder in folders:
            for _url in url_lst:
                url_prefix = '/' + log_folder if log_folder else ''
                status, headers, html_doc = self.http_request(url_prefix + '/' + _url)
                # print '/' + log_folder + '/' + _url
                if status == 206 and \
                        (self._404_status == 404 or headers.get('content-type', '').find('application/') >= 0):
                    save_script_result(self, status, self.base_url + url_prefix + '/' + _url,
                                       '', 'Log File')

        for log_folder in folders:
            for _url in ['log.txt', 'logs.txt']:
                url_prefix = '/' + log_folder if log_folder else ''
                status, headers, html_doc = self.http_request(url_prefix + '/' + _url)
                # print '/' + log_folder + '/' + _url
                if status == 206 and headers.get('content-type', '').find('text/plain') >= 0:
                    save_script_result(self, status, self.base_url + url_prefix + '/' + _url,
                                       '', 'Log File')
