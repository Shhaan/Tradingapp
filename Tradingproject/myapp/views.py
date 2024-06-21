import pandas as pd
import json
from django.shortcuts import render 
from django.views import View 
from django.core.files.storage import FileSystemStorage
import asyncio 

# Candle class for creating candle instance for storing data
class Candle:
    def __init__(self, id, open, high, low, close, date):
        self.id = id
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.date = date

class Cvsreader(View):
    def get(self,request):

        return render(request,'App.html')
    def post(self,request):
        file =request.FILES.get('csvfile')
        time = int(request.POST.get('Addtime'))
        if not file :

            return render(request,'App.html',{'error':'Must upload a csv file'})
        if not time :

            return render(request,'App.html',{'error':'Plese Enter time'})
        fs = FileSystemStorage()
        filename = fs.save(file.name, file) 
        file_path = fs.path(filename)
        data = pd.read_csv(file_path,low_memory=False)
         
        candles = [Candle(index, row['OPEN'], row['HIGH'], row['LOW'], row['CLOSE'], row['DATE']) for index, row in data.iterrows()]
        
        converted_candles = asyncio.run(self.convert_timeframe(candles, time))
        json_data = json.dumps([candle.__dict__ for candle in converted_candles])

        json_file_name = f'{filename}.json'
        
        json_file_path = fs.path(json_file_name)
        
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
 
        download_url = fs.url(json_file_name)
 
 
        return render(request,'App.html',{'download_url': download_url})
         
 
          

    async def convert_timeframe(self, candles, timeframe):
            converted_candles = []
             
            
            for i in range(0, len(candles), timeframe):
                chunk = candles[i:i + timeframe]
                if not chunk:
                    continue 
                open_price = chunk[0].open
                close_price = chunk[-1].close
                high_price = max(candle.high for candle in chunk)
                low_price = min(candle.low for candle in chunk)
                date = chunk[0].date   
                
                converted_candles.append(Candle(i // timeframe, open_price, high_price, low_price, close_price, date))
            
            return converted_candles