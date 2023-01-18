#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import configparser, pymysql.cursors, pathlib, sqlite3, paramiko, json

#* функция ssh_connection
class CFunc_conn:
    @staticmethod
    def paramiko_conn(paramiko_cammand):
        # Объединяем полученную строку с недостающими частями пути
        path_config = Path(pathlib.Path.cwd(), 'config.ini')
        print (path_config)
        config = configparser.ConfigParser()
        config.read(path_config, encoding='utf-8-sig')
        # Создать объект SSH
        ssh = paramiko.SSHClient()
        # Разрешить соединения с хостами, которых нет в файле know_hosts

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # подключиться к серверу
        ssh.connect(
            hostname=config.get('paramiko', 'machine'),
            port=config.get('paramiko', 'port'),
            username=config.get('paramiko', 'username'),
            password=config.get('paramiko', 'password')
            )
        # Исключая заказ
        stdin, stdout, stderr = ssh.exec_command(paramiko_cammand)
        # Получить результат команды
        res,err = stdout.read(),stderr.read()
        result = res if res else err
        # Закрыть соединение
        ssh.close()
        #возвращаем результат выполнения
        return (result)

#* функция транслита
class CFunc_translitizator:
    @staticmethod
    def translitizator(letter, dic):

        legend_ru_top = {
        'Щ':'Shh', 'щ':'shh',
        }
        legend_en_top = dict({v:k for k, v in legend_ru_top.items()})

        legend_ru_middle = {
        'Ё':'Yo', 'ё':'yo',
        'Ж':'Zh', 'ж':'zh',
        'Х':'Kh', 'х':'kh',
        'Ц':'Ts', 'ц':'ts',
        'Ч':'Ch', 'ч':'ch',
        'Ш':'Sh', 'ш':'sh',
        'Ы':'Yy', 'ы':'yy',
        'Й':'Ij', 'й':'ij',
        'Э':'Ej', 'э':'ej',
        'Ю':'Yu', 'ю':'yu',
        'Ъ':'Jj', 'ъ':'jj',
        'Я':'Ya', 'я':'ya',
        }
        legend_en_middle = dict({v:k for k, v in legend_ru_middle.items()})

        legend_ru_last = {
        'А':'A', 'а':'a',
        'Б':'B', 'б':'b',
        'В':'V', 'в':'v',
        'Г':'G', 'г':'g',
        'Д':'D', 'д':'d',
        'Е':'E', 'е':'e',
        'З':'Z', 'з':'z',
        'И':'I', 'и':'i',
        'К':'K', 'к':'k',
        'Л':'L', 'л':'l',
        'М':'M', 'м':'m',
        'Н':'N', 'н':'n',
        'О':'O', 'о':'o',
        'П':'P', 'п':'p',
        'Р':'R', 'р':'r',
        'С':'S', 'с':'s',
        'Т':'T', 'т':'t',
        'У':'U', 'у':'u',
        'Ь':"J", 'ь':"j",
        'Ф':'F', 'ф':'f',
        }
        legend_en_last = dict({v:k for k, v in legend_ru_last.items()})

        legend_ru_655={
        'А': 'A', 'а': 'a',
        'Б': 'B', 'б': 'b',
        'В': 'V', 'в': 'v',
        'Г': 'G', 'г': 'g',
        'Д': 'D', 'д': 'd',
        'Е': 'E', 'е': 'e',
        'Ё': 'YO', 'ё': 'yo',
        'Ж': 'ZH', 'ж': 'zh',
        'З': 'Z', 'з': 'z',
        'И': 'I', 'и': 'i',
        'Й': 'Y', 'й': 'y',
        'К': 'K', 'к': 'k',
        'Л': 'L', 'л': 'l',
        'М': 'M', 'м': 'm',
        'Н': 'N', 'н': 'n',
        'О': 'O', 'о': 'o',
        'П': 'P', 'п': 'p',
        'Р': 'R', 'р': 'r',
        'С': 'S', 'с': 's',
        'Т': 'T', 'т': 't',
        'У': 'U', 'у': 'u',
        'Ф': 'F', 'ф': 'f',
        'Х': 'KH', 'х': 'kh',
        'Ц': 'TS', 'ц': 'ts',
        'Ч': 'CH', 'ч': 'ch',
        'Ш': 'SH', 'ш': 'sh',
        'Щ': 'SHH', 'щ': 'shh',
        'Ъ': '', 'ъ': '',
        'Ы': 'Y', 'ы': 'y',
        "Ь": '', "ь": '',
        'Э': 'E', 'э': 'e',
        'Ю': 'YU', 'ю': 'yu',
        'Я': 'YA', 'я': 'ya',
        }

        legend_en_iii = {
            'i0'   :  '-',
            'i055' :  '729055',
            'i244' :  '258244',
            'i154' :  '652154',
            'i180' :  '653180',
            'i314' :  '653314',
            'i208' :  '652208',
            'i928' :  '655928',
            'i286' :  '230286',
            'i300' :  '251300',
            'i575' :  '605575',
            'i597' :  '606597',
            'i600' :  '628600',
            'i091' :  '629091',
            'i257' :  '651257',
            'i643' :  '650643',
            'i629' :  '652629',
            'i152' :  '653152',
            'i394' :  '653394',
            'i290' :  '656290',
            'i537' :  '653537',
            'i093' :  '651093',
            'i910' :  '957910',
            'i911' :  '957911',
            'i912' :  '957912',
            'i913' :  '957913',
            'i914' :  '957914',
            'i915' :  '957915',
            'i916' :  '957916',
            'i917' :  '957917',
            'i918' :  '957918',
            'i919' :  '957919',
            'i447' :  '653447',
            'i413' :  '653413',
            'i423' :  '653423',
            'i609' :  '652609',
            'i777' :  '652777',
            'i012' :  '653012',
            'i920' :  '957920',
            'i921' :  '957921',
            'i407' :  '653407',
            'i101' :  '629101',
            'i496' :  '652496',
            'i774' :  '652774',
            'i691' :  '658691',
            'i786' :  '652786',
            'i584' :  '653584',
        }

        if dic == 'ru':
            legend_id_dic = [legend_ru_top, legend_ru_middle, legend_ru_last]
        if dic == 'en':
             legend_id_dic = [legend_en_iii, legend_en_top, legend_en_middle, legend_en_last]
        if dic == 'ru_655':
            legend_id_dic = [legend_ru_655,]
        for legend_id in legend_id_dic:    
            for i, j in legend_id.items():
                letter = letter.replace(i, j)
        return letter.strip()

