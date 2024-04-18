import requests
from lxml import html
import re
import yfinance as yf
import pandas as pd
from datetime import date, datetime,timedelta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1',
    'Sec-GPC': '1',
    'TE': 'Trailers'
}

x_preco_atual = '//*[@id="carbon_fields_fiis_header-2"]/div/div/div[1]/div[1]/p'
x_ultimo_dividendo = '//*[@id="indicators"]/div[2]/p[2]/b'
x_p_vp = '//*[@id="indicators"]/div[7]/p[2]/b'
x_valor_patrimonial = '//*[@id="indicators"]/div[5]/p[2]'
x_dividendos_hitoricos = '//*[@id="table-dividends-history"]/tbody/tr[1]/td[4]'

def cotacao_atual(ativo):
    url_base = 'https://www.fundsexplorer.com.br/funds/'
    url = url_base + ativo
    response = requests.get(url, verify=False)
    tree = html.fromstring(response.content) 
    valor = tree.xpath(x_preco_atual)[0].text_content()
    valor = valor[3:]
    valor = float(valor.replace(',','.'))
    
    return valor

def ultimo_dividendo(ativo):
    url_base = 'https://www.fundsexplorer.com.br/funds/'
    url = url_base + ativo
    response = requests.get(url, verify=False)
    tree = html.fromstring(response.content) 
    valor = tree.xpath(x_ultimo_dividendo)[0].text_content()
    valor = float(valor.replace(',','.'))
    
    return valor

def p_vp(ativo):
    url_base = 'https://www.fundsexplorer.com.br/funds/'
    url = url_base + ativo
    response = requests.get(url, verify=False)
    tree = html.fromstring(response.content) 
    valor = tree.xpath(x_p_vp)[0].text_content()
    valor = float(valor.replace(',','.'))
    
    return valor

def valor_patrimonial(ativo):
    url_base = 'https://www.fundsexplorer.com.br/funds/'
    url = url_base + ativo
    response = requests.get(url, verify=False)
    tree = html.fromstring(response.content) 
    valor = tree.xpath(x_valor_patrimonial)[0].text_content()
    valor_numerico = re.search(r'\d+\,\d+', valor)

    valor_numerico = float(valor_numerico.group().replace(',', '.'))
    
    return valor_numerico

def cotacao_historica(ativo):
    df1 = pd.DataFrame()
    datas = []
    chamada_api = yf.Ticker(ativo+'.SA').history(period='12mo')
    closes = chamada_api['Close'].values
    df1[ativo] = closes
    datas.append(list(chamada_api.index.date))
    df1['Datas'] = datas[0]
    df1 = df1.set_index('Datas', drop=True)

    return df1

def dividendos_historicos(ativo):
    url_base = 'https://investidor10.com.br/fiis/'
    url = url_base + ativo
    response = requests.get(url, verify=False)
    tree = html.fromstring(response.content) 
    valor = tree.xpath(x_dividendos_hitoricos)[0].text_content()
    #valor = valor[3:]
    #valor = float(valor.replace(',','.'))
    
    return valor

print(dividendos_historicos('knip11'))