# flask_asterisk_dev
## 


**Приложение, написанное с использованием фраемвока Flask**

Возможности:
1. Выгрузка контактов из FreePBX в JSON файл
2.Отображение выгрузки на web странице
3. Поиск по отображаемой информации
4. Функция транслита из кириллицы в латиницу и обратно без потери смысла и искажения информации
5. Проверка доступности устройства, вывод его IP адреса
6. Функция звонка с сайта с выбором исходящей линии

*для работы необходимо создать файл **config.ini** со следующим содержимым:*
---
##  config.ini

[mysql]\
host = host_freepbx\
database = asteriskcdrdb\
user = user_db\
password = password_db\

[paramiko]\
machine = host_freepbx\
username = user_ssh\
password = pass_ssh\
port = port_ssh\

---
