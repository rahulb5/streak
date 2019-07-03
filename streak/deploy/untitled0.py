import requests
import json

api_url = 'https://emt.edelweiss.in/edelmw-content/content/charts/v2/main/M1/NSE/EQUITY/11536_NSE'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHAiOjAsImV4cCI6MTUzMTQ1MjU0MywiZmYiOiJNIiwiaXNzIjoiZW10IiwibmJmIjoxNTI4ODYwMjQzLCJhcHBpZCI6ImM2ZjZhMDMzYjBiZWY1OTExNzNmNjM1N2I4YTllMDYyIiwic3JjIjoiZW10bXciLCJpYXQiOjE1Mjg4NjA1NDMsImF2IjoiMTUuMSIsImJkIjoiYW5kcm9pZC1waG9uZSJ9.BruotpCV-NyiCmeSAPm_AvyeY6kYzF04TWSvtIOnpfc'
headers = {
    'accept': 'application/json',
    'appidkey': api_key,
    'content-type': 'application/json',
}

data = '{"frcConti":false,"crpAct":true,"conti":false, "chTyp":"Interval", "tiInLst": [{"tiTyp": "SMA", "tiIn": {"period" : 14}}, {"tiTyp": "SMA", "tiIn": {"period" : 100}}], "isPvl":true}'

response = requests.post(api_url, headers=headers, data=data)
print(response.status_code)
data = json.loads(response.content.decode('utf-8'))
datapoints = {}
pltpnts = data['data']['pltPnts']


key_list = ['open','close', 'high', 'low' , 'vol' , 'ltt']
tiOut = data['data']['tiOut']
for i in key_list:
    temp_list = [pltpnts[i][-2] ,pltpnts[i][-1]]
    datapoints[i] = temp_list
    
for i in range(0 , len(tiOut)):
    datapoints[str(i)] = [tiOut[i]['rsltSet'][0]['vals'][-2], tiOut[i]['rsltSet'][0]['vals'][-1] ]

print(datapoints['ltt'])