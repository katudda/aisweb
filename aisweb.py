import requests
from bs4 import BeautifulSoup

def get_page_content(icao_code):
    req = requests.get(f"https://www.aisweb.decea.gov.br/?i=aerodromos&codigo={icao_code}")
    content = ""

    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

    return content

def get_aerodromo(content):
    soup = get_parser(content)
    aero = soup.find('h1').get_text()
    aero = aero.replace("\n", " ").replace("CIAD:", "\n-- -- CIAD:")
    print(f"\n\n-- Aeródromo: {aero}")

def get_parser(content):
    return BeautifulSoup(content, 'html.parser')

def get_sunset(content):
    soup = get_parser(content)
    print(f"-- Sunset: {soup.find('sunset').get_text()}")


def get_sunrise(content):
    soup = get_parser(content)
    print(f"-- Sunrise: {soup.find('sunrise').get_text()}")

def get_metar(content):
    soup = get_parser(content)
    p_list = soup.find_all('h5', attrs={'class': 'mb-0 heading-primary'})
    metar = p_list[0].find_next_sibling('p').get_text().replace("\n", " ")
    print(f"-- METAR: \n\t{metar}")

def get_taf(content):
    soup = get_parser(content)
    p_list = soup.find_all('h5', attrs={'class': 'mb-0 heading-primary'})
    taf = p_list[1].find_next_sibling('p').get_text().replace("\n", " ")
    print(f"-- TAF: \n\t{taf}")

def get_cartas(content):
    soup = get_parser(content)
    link_list = soup.find_all('a', href=True, attrs={'onclick':"javascript:pageTracker._trackPageview('/cartas/aerodromos');"})

    print("-- Cartas:\n")
    for link in link_list:
        print(f" -- {link.get_text()} \n -- Download: {link['href']}\n")
    print("----------")

if __name__ == '__main__':
    import sys
    icao_code = sys.argv[1]

    content = get_page_content(icao_code)
    get_aerodromo(content)
    get_sunset(content)
    get_sunrise(content)
    get_metar(content)
    get_taf(content)
    get_cartas(content)