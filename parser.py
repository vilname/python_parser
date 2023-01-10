from service.parser_service import ParserService

name_script = "1"

list_host = [
    # '11.111.111.111',
    # '222.222.22.222',
    # '33.333.333.333'
]


def get_source_html(url):
    parser_service = ParserService(list_host, url, name_script)
    parser_service.started()


def main():
    get_source_html(url='https://www.avito.ru/tatarstan/predlozheniya_uslug/transport_perevozki/kommercheskiye_perevozki-ASgBAgICAkSYC8SfAZoLiPgB?cd={}&user=2')


if __name__ == '__main__':
    main()