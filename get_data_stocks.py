import pandas_datareader.data as web
import os

def main(symbol="AMZN", start="2000-01-01", end="2020-02-22",dataSource="yahoo"):
    df = web.DataReader(name=symbol, data_source=dataSource, start=start, end=end)
    df = df.rename(columns={
        "Open": "open",
        "Close": "close",
        "High": "high",
        "Low": "low",
        "Volume": "volume"
    })
    if not os.path.isdir("data/raw_history/stocks"):
        os.mkdir("data/raw_history/stocks")

    df.to_csv(f"data/raw_history/stocks/{symbol}.csv")
    print(f"data saved for {symbol} from {start} to {end}")

def readFromTXT(filename):
    File_object = open(filename, "r")
    symbols = File_object.readlines()
    newList = []
    for sym in symbols:
        sym = sym.replace("\n", "")
        newList.append(sym)
    #print(newList)
    return newList


symbols = readFromTXT("data/s&p500_symbols.txt")

for symbol in symbols:
    startDate = "-01-01"
    endDate = "-01-02"
    i = 0
    print(f"===================================")
    print(f"starting loop for {symbol}")
    while i < 20:
        #print(f"trying for year {20 - i}")
        startDate = "-01-01"
        endDate = "-01-02"
        if i == 0:
            try:
                startDate = "2002-01-01"
                #df = web.DataReader(name=symbol, data_source="yahoo", start=startDate, end=endDate)
                main(symbol=symbol, start=startDate, end="2020-03-03")
                break
            except:
                print(f"2002 is not the oldest data")
        try:
            #print(type(str((2020 - i))))
            startDate = str((2020 - i)) + startDate
            endDate = str((2021 - i)) + endDate
            df = web.DataReader(name=symbol, data_source="yahoo", start=startDate, end=endDate)
        except:
            startDate = "-01-02"
            endDate = "-01-02"
            startDate = (str((2020 - i + 1))) + startDate
            print(f"oldest date {startDate} for {symbol}")
            main(symbol=symbol, start=startDate, end="2020-03-03")
            break
        if i == 19:
            startDate = "-01-01"
            endDate = "-01-02"
            startDate = (str((2020 - i + 1))) + startDate
            print(f"oldest date {startDate} for {symbol}")
            main(symbol=symbol, start=startDate, end="2020-03-03")

        print(f"i = {i}, date {startDate}")
        i += 1
    print(f"finished loop for {symbol}")