from wsgiref.simple_server import make_server
import urllib.parse
import json


def application(environ, start_response):
    credentials = {
        "Cyberman": "John Lumic",
        "Dalek": "Davros",
        "Judoon": "Shadow Proclamation Convention 15 Enforcer",
        "Human": "Leonardo da Vinci",
        "Ood": "Klineman Halpen",
        "Silence": "Tasha Lem",
        "Slitheen": "Coca-Cola salesman",
        "Sontaran": "General Staal",
        "Time Lord": "Rassilon",
        "Weeping Angel": "The Division Representative",
        "Zygon": "Broton",
    }

    query_string = environ['QUERY_STRING']
    params = urllib.parse.parse_qs(query_string)
    species = params.get('species', [''])[0]

    response_body = json.dumps({
        "credentials": credentials.get(species, "Unknown")
    })

    status = '200 OK' if species in credentials else '404 Not Found'
    headers = [('Content-Type', 'application/json'), ('Content-Length', str(len(response_body)))]

    start_response(status, headers)
    return [response_body.encode('utf-8')]


if __name__ == '__main__':
    port = 8888
    server = make_server('', port, application)
    print(f"Running on port {port}...")

    server.serve_forever()
