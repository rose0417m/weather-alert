import os
import requests
import smtplib
from email.mime.text import MIMEText

# Environment Variables
API_KEY = os.getenv("OWM_API_KEY")
CITY = "Kottayam"   

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")


def send_email(subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)


def check_weather():
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast"
        f"?q={CITY}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200:
        print("Error:", data)
        return

    current_temp = data["list"][0]["main"]["temp"]

    rain_expected = False

    for forecast in data["list"][:8]:  
        weather_main = forecast["weather"][0]["main"]

        if weather_main.lower() in ["rain", "drizzle", "thunderstorm"]:
            rain_expected = True
            break

    print(f"Temperature: {current_temp}°C")
    print(f"Rain Expected: {rain_expected}")

    if current_temp > 35 or rain_expected:

        subject = "⚠️ Weather Alert"

        body = (
            f"City: {CITY}\n"
            f"Temperature: {current_temp}°C\n"
            f"Rain Expected: {'Yes' if rain_expected else 'No'}\n\n"
            "Weather alert triggered!"
        )

        send_email(subject, body)
        print("Email alert sent!")

    else:
        print("No alert needed.")


if __name__ == "__main__":
    check_weather()