#* выгрузка из астера номеров
class CFunc_ast_to_number:
    @staticmethod
    def ast_to_number():
        path_config = Path(pathlib.Path.cwd(), 'config.ini')
        config = configparser.ConfigParser()
        config.read(path_config, encoding='utf-8-sig')
        connection = pymysql.connect(host=config.get('mysql', 'host'),
                            user=config.get('mysql', 'user'),
                            passwd=config.get('mysql', 'password'),
                            database=config.get('mysql', 'database'),
                            charset="utf8mb4")
        
        with connection:
            with connection.cursor() as cursor:
            # Read a single record
                sql = "SELECT `user`, `description` FROM `devices` ORDER BY `user`;"
                cursor.execute(sql,)
                result = cursor.fetchall()

        # формирования json массива
        data_number_db = {}
        data_number_db['data_number'] = []
        for d2 in result:
            print (d2[1])
            b_dict_ast = CFunc_translitizator.translitizator(d2[1], 'en')
            b_dict_ast_split = b_dict_ast.split("_")
            if len(b_dict_ast_split) == 2:
                b_dict_ast_split.append('None2')
            if len(b_dict_ast_split) == 1:
                b_dict_ast_split.append('None1')
                b_dict_ast_split.append('None2')
            data_number_db['data_number'].append({
                'number': d2[0],
                'user': b_dict_ast_split[0],
                'location': b_dict_ast_split[1],
                'outline' : b_dict_ast_split[2]
            })

        with open('data_number_db.json', 'wt', encoding='utf-8') as outfile:
            json.dump(data_number_db, outfile, ensure_ascii=False, indent=4)
        return (data_number_db)