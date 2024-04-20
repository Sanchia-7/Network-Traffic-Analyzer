from flask import Flask, render_template, request
import socket
import requests
import re

app = Flask(__name__)

def resolve_url(url):
    url = re.sub(r'^https://', '', url)
    url = re.sub(r'^http://', '', url)
    url = re.sub(r'^www\.', '', url)
    
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.gaierror:
        return None

def sort_headers(headers):
    sorted_headers = {
        'Content': {},
        'X': {},
        'Set-Cookie': {},
        'Other': {}
    }
    for header_name, header_value in headers.items():
        if re.match(r'^Content-', header_name):
            sorted_headers['Content'][header_name] = header_value
        elif re.match(r'^X-', header_name):
            sorted_headers['X'][header_name] = header_value
        elif re.match(r'^Set-Cookie', header_name):
            sorted_headers['Set-Cookie'][header_name] = header_value
        else:
            sorted_headers['Other'][header_name] = header_value
    return sorted_headers


def fetch_traffic_info(url):
    ip_address = resolve_url(url)
    if ip_address:
        try:
            response = requests.get(f"http://{ip_address}", verify=False)
            status_code = response.status_code
            status_message = http_status_codes.get(status_code, 'Unknown')

            sorted_headers = sort_headers(response.headers)
            
            return {
                'url': url,
                'ip_address': ip_address,
                'status_code': status_code,
                'status_message': status_message,
                'headers': sorted_headers,
                'body': response.text
            }
        except requests.RequestException as e:
            return {'error': str(e)}

http_status_codes = {
    100: 'Continue',
    101: 'Switching Protocols',
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    203: 'Non-Authoritative Information',
    204: 'No Content',
    205: 'Reset Content',
    206: 'Partial Content',
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    402: 'Payment Required',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    407: 'Proxy Authentication Required',
    408: 'Request Timeout',
    409: 'Conflict',
    410: 'Gone',
    411: 'Length Required',
    412: 'Precondition Failed',
    413: 'Request Entity Too Large',
    414: 'Request-URI Too Long',
    415: 'Unsupported Media Type',
    416: 'Requested Range Not Satisfiable',
    417: 'Expectation Failed',
    500: 'Internal Server Error',
    501: 'Not Implemented',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout',
    505: 'HTTP Version Not Supported'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        traffic_info = fetch_traffic_info(url)
        return render_template('/trail1.html', traffic_info=traffic_info)
    return render_template('/trail1.html')

if __name__ == '__main__':
    app.run(debug=True)