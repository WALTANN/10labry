import random
import requests
import pyttsx3
import datetime
import speech_recognition as sr
import webbrowser


# распознавание речи
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        print("Вы сказали:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Речь не распознана")
        return ""
    except sr.RequestError as e:
        print("Ошибка в запросе:", e)
        return ""


# импорт списка праздников
def get_holidays(country_code, year):
    url = f"https://date.nager.at/api/v2/publicholidays/{year}/{country_code}"
    response = requests.get(url)
    if response.status_code == 200:
        holidays = response.json()
        return holidays
    else:
        print("Ошибка при получении праздников")
        return None


# обработкa команд
def process_command(command, holidays, engine):
    if "привет" in command:
        greetings = ["салам", "здарова", "васап"]
        greeting = random.choice(greetings)
        print(greeting)
        engine.say(greeting)
    elif "как дела" in command:
        responses = ["Прекрасно, спасибо!", "Неплохо, спасибо!", "У меня всё отлично, спасибо!"]
        response = random.choice(responses)
        print(response)
        engine.say(response)
    elif "что ты умеешь" in command:
        print("Доступные команды:")
        print("1. привет")
        print("2. как дела")
        print("3. перечислить")
        print("4. сохранить")
        print("5. даты")
        print("6. ближайший")
        print("7. количество")
        print("8. открыть праздники")
        engine.say("Доступные команды: привет, как дела, перечислить, сохранить, даты, ближайший, количество, открыть праздники")
    elif "перечислить" in command:
        print("Список праздников:")
        for holiday in holidays:
            print(holiday["name"])
    elif "сохранить" in command:
        with open("names.txt", "w", encoding="utf-8") as file:
            for holiday in holidays:
                file.write(holiday["name"] + "\n")
        print("Список праздников сохранен в файле names.txt")
    elif "даты" in command:
        with open("dates.txt", "w", encoding="utf-8") as file:
            for holiday in holidays:
                file.write(f"{holiday['date']} - {holiday['name']}\n")
        print("Список праздников с датами сохранен в файле dates.txt")
    elif "ближайший" in command:
        today = datetime.date.today()
        nearest_holiday = min(holidays, key=lambda x: abs(datetime.datetime.strptime(x['date'], '%Y-%m-%d').date() - today))
        print("Ближайший праздник:", nearest_holiday["name"], "дата:", nearest_holiday["date"])
    elif "количество" in command:
        print("Количество праздников:", len(holidays))
    elif "открыть праздники" in command:
        webbrowser.open("https://date.nager.at/")
    else:
        print("Не распознана команда")


def main():
    country_code = "GB"
    year = 2020

    holidays = get_holidays(country_code, year)
    if holidays is None:
        return

    engine = pyttsx3.init()

    while True:
        command = recognize_speech()
        if command:
            process_command(command, holidays, engine)
            engine.runAndWait()


if __name__ == "__main__":
    main()
