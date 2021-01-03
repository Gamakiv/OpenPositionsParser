import requests
import json
import datetime

def GetOpenPos():
  url = 'https://scripts.tlap.com/open_positions/'
  r = requests.get(url)

  if r.status_code == 200:
    print("Data received. 200.")
  elif r.status_code == 404:
    print("Data not found. 404")
    exit()

  with open('open_positions.json', 'w') as output_file:
    output_file.write(r.text)

def ReadJsonData():
  with open('open_positions.json') as f:
    file_content = f.read()
    templates = json.loads(file_content)

  print('Data from file received. Ok.')
  return (templates)


def ParsDataJson():
  ParsDataJson = json.loads(ReadJsonData())

  #получим дату
  value_date = datetime.datetime.fromtimestamp(ParsDataJson['timestamp'])
  #print(value_date.strftime('%Y-%m-%d %H:%M:%S'))

  #Getsimbol = ParsDataJson['bycompany']['XTrade']['AUDUSD']['buy']
  #будем отбирать по компании
  Getsimbol = ParsDataJson['bycompany']
  OutputData = []

  # получить значение компании
  for k, v in Getsimbol.items():

    #обработка исключения NoneType - для  \"Oanda\": null
    if v is None:
      break

    for k1, v1 in v.items(): # получить значение инструмента
      Symbol = k1

      for k2, v2 in v1.items(): #получить значение sell/buy
        Buy = v1.get('buy')
        Sell = v1.get('sell')
        SymbolBuySell = Symbol + ':' + str(Buy) + ':' + str(Sell)
        OutputData.append(SymbolBuySell)
        continue

  #убрать дубликаты
  OutputData = list(set(OutputData))

  return OutputData

def AverageCalc(EtalonList):
    SourceData = ParsDataJson()
    OutputAvarageList = []
    IterCount = 0
    SummBuy = 0
    SummSell = 0
    AverageBuy = 0
    AverageSell = 0

    for Element in EtalonList:
      #print('Calculate for ', Element)

      for k in SourceData:
        if Element in k:
          ChunkString = k.split(':')
          SummBuy = SummBuy + float(ChunkString[1])
          SummSell = SummSell + float(ChunkString[2])
          IterCount = IterCount + 1

      #если нет нужных нам символов - выйти
      if (SummBuy == 0) or (SummSell == 0):
        continue

      #расчет среднего с округлением до 2 знаков после точки
      AverageBuy = SummBuy / IterCount
      AverageBuy = round(AverageBuy, 2)

      AverageSell = SummSell / IterCount
      AverageSell = round(AverageSell, 2)

      ResutStr = Element + ':' + str(AverageBuy) + ':' + str(AverageSell)
      #print(ResutStr)
      OutputAvarageList.append(ResutStr)

      #обнулим переменные
      IterCount = 0
      SummBuy = 0
      SummSell = 0
      AverageBuy = 0
      AverageSell = 0
      ResutStr = ''

    return(OutputAvarageList)

def WriteData(InputData):

  Path = r'C:\Program Files (x86)\RoboForex - MetaTrader 4\MQL4\Files\open_positions.txt'
  FileData = open(Path, 'w')

  for Item in InputData:
    FileData.write("%s\n" % Item)


if __name__ == '__main__':

  CheckSymlols = ['EURUSD', 'GBPUSD', 'AUDUSD', 'NZDUSD', 'USDCHF',
                  'USDJPY', 'USDCAD', 'XAUUSD', 'AUDCAD', 'AUDJPY',
                  'AUDNZD','CADJPY', 'EURAUD', 'EURCAD', 'EURCHF',
                  'EURGBP', 'EURJPY', 'GBPAUD', 'GBPCAD', 'GBPCHF',
                  'GBPJPY']

  #GetOpenPos()
  #ReadJsonData()
  #ParsDataJson()
  #AverageCalc(CheckSymlols)
  WriteData(AverageCalc(CheckSymlols))