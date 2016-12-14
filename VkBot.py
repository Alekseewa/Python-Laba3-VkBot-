import vk
import time
import datetime
import pyowm

owm = pyowm.OWM("69bbca9d1eab20bbc6e314c78c28d893")
obs= owm.weather_at_place('Rostov-on-Don,ru')
weather = obs.get_weather()
location = obs.get_location()
strana = location.get_country()
oblaka = weather.get_clouds()
vet = weather.get_wind()['deg']
fc = owm.daily_forecast('Rostov-on-Don,ru')
rain = fc.will_have_rain()

translate = {'Rostov-na-Donu' : 'Ростов-на-Дону'}

def obl() :
    if 0 <= oblaka <= 10:
        return 'ясная'

    if 10 < oblaka <= 50:
        return 'облачная'

    if 50 < oblaka <= 100:
        return 'пасмурная'
def deg():
    if 0 <= vet < 90:
        return 'северо-восточный'
    if vet == 90:
        return  'восточный'
    if 91 <= vet < 180:
        return 'юго-восточный'
    if vet == 180:
        return 'южный'
    if 181 <= vet < 270:
        return 'юго-западный'
    if vet == 270:
        return 'западный'
    if 271 <= vet < 360:
        return ('северо-западный')
    if vet == 360:
        return  'северный'
def rainn():
    if rain == 0:
        return "Осадков не ожидается"
    if rain == 1:
        return 'Ожидаются осадки'

session = vk.Session('77625ce91a6a7e06dc372f5275bc6e8577828a624d506b683dd58e2f162588fb83224a9c652c2d59801b6')

api = vk.API(session)

while (True):

    messages = api.messages.get()

    commands = ['Погода', 'Как дела?', 'Привет', 'Помощь', '']

    messages = [(m['uid'], m['mid'], m['body'])
                for m in messages[1:] if m['body'] in commands and m['read_state'] == 0]

    for m in messages:
        user_id = m[0]
        message_id = m[1]
        comand = m[2]

        date_time_string = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        if comand == 'Помощь':
            api.messages.send(user_id=user_id,
                              message=date_time_string + '\n>Разработано Щуровой Юлией \n'
                                                        + ' Доступные команды: Привет, Как дела? Помощь, Погода \n')
        if comand == 'Привет':
            api.messages.send(user_id=user_id,
                              message='\n>Привет, чем я могу помочь тебе? ')

        if comand == 'Как дела?':
            api.messages.send(user_id=user_id,
                              message='\n>Могло быть и лучше, как насчет погода на сегодня?')
        if comand == 'Погода':
            api.messages.send(user_id=user_id,
                              message='Погода в городе ' + translate[location.get_name()]
                                      + ' на ' + obs.get_reception_time(timeformat='iso') + 'Ожидается ' + obl()
                                      + 'погода. Ветер ' + deg() + 'со скоростью = ' + str(weather.get_wind()['speed'])
                                      +'м/с') + rainn() + 'Температура составляет ' \
                                + str(weather.get_temperature('celsius')['temp']) + 'градусов по цельсию.'

    ids = ', '.join([str(m[1]) for m in messages])

    if ids:
        api.messages.markAsRead(message_ids=ids)

    time.sleep(3)