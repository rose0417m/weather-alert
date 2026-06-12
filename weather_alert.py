import requests
import smtplib
import os

API_KEY = os.getenv("WEATHER_API_KEY")

CITY = "Thiruvananthapuram"

URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric"

response = requests.get(URL)
data = response.json()
print(data)

temp_alert = False
rain_alert = False

for item in data["list"]:
    temp = item["main"]["temp"]

    if temp > 35:
        temp_alert = True

    if "rain" in item:
        rain_alert = True

if temp_alert or rain_alert:

    subject = "Weather Alert"

    body = f"""
Temperature above 35°C: {temp_alert}
Rain predicted: {rain_alert}

City: {CITY}
"""

    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_ADDRESS")

    message = f"Subject: {subject}\n\n{body}"

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message)

    print("Alert sent!")

else:
    print("No alert needed.")