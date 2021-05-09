import requests
import smtplib

patient_sid = ''
csrf_token = ''
prescriptionId = ""

#Krakow
geo_id = "1261011"
voi_Id = "12"

# Rzeszow
# geo_id = "1863011"
# voi_Id = "18"

#Katowice
# geo_id = "2469011"
# voi_Id = "24"

# hourRange":{"from":"16:00","to":"20:00"}

headers = {
    'authority': 'pacjent.erejestracja.ezdrowie.gov.pl',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    'accept': 'application/json, text/plain, */*',
    'x-csrf-token': csrf_token,
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://pacjent.erejestracja.ezdrowie.gov.pl',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://pacjent.erejestracja.ezdrowie.gov.pl/rezerwacja-wizyty',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,pl;q=0.7',
    'cookie': ('patient_sid=%s' % patient_sid)
}

# Rzeszow 1863011 voiId 18
payload = {
    "dayRange": {
        "from": "2021-05-09",
        "to": "2021-05-30"
    },
    "geoId": geo_id,
    "prescriptionId": prescriptionId,
    "voiId": voi_Id,
    "vaccineTypes": ["cov19.astra_zeneca", "cov19.pfizer", "cov19.moderna"]
}

r = requests.post('https://pacjent.erejestracja.ezdrowie.gov.pl/api/calendarSlots/find', headers=headers, json=payload)

response = r.json()
# print(response)
slots = ""
for slot in response['list']:
    address = slot['servicePoint']['addressText']
    s = address + " " + slot['vaccineType'] + " " + slot['startAt']
    slots += s.encode("ascii", "ignore").decode("ascii") + '\n'

if len(response['list']) > 0:
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.login("", "")
    mail_body = """From: Mateusz Szulc <mateusz.szulc@gmail.com>
To: Mateusz Szulc <mateusz.szulc@hotmail.com>, Krzysztof Piszczek <krzysztof.piszczek@gmail.com>
Subject: Vaccine Found

%s
""" % slots

    print(mail_body)
    # server.sendmail("mateusz.szulc@gmail.com", ["mateusz.szulc@hotmail.com"], mail_body)

for slot in response['list']:
    address = slot['servicePoint']['addressText']
    print(address + " " + slot['vaccineType'] + " " + slot['startAt'])
