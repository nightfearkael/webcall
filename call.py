import cgi
import json
from asterisk.ami import AMIClient, SimpleAction

#CGI Params
form = cgi.FieldStorage()
#Get value 'manager' from params (managers internal number)
internal_number = form.getvalue('manager')
#Get value 'client' from params (clients phone number)
client_number = form.getvalue('client')

#Авторизация на Астериске
client = AMIClient(address='192.168.1.170', port=5038, timeout=None)
client.login(username='Python_user', secret='strong_password')

#Запрос у астера информации о extension
action = SimpleAction(
    name='SIPshowpeer',
    Peer=internal_number
)
#Получение Custom Context extension'a
ext = client.send_action(action)
context = ext.response.keys['Context']

#Создание действия для астера с параметрами
action = SimpleAction(
    name='Originate',
    Channel=f'SIP/{internal_number}',
    Exten=f'{client_number}',
    Priority=1,
    Context=context,
    CallerID='Webcall',
)

#Отправка задачи на Астер
call = client.send_action(action)
#Получаем статус звонка
call_status = call.response.status

if call_status == 'Success':
    status_code = 1
else:
    status_code = 0

#Закрытие подключения к Астеру
client.logoff()

#Return content type
print("Content-type: application/json\n")
#Generate json object for response
response = {'statusCode': status_code}
#Return json
print(json.dumps(response))
