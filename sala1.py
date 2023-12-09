# -*- coding: utf-8 -*-
import requests
import telebot
import pytz
from datetime import datetime
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

fuso_horario_sp = pytz.timezone('America/Sao_Paulo')

class Bot:
    def __init__(self):
        self.url_api = 'http://144.217.215.53:9923/api/treze/v2'
        self.message_gale = None

        # CHAT ID E TOKEN DO BOT
        self.chat_id = '-1002014635868'
        self.token = '6034798397:AAHeLTHjFAULracJz8NbKVeHsovrdlDIdcQ'
        self.bot = telebot.TeleBot(token=self.token, parse_mode='MARKDOWN', disable_web_page_preview=True)
        self.wins = 0
        self.loss = 0
        self.link = 'https://www.youtube.com/'
        self.verdes = 0
        self.count = 0
        #MARTINGALES 👇
        self.gales = 2


        self.daymon = []
        self.analisar = True
        #PROTEÇÃO NO 13 👇
        self.protection = True

        self.direction_color = []

        self.max_hate = 0
        self.deletemessage = False

        self.list_houra = []

        self.count_parcial = 0
        #RELATORIO
        self.ultim_count = 10

        self.date_now = str(datetime.now(fuso_horario_sp).strftime("%d/%m/%Y"))
        self.check_date = self.date_now
    def button_link(self):
        markup = InlineKeyboardMarkup()
        markup.row_width = 1  # Definir a largura da linha conforme necessário

        button_text = '🕹️CADASTRE-SE AQUI'  # Texto do botão
        button_url = self.link  # URL para redirecionamento

    # Criar e adicionar o botão ao teclado inline
        markup.add(InlineKeyboardButton(text=button_text, url=button_url))

        return markup

    def restart(self):
        if self.date_now != self.check_date:
            print("Reiniciando bot!")
            self.check_date = self.date_now
            # ZERA OS RESULTADOS
            self.wins = 0
            self.loss = 0
            self.verdes = 0
            self.max_hate = 0
            time.sleep(10)
            return True
        else:
            return False

    #ANALISADOR API
    def start(self):
        last_response = None
        while True:
            try:
                data = requests.get(self.url_api)
                response = data.json()
                if response != last_response:
                    last_response = response
                    self.caracteristicas(response)
                time.sleep(2)
            except Exception as e:
                print(f'ERROR API', e)
                time.sleep(2)

    #MAPEAMENTO DAS CORES E NUMEROS
    def mapeam(self, results):

        mapeamento = {
        '1': 'V',
        '2': 'P',
        '3': 'V',
        '4': 'P',
        '5': 'V',
        '6': 'P',
        '7': 'P',
        '8': 'P',
        '9': 'V',
        '10': 'P',
        '11': 'P',
        '12': 'V',
        '13': 'G',
        '14': 'V',
        '15': 'P',
        '16': 'V',
        '17': 'P',
        '18': 'V',
        '19': 'V',
        '20': 'P',
        '21': 'V',
        '22': 'P',
        '23': 'V',
        '24': 'P',
        '25': 'V'
    }
    
        return [mapeamento[numero] for numero in results]
    #DEF CARACTERISTICAS
    def caracteristicas(self, data):
        self.restart()
        strateg = self.mapeam(data['results'])
        print(strateg)
        print(data['results'])
        if self.deletemessage:
            self.bot.delete_message(chat_id=self.chat_id, message_id=self.message_gale)
            self.deletemessage = False

        
        if self.analisar:
            self.verificar_estrategias(strateg, data['results'])
        else:
            self.check_results(strateg[:1])
            
    def check_results(self, result): 
        print(result[:1])
        print(self.direction_color)
        if result[:1] == self.direction_color:
            self.martingale('WIN')
        elif self.protection == True and result[:1] == ['G']:
            self.martingale('VERDE')
        else:
            self.martingale('LOSS')

    #DEF GREEN RESULT
    def green_resu(self):
        print('GREEN')
        self.count = 0
        hora_atual_sp = datetime.now(fuso_horario_sp)
        self.list_houra.append({'STATUS': '✅GREEN', 'HORARIO' : hora_atual_sp.strftime('%H:%M')})
        self.max_hate += 1
        self.count_parcial += 1
        self.analisar = True
        self.wins += 1
        self.bot.reply_to(message=self.message_entrada_SUCESS, text=(f'''
✅✅✅*GREEN*✅✅✅
                                                                     
*🟢 WINS : {self.wins} |🔴 LOSS {self.loss} |🔵 13 : {self.verdes}*    

💵Estamos Com *{self.max_hate}* Wins Seguidos ‼️
'''))
        if self.count_parcial == self.ultim_count:
            self.parcial_text()
            self.count_parcial = 0
        return
    
    def green_empate_message(self):
        self.analisar = True
        print('GREEN NO VERDE')
        self.max_hate += 1
        self.wins += 1
        self.count_parcial += 1
        self.count = 0
        self.verdes += 1
        hora_atual_sp = datetime.now(fuso_horario_sp)
        self.list_houra.append({'STATUS': '✅GREEN NO 13', 'HORARIO' : hora_atual_sp.strftime('%H:%M')})
        self.bot.reply_to(message=self.message_entrada_SUCESS, text=(f'''
✅✅✅*GREEN NO 13*✅✅✅
                                                                     
*🟢 WINS : {self.wins} |🔴 LOSS {self.loss} |🔵 13 : {self.verdes}*    

💵Estamos Com *{self.max_hate}* Wins Seguidos ‼️
'''))
        if self.count_parcial == self.ultim_count:
            self.parcial_text()
            self.count_parcial = 0
        return
    
    def loss_message(self):
        print('LOSSS')
        self.max_hate = 0
        self.analisar = True
        self.count = 0
        self.count_parcial += 1
        hora_atual_sp = datetime.now(fuso_horario_sp)
        self.list_houra.append({'STATUS': '🔴LOSS', 'HORARIO' : hora_atual_sp.strftime('%H:%M')})
        self.bot.reply_to(message=self.message_entrada_SUCESS, text=(f'''
🔴*Loss Tenha Gerenciamento nas Entradas e Aguarde a Proxima oportunidade de Sinal*
'''))
        if self.count_parcial == self.ultim_count:
            self.parcial_text()
            self.count_parcial = 0
        return


    def martingale_message(self):
        self.deletemessage = True
        self.message_gale = self.bot.reply_to(message=self.message_entrada_SUCESS, text=(f'''
*⚠️Atenção Vamos para a {self.count}ª Proteção⚠️*
''')).message_id
        return
    #DEF MARTINGALE CHECK
    def martingale(self, data):

        if data == 'WIN':
            self.green_resu()
            return
        elif data == 'LOSS':
            self.count += 1
            if self.count > self.gales:
                self.loss += 1
                self.loss_message()
            else:
                self.martingale_message()
                return

        elif data == 'VERDE':
            self.green_empate_message()

    def parcial_text(self):
        message = ""
        for result in self.list_houra:
            message += f"{result['STATUS']} -> {result['HORARIO']}\n"
        self.bot.send_message(chat_id=self.chat_id, text=(f'''
*➡️RESULTADO DOS ULTIMOS {self.ultim_count} RESULTADOS🔵*

{message}

*🟢 WINS : {self.wins} |🔴 LOSS {self.loss} |🔵 13 : {self.verdes}*    
'''))
        self.list_houra = []
        return

    #DEF ENTRADA CONFIRMADA
    def send_alert(self, cor, padrao):
        print('Estrátégia Encontrada')
        self.analisar = False
        self.message_entrada_SUCESS = self.bot.send_message(chat_id=self.chat_id, text=(f'''
✅*ENTRADA CONFIRMADA*


🕹️ *Estratégia :* {padrao}                                                                         
➡️ *Entrar no :* {cor}     

🛡️ *Aplicar Proteção no :* 🟢

➡️ Fazer Até *{self.gales}* Proteções!
'''),reply_markup=self.button_link())
        return
    
    #DEF ESTRÁTEGIAS 👇
    def verificar_estrategias(self,results, numeros):
        if results[:3] == ['V', 'V', 'P']:
            strategy = 'Sequencia de Vermelhos'
            self.direction_color = ['P']
            cor = 'PRETO ⚫'
            self.send_alert(cor, strategy)
        if results[:3] == ['P', 'P', 'P']:
            strategy = 'Sequencia de Pretos'
            self.direction_color = ['V']
            cor = 'VERMELHO 🔴'
            self.send_alert(cor, strategy)
        
        if numeros[3] == '6':
            strategy = 'Numero 5'
            self.direction_color = ['V']
            cor = 'VERMELHO 🔴'
            if self.analisar:
                self.send_alert(cor, strategy)
            

        if results[:3] == ['V', 'V', 'V']:
            strategy = 'Sequencia de Vermelhos'
            self.direction_color = ['P']
            cor = 'PRETO ⚫'
            if self.analisar:
                self.send_alert(cor, strategy)
            
        
        


bot = Bot()
bot.start()
