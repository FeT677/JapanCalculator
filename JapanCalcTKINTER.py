import customtkinter as ctk 
from datetime import datetime
import requests 
from bs4 import BeautifulSoup
from lxml import etree
from tkinter import BooleanVar
from PIL import Image

ctk.set_default_color_theme("blue")

#ввод основных переменных
def set_variables():
    #Для фрейса CTkFrame (основные данные необходимые для расчетов)
    global motor_volume, horse_power, current_year, current_month, vehicle_year, vehicle_month, yen_swift_rate, euro_rate, yen_central_bank_rate
    motor_volume = None
    horse_power = None
    current_year = None
    current_month = None
    vehicle_year = None
    vehicle_month = None
    yen_swift_rate = None
    euro_rate = None
    yen_central_bank_rate = None
    

    #Для фрейма CTkFrame2 (подробный отчет при неактивном чекбоксе "Для ЮР лиц") (ДЛЯ ЮР ЛИЦ)
    global auc_vehicle_price, freight, fob, japan_comission, bank_comission, summary_in_jp, summary_in_jp_rub, util_sbor, custom_rate, \
    nds, custom_duty, excise, custom_services, broker_and_glonas, my_commission, take_to_the_bank, customs_charges

    auc_vehicle_price = None 
    freight = None
    fob = None
    japan_comission = None
    bank_comission = None
    summary_in_jp = None
    summary_in_jp_rub = None
    util_sbor = None
    custom_rate = 1
    nds = None
    custom_duty = None
    excise = None
    custom_services = None
    broker_and_glonas = None
    my_commission = None
    take_to_the_bank = None
    customs_charges = None

    #Для фрейма CTkFrame2 (подробный отчет при АКТИВНОМ чекбоксе "Для ЮР лиц")  (ДЛЯ ФИЗ ЛИЦ)
    global fiz_auc_vehicle_price, fiz_freight, fiz_japan_comission, fiz_bank_comission, fiz_summary_in_jp, fiz_summary_in_jp_rub, fiz_util_sbor, fiz_custom_duty, fiz_custom_rate, fiz_custom_services, fiz_sbkts, fiz_svh, \
    fiz_svh_lab_parking, fiz_broker_services, fiz_temp_registrarion, fiz_glonas

    fiz_auc_vehicle_price = None
    fiz_freight = None
    fiz_japan_comission = None
    fiz_bank_comission = None
    fiz_summary_in_jp = None
    fiz_summary_in_jp_rub = None
    fiz_util_sbor = None
    fiz_custom_duty = None
    fiz_custom_rate = None
    fiz_custom_services = None
    fiz_sbkts = None
    fiz_svh = None
    fiz_svh_lab_parking = None
    fiz_broker_services = None
    fiz_temp_registrarion = None
    fiz_glonas = None

    global jp_comission_global
    jp_comission_global = None

set_variables()

#Парсинг сайта ББР банка для получения курса JPY
def bbr_pars():
    url = "https://bbr.ru"
    response = requests.get(url)

    if response.status_code == 200:
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Преобразуем BeautifulSoup объект в объект lxml для использования XPath
        root = etree.HTML(str(soup))
        # Используем новый XPath для извлечения курса покупки йен
        
        result = root.xpath('//*[@id="__next"]/div[1]/main[1]/div[1]/div[3]/div[1]/div[2]/div[4]/div[3]/div[1]/span[1]/text()')
        if result:  # Проверяем, что результат не пуст
            bbr_pars = str(result[0]) 
            bbr_pars = bbr_pars.replace(',', '.')
            return bbr_pars
        else:
            return "XPath не нашел ни одного элемента."

#Парсинг сайта ЦБРФ для получения курса EUR и JPY
def get_exchange_rates():
    url = "https://www.cbr.ru/currency_base/daily/"
    response = requests.get(url)
    response.raise_for_status()  # Проверяем успешность запроса
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'data'})
    exchange_rates = {}
    for row in table.find_all('tr')[1:]:  # Пропускаем заголовок таблицы
        cells = row.find_all('td')
        if len(cells) == 5:
            currency_code = cells[1].text.strip()
            currency_name = cells[3].text.strip()
            exchange_rate = float(cells[4].text.replace(',', '.').strip())
            exchange_rates[currency_code] = {
                'currency_name': currency_name,
                'exchange_rate': exchange_rate
            }
    return exchange_rates.get('EUR', {}).get('exchange_rate'), exchange_rates.get('JPY', {}).get('exchange_rate')

#Автозаполнение полей
def auto_fill():

    current_month_entry.delete(0, ctk.END)
    current_month_entry.insert(0, current_month)
    current_month_entry.configure(state='disabled')

    current_year_entry.delete(0, ctk.END)
    current_year_entry.insert(0, current_year)
    current_year_entry.configure(state='disabled')

    yen_central_bank_rate_entry.delete(0, ctk.END)
    yen_central_bank_rate_entry.insert(0, (round(jpy_rate, 4)))
    yen_central_bank_rate_entry.configure(state='disabled')

    euro_rate_entry.delete(0, ctk.END)
    euro_rate_entry.insert(0, eur_rate)
    euro_rate_entry.configure(state='disabled')

    yen_swift_rate_entry.insert(0,(round(bbr_final_final_pars, 4)))

#Удаление всех виджетов во втором фрейме. Используется в функции смены ЮР/ФИЗ лицо  
def clear_frame():
    for widget in CTkFrame2.winfo_children():
        widget.destroy()   

#Создание полей с информацией под ЮР ЛИЦО      
def legal_checkbox_ON():

    clear_frame()

    global auc_vehicle_price_entry, freight_entry, fob_entry, japan_comission_entry, bank_comission_entry, summary_in_jp_entry, summary_in_jp_rub_entry, \
    util_sbor_entry, custom_rate_entry, nds_entry, custom_duty_entry, excise_entry, custom_services_entry, broker_and_glonas_entry, \
    my_commission_entry, take_to_the_bank_entry, customs_charges_entry, custom_services_entry, broker_plus_glonas_final_entry, broker_plus_glonas_final_label
    
    auc_vehicle_price_lable = ctk.CTkLabel(CTkFrame2, text='Аукционная стоимость')
    auc_vehicle_price_lable.grid(row=1, column=0, padx=10, pady=4, sticky='w')
    auc_vehicle_price_entry = ctk.CTkEntry(CTkFrame2)
    auc_vehicle_price_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')

    freight_lable = ctk.CTkLabel(CTkFrame2, text="Фрахт")
    freight_lable.grid(row=2, column=0, padx=10, pady=4, sticky='w')
    freight_entry = ctk.CTkEntry(CTkFrame2)
    freight_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')

    fob_lable = ctk.CTkLabel(CTkFrame2, text="Фоб")
    fob_lable.grid(row=3, column=0, padx=10, pady=4, sticky='w')
    fob_entry = ctk.CTkEntry(CTkFrame2)
    fob_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')

    japan_comission_lable = ctk.CTkLabel(CTkFrame2, text= f"Комиссия Японии за стоимость")
    japan_comission_lable.grid(row=4, column=0, padx=10, pady=4, sticky='w')
    japan_comission_entry = ctk.CTkEntry(CTkFrame2)
    japan_comission_entry.grid(row=4, column=1, padx=10, pady=4, sticky='w')

    bank_comission_lable = ctk.CTkLabel(CTkFrame2, text='Комиссия банка за переводы')
    bank_comission_lable.grid(row=5, column=0, padx=10, pady=4, sticky='w')
    bank_comission_entry = ctk.CTkEntry(CTkFrame2)
    bank_comission_entry.grid(row=5, column=1, padx=10, pady=4, sticky='w')

    summary_in_jp_lable = ctk.CTkLabel(CTkFrame2, text='ИТОГО В ЯПОНИЮ (JPY)')
    summary_in_jp_lable.grid(row=6, column=0, padx=10, pady=4, sticky='w')
    summary_in_jp_entry = ctk.CTkEntry(CTkFrame2)
    summary_in_jp_entry.grid(row=6, column=1, padx=10, pady=4, sticky='w')

    summary_in_jp_rub_lable = ctk.CTkLabel(CTkFrame2, text='ИТОГО В ЯПОНИЮ (RUB)')
    summary_in_jp_rub_lable.grid(row=7, column=0, padx=10, pady=4, sticky='w')
    summary_in_jp_rub_entry = ctk.CTkEntry(CTkFrame2)
    summary_in_jp_rub_entry.grid(row=7, column=1, padx=10, pady=4, sticky='w')

    util_sbor_lable = ctk.CTkLabel(CTkFrame2, text='Утилизационный сбор')
    util_sbor_lable.grid(row=1, column=2, padx=10, pady=4, sticky='w')
    util_sbor_entry = ctk.CTkEntry(CTkFrame2)
    util_sbor_entry.grid(row=1, column=3, padx=10, pady=4, sticky='w')
    
    custom_rate_lable = ctk.CTkLabel(CTkFrame2, text='Таможенная ставка')
    custom_rate_lable.grid(row=3, column=2, padx=10, pady=4, sticky='w')
    custom_rate_entry = ctk.CTkEntry(CTkFrame2)
    custom_rate_entry.grid(row=3, column=3, padx=10, pady=4)

    nds_lable = ctk.CTkLabel(CTkFrame2, text='НДС')
    nds_lable.grid(row=6, column=2, padx=10, pady=4, sticky='w')
    nds_entry = ctk.CTkEntry(CTkFrame2)
    nds_entry.grid(row=6, column=3, padx=10, pady=4, sticky='w')

    custom_duty_lable = ctk.CTkLabel(CTkFrame2, text='Пошлина')
    custom_duty_lable.grid(row=2, column=2, padx=10, pady=4, sticky='w')
    custom_duty_entry = ctk.CTkEntry(CTkFrame2)
    custom_duty_entry.grid(row=2, column=3, padx=10, pady=4, sticky='w')

    excise_lable = ctk.CTkLabel(CTkFrame2, text='Акциз')
    excise_lable.grid(row=5, column=2, padx=10, pady=4, sticky='w')
    excise_entry = ctk.CTkEntry(CTkFrame2)
    excise_entry.grid(row=5, column=3, padx=10, pady=4, sticky='w')

    custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Таможенное оформление')
    custom_services_lable.grid(row=4, column=2, padx=10, pady=4, sticky='w')
    custom_services_entry = ctk.CTkEntry(CTkFrame2)
    custom_services_entry.grid(row=4, column=3, padx=10, pady=4, sticky='w')

    broker_and_glonas_lable = ctk.CTkLabel(CTkFrame2, text='Брокер+Глонас')
    broker_and_glonas_lable.grid(row=7, column=2, padx=10, pady=4, sticky='w')
    broker_and_glonas_entry = ctk.CTkEntry(CTkFrame2)
    broker_and_glonas_entry.grid(row=7, column=3, padx=10, pady=4, sticky='w')
    
    payment_stages_lable = ctk.CTkLabel(CTkFrame2, text='ЭТАПЫ ОПЛАТЫ')
    payment_stages_lable.grid(row=8, column=0, columnspan=2, sticky='we', padx=10, pady=4)

    my_commission_lable = ctk.CTkLabel(CTkFrame2, text="Моя комиссия")
    my_commission_lable.grid(row=9, column=0, padx=10, pady=4, sticky='w')
    my_commission_entry = ctk.CTkEntry(CTkFrame2)
    my_commission_entry.grid(row=9, column=1, padx=10, pady=4, sticky='w')
    
    take_to_the_bank_lable = ctk.CTkLabel(CTkFrame2, text='Взять с собой в банк')
    take_to_the_bank_lable.grid(row=10, column=0, padx=10, pady=4, sticky='w')
    take_to_the_bank_entry = ctk.CTkEntry(CTkFrame2)
    take_to_the_bank_entry.grid(row=10, column=1, padx=10, pady=4, sticky='w')

    customs_charges_lable = ctk.CTkLabel(CTkFrame2, text='Оплата таможни')
    customs_charges_lable.grid(row=11, column=0, padx=10, pady=4, sticky='w')
    customs_charges_entry = ctk.CTkEntry(CTkFrame2)
    customs_charges_entry.grid(row=11, column=1, padx=10, pady=4, sticky='w')

    broker_plus_glonas_final_label = ctk.CTkLabel(CTkFrame2, text='Брокер+Глонас')
    broker_plus_glonas_final_label.grid(row=12, column=0, padx=10, pady=4, sticky='w')
    broker_plus_glonas_final_entry = ctk.CTkEntry(CTkFrame2)
    broker_plus_glonas_final_entry.grid(row=12, column=1, padx=10, pady=4, sticky='w')

#Создание полей с информацией под ФИЗ ЛИЦО
def legal_checkbox_OFF():

    clear_frame()

    global fiz_auc_vehicle_price_entry, fiz_freight_entry, fiz_fob_entry, fiz_japan_comission_entry, fiz_bank_comission_entry, fiz_summary_in_jp_entry, fiz_summary_in_jp_rub_entry, fiz_util_sbot_entry, \
    fiz_custom_duty_entry, fiz_custom_rate_entry, fiz_custom_services_entry, fiz_sbkts_entry, fiz_svh_entry, fiz_svh_lab_parking_entry, fiz_broker_services_entry, fiz_temp_registrarion_entry, fiz_glonas_entry, \
    fiz_my_commission_entry, fiz_take_to_the_bank_entry, fiz_customs_charges_entry, fiz_broker_entry

    fiz_auc_vehicle_price_lable = ctk.CTkLabel(CTkFrame2, text='Аукционная стоимость')
    fiz_auc_vehicle_price_lable.grid(row=1, column=0, padx=10, pady=4, sticky='w')
    fiz_auc_vehicle_price_entry = ctk.CTkEntry(CTkFrame2)
    fiz_auc_vehicle_price_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')

    fiz_freight_lable = ctk.CTkLabel(CTkFrame2, text="Фрахт")
    fiz_freight_lable.grid(row=2, column=0, padx=10, pady=4, sticky='w')
    fiz_freight_entry = ctk.CTkEntry(CTkFrame2)
    fiz_freight_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')

    fiz_fob_lable = ctk.CTkLabel(CTkFrame2, text="Фоб")
    fiz_fob_lable.grid(row=3, column=0, padx=10, pady=4, sticky='w')
    fiz_fob_entry = ctk.CTkEntry(CTkFrame2)
    fiz_fob_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')

    fiz_japan_comission_lable = ctk.CTkLabel(CTkFrame2, text= f"Комиссия Японии за стоимость")
    fiz_japan_comission_lable.grid(row=4, column=0, padx=10, pady=4, sticky='w')
    fiz_japan_comission_entry = ctk.CTkEntry(CTkFrame2)
    fiz_japan_comission_entry.grid(row=4, column=1, padx=10, pady=4, sticky='w')

    fiz_bank_comission_lable = ctk.CTkLabel(CTkFrame2, text='Комиссия банка за переводы')
    fiz_bank_comission_lable.grid(row=5, column=0, padx=10, pady=4, sticky='w')
    fiz_bank_comission_entry = ctk.CTkEntry(CTkFrame2)
    fiz_bank_comission_entry.grid(row=5, column=1, padx=10, pady=4, sticky='w')

    fiz_summary_in_jp_lable = ctk.CTkLabel(CTkFrame2, text='ИТОГО В ЯПОНИЮ (JPY)')
    fiz_summary_in_jp_lable.grid(row=6, column=0, padx=10, pady=4, sticky='w')
    fiz_summary_in_jp_entry = ctk.CTkEntry(CTkFrame2)
    fiz_summary_in_jp_entry.grid(row=6, column=1, padx=10, pady=4, sticky='w')

    fiz_summary_in_jp_rub_lable = ctk.CTkLabel(CTkFrame2, text='ИТОГО В ЯПОНИЮ (RUB)')
    fiz_summary_in_jp_rub_lable.grid(row=7, column=0, padx=10, pady=4, sticky='w')
    fiz_summary_in_jp_rub_entry = ctk.CTkEntry(CTkFrame2)
    fiz_summary_in_jp_rub_entry.grid(row=7, column=1, padx=10, pady=4, sticky='w')

    fiz_util_sbor_lable = ctk.CTkLabel(CTkFrame2, text='Утилизационный сбор')
    fiz_util_sbor_lable.grid(row=1, column=2, padx=10, pady=4, sticky='w')
    fiz_util_sbot_entry = ctk.CTkEntry(CTkFrame2)
    fiz_util_sbot_entry.grid(row=1, column=3, padx=10, pady=4, sticky='w')

    fiz_custom_duty_lable = ctk.CTkLabel(CTkFrame2, text='Пошлина')
    fiz_custom_duty_lable.grid(row=2, column=2, padx=10, pady=4, sticky='w')
    fiz_custom_duty_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_duty_entry.grid(row=2, column=3, padx=10, pady=4, sticky='w')

    fiz_custom_rate_lable = ctk.CTkLabel(CTkFrame2, text='Таможенная ставка')
    fiz_custom_rate_lable.grid(row=3, column=2, padx=10, pady=4, sticky='w')
    fiz_custom_rate_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_rate_entry.grid(row=3, column=3, padx=10, pady=4, sticky='w')

    fiz_custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Таможенное оформление')
    fiz_custom_services_lable.grid(row=4, column=2, padx=10, pady=4, sticky='w')
    fiz_custom_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_services_entry.grid(row=4, column=3, padx=10, pady=4, sticky='w')

    fiz_sbkts_lable = ctk.CTkLabel(CTkFrame2, text='СБКТС')
    fiz_sbkts_lable.grid(row=5, column=2, padx=10, pady=4, sticky='w')
    fiz_sbkts_entry = ctk.CTkEntry(CTkFrame2)
    fiz_sbkts_entry.grid(row=5, column=3, padx=10, pady=4, sticky='w')

    fiz_svh_lable = ctk.CTkLabel(CTkFrame2, text='СВХ')
    fiz_svh_lable.grid(row=6, column=2, padx=10, pady=4, sticky='w')
    fiz_svh_entry = ctk.CTkEntry(CTkFrame2)
    fiz_svh_entry.grid(row=6, column=3, padx=10, pady=4, sticky='w')

    fiz_svh_lab_parking_lable = ctk.CTkLabel(CTkFrame2, text='СВХ-Лаб.-Стоянка')
    fiz_svh_lab_parking_lable.grid(row=7, column=2, padx=10, pady=4, sticky='w')
    fiz_svh_lab_parking_entry = ctk.CTkEntry(CTkFrame2)
    fiz_svh_lab_parking_entry.grid(row=7, column=3, padx=10, pady=4, sticky='w')

    fiz_broker_services_lable= ctk.CTkLabel(CTkFrame2, text='Услуги брокера')
    fiz_broker_services_lable.grid(row=8, column=2, padx=10, pady=4, sticky='w')
    fiz_broker_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_broker_services_entry.grid(row=8, column=3, padx=10, pady=4, sticky='w')

    fiz_temp_registrarion_lable = ctk.CTkLabel(CTkFrame2, text='Временная регистрация')
    fiz_temp_registrarion_lable.grid(row=9, column=2, padx=10, pady=4, sticky='w')
    fiz_temp_registrarion_entry = ctk.CTkEntry(CTkFrame2)
    fiz_temp_registrarion_entry.grid(row=9, column=3, padx=10, pady=4, sticky='w')

    fiz_glonas_lable = ctk.CTkLabel(CTkFrame2, text='Глонас для физ')
    fiz_glonas_lable.grid(row=10, column=2, padx=10, pady=4, sticky='w')
    fiz_glonas_entry = ctk.CTkEntry(CTkFrame2)
    fiz_glonas_entry.grid(row=10, column=3, padx=10, pady=4, sticky='w')

    fiz_payment_stages_lable = ctk.CTkLabel(CTkFrame2, text='ЭТАПЫ ОПЛАТЫ')
    fiz_payment_stages_lable.grid(row=8, column=0, columnspan=2, padx=10, pady=4, sticky='we')

    fiz_my_commission_lable = ctk.CTkLabel(CTkFrame2, text='Моя комиссия')
    fiz_my_commission_lable.grid(row=9, column=0, padx=10, pady=4, sticky='w')
    fiz_my_commission_entry = ctk.CTkEntry(CTkFrame2)
    fiz_my_commission_entry.grid(row=9, column=1, padx=10, pady=4, sticky='w')

    fiz_take_to_the_bank_label = ctk.CTkLabel(CTkFrame2, text='Взять с собой в банк')
    fiz_take_to_the_bank_label.grid(row=10, column=0, padx=10, pady=4, sticky='w')
    fiz_take_to_the_bank_entry = ctk.CTkEntry(CTkFrame2)
    fiz_take_to_the_bank_entry.grid(row=10, column=1, padx=10, pady=4, sticky='w')

    fiz_customs_charges_lable = ctk.CTkLabel(CTkFrame2, text='Оплата таможни')
    fiz_customs_charges_lable.grid(row=11, column=0, padx=10, pady=4, sticky='w')
    fiz_customs_charges_entry = ctk.CTkEntry(CTkFrame2)
    fiz_customs_charges_entry.grid(row=11, column=1, padx=10, pady=4, sticky='w')

    fiz_broker_label = ctk.CTkLabel(CTkFrame2, text='Оплата брокеру')
    fiz_broker_label.grid(row=12, column=0, padx=10, pady=4, sticky='w')
    fiz_broker_entry = ctk.CTkEntry(CTkFrame2)
    fiz_broker_entry.grid(row=12, column=1, padx=10, pady=4, sticky='w')

#Что делать при нажатии чекбокса ЮР ЛИЦО/ФИЗ ЛИЦО    
def on_legal_checkbox():

    if legal_check_var.get():
        legal_checkbox_ON()
    else:
        legal_checkbox_OFF() 

#определение абстракного возраста авто для расчетов на юр лицо
def legal_age_rank_check():

    global legal_age_rank
    current_date_in_months = (int(current_year_entry.get())) * 12 + int(current_month_entry.get())
    vehicle_date_in_months = (int(vehicle_year_entry.get())) * 12 + int(vehicle_month_entry.get())

    if (current_date_in_months - 82) > vehicle_date_in_months:
        legal_age_rank = 2016
    elif (current_date_in_months - 35) < vehicle_date_in_months:
        legal_age_rank =  2023
    else:
        legal_age_rank = 2018

#определение абстракного возраста авто для расчетов на физ лицо
def fiz_age_rank_check():
    global fiz_age_rank
    current_date_in_months = (int(current_year_entry.get())) * 12 + int(current_month_entry.get())
    vehicle_date_in_months = (int(vehicle_year_entry.get())) * 12 + int(vehicle_month_entry.get())
    
    if (current_date_in_months - 58) > vehicle_date_in_months:
        fiz_age_rank = 2015
    elif (current_date_in_months - 35) < vehicle_date_in_months:
        fiz_age_rank = 2023
    else:
        fiz_age_rank = 2020
    
# Функция вычисления комиссии Японского брокера за цену на аукционе 
def japan_comission_for_the_price():
    global jp_comission_global
    vehicle_auc_price_entryed = int(vehicle_auc_price_entry.get())

    if vehicle_auc_price_entryed > 2999000:
        jp_comission_global = 40000
    elif vehicle_auc_price_entryed > 1999000:
        jp_comission_global = 30000
    elif vehicle_auc_price_entryed > 999000:
        jp_comission_global = 20000
    else:
        jp_comission_global = 0
    
    if legal_check_var.get():
        japan_comission_entry.delete(0, ctk.END)
        japan_comission_entry.insert(0, f'{jp_comission_global}')
    else:
        fiz_japan_comission_entry.delete(0, ctk.END)
        fiz_japan_comission_entry.insert(0, f'{jp_comission_global}')

#Функция вычисления таможенной ставки для ЮР лиц
def calculate_legal_custom_rate(): 

    vehicle_month_entryed = int(vehicle_month_entry.get())
    vehicle_year_entryed = int(vehicle_year_entry.get())
    current_month_entryed = int(current_month_entry.get())
    current_year_entryed = int(current_year_entry.get())
    engine_volume = int(motor_volume_entry.get())
    if legal_age_rank < 2017:
        if engine_volume < 1100:
            custom_ratee = 1.4
        elif engine_volume < 1600:
            custom_ratee = 1.5
        else:
            custom_ratee = 1.6
    else:
        custom_ratee = 0

    custom_rate_entry.delete(0, ctk.END)
    custom_rate_entry.insert(0, (custom_ratee))

#Функция вычисления акциза
def calculate_excise():
    horse_power = int(horse_power_entry.get())

    if horse_power < 150:
        if horse_power > 91:
            excice = (55 * horse_power)
        else:
            excice =  0
    else:
        excice =  (531 * horse_power)
    
    excise_entry.delete(0, ctk.END)
    excise_entry.insert(0, (excice))

#Функция вычисления таможенного платежа для физ лиц
def calculate_duty_for_fiz_entity():
    car_price_yen = int(vehicle_auc_price_entry.get())
    engine_volume = int(motor_volume_entry.get())
    utilization_fee = int(fiz_util_sbot_entry.get())
    custom_clearance_cost = int(fiz_custom_services_entry.get())
    yen_rate = float(yen_central_bank_rate_entry.get())
    euro_rate = float(euro_rate_entry.get())
    custom_duty = float(fiz_custom_rate_entry.get())

    if fiz_age_rank < 2021:
        if car_price_yen < 300000:
            additional_cost = 775
        elif car_price_yen < 700000:
            additional_cost = 1500
        elif car_price_yen < 1980000:
            additional_cost = 3100
        else:
            additional_cost = 8500
        
        total_cost = ((engine_volume * custom_duty) * euro_rate) + utilization_fee + additional_cost
    else:
        cost_yen_plus_140 = car_price_yen + 140000
        multiplier = 0.54 if car_price_yen < 1300000 else 0.48
        
        if (cost_yen_plus_140 * (multiplier * yen_rate)) < (engine_volume * ((2.5 if car_price_yen < 1300000 else 3.5) * euro_rate)):
            total_cost = (engine_volume * ((2.5 if car_price_yen < 1300000 else 3.5) * euro_rate)) + custom_clearance_cost + utilization_fee
        else:
            total_cost = (cost_yen_plus_140 * (multiplier * yen_rate)) + custom_clearance_cost + utilization_fee

    fiz_custom_duty_entry.delete(0, ctk.END)
    fiz_custom_duty_entry.insert(0, total_cost)

#Функция вычисления таможенного платежа для юр лиц
def calculate_duty_for_legal_entity():
    customs_rate = float(custom_rate_entry.get())
    engine_volume = int(motor_volume_entry.get())
    euro_exchange_rate = float(euro_rate_entry.get())
    yen_exchange_rate = float(yen_central_bank_rate_entry.get())
    car_price = int(vehicle_auc_price_entry.get())
    legal_age_rank_check()

    
    if legal_age_rank < 2021:
        if legal_age_rank < 2017:
            returns = customs_rate * engine_volume * euro_exchange_rate
        else:
            cost1 = 0.36 * engine_volume * euro_exchange_rate
            cost2 = (car_price + 175000) * yen_exchange_rate * 0.2
            returns = max(cost1, cost2)
    else:
        returns = "Нельзя <3лет"

    custom_duty_entry.delete(0, ctk.END)
    custom_duty_entry.insert(0, returns)   

#Функция вычисления утилизационного сбора для физ и для юр
def calculate_util_sbor():
    motor_volume = float(motor_volume_entry.get())
    if legal_check_var.get():
        if motor_volume > 2000:
            result = 1279
        elif motor_volume > 1000:
            result = 529000
        else:
            result = 207000
        util_sbor_entry.delete(0, ctk.END)
        util_sbor_entry.insert(0, result)
    else:
        vehicle_month_entryed = int(vehicle_month_entry.get())
        vehicle_year_entryed = int(vehicle_year_entry.get())
        current_month_entryed = int(current_month_entry.get())
        current_year_entryed = int(current_year_entry.get())
        vehicle_date_in_months = (vehicle_year_entryed * 12) + vehicle_month_entryed
        current_date_in_months = (current_year_entryed * 12) + current_month_entryed

        b41 = current_date_in_months
        b42 = vehicle_date_in_months

        if (b41 - 58) > b42:
            yearr = 2015
        elif (b41 - 35) < b42:
            yearr = 2023
        else:
            yearr = 2020
        
        if yearr < 2021:
            result = 5200
        else:
            result = 3400

        fiz_util_sbot_entry.delete(0, ctk.END)
        fiz_util_sbot_entry.insert(0, result)

#Функция вычисления комисси банка за переводы
def calculate_bank_fee():
    def safe_float(entry):
        value = entry.get().strip()
        return float(value) if value else 0.0

    if legal_check_var.get():
        # Получаем значения до любых изменений
        freight_value = freight_entry.get().strip()
        fob_value = fob_entry.get().strip()
        japan_comission_value = japan_comission_entry.get().strip()

        # Преобразуем значения в числа, если возможно
        freightt = float(freight_value) if freight_value else 0.0
        fobb = float(fob_value) if fob_value else 0.0
        japan_comission_entryy = float(japan_comission_value) if japan_comission_value else 0.0

        payment_amount_yen = float(vehicle_auc_price_entry.get()) + \
                             freightt + \
                             fobb + \
                             japan_comission_entryy
        fee = (payment_amount_yen * 0.008 + 4500) * safe_float(yen_swift_rate_entry)
        fee_final = fee if fee > 7400 else 7400
        
        bank_comission_entry.delete(0, ctk.END)
        bank_comission_entry.insert(0, fee_final)
    else:
        # Получаем значения до любых изменений
        fiz_freight_value = fiz_freight_entry.get().strip()
        fiz_fob_value = fiz_fob_entry.get().strip()
        fiz_japan_comission_value = fiz_japan_comission_entry.get().strip()

        # Преобразуем значения в числа, если возможно
        fiz_freightt = float(fiz_freight_value) if fiz_freight_value else 0.0
        fiz_fobb = float(fiz_fob_value) if fiz_fob_value else 0.0
        fiz_japan_comission_entryy = float(fiz_japan_comission_value) if fiz_japan_comission_value else 0.0

        payment_amount_yen = float(vehicle_auc_price_entry.get()) + \
                             fiz_freightt + \
                             fiz_fobb + \
                             fiz_japan_comission_entryy
        fee = (payment_amount_yen * 0.008 + 4500) * safe_float(yen_swift_rate_entry)
        fee_final = fee if fee > 7400 else 7400
        
        fiz_bank_comission_entry.delete(0, ctk.END)
        fiz_bank_comission_entry.insert(0, fee_final)

#Функция вычисления НДС для ЮР лиц
def calculate_nds():
    total_cost = 0.555
    car_price_yen = vehicle_auc_price_entry.get()
    yen_rate = yen_central_bank_rate_entry.get()
    custom_duty = custom_duty_entry.get()
    excise = excise_entry.get()
    custom_clearancee = custom_services_entry.get()
    
    if legal_check_var.get():
        total_cost = (((int(car_price_yen) + 175000) * float(yen_rate)) + int(float(custom_duty)) + int(excise) + int(custom_clearancee)) * 0.2

        nds_entry.delete(0, ctk.END)
        nds_entry.insert(0, total_cost) 

#Функция вычисления стоимости таможенного оформления
def custom_clearance():
    clearance = 1
    price = int(vehicle_auc_price_entry.get())
    if legal_check_var.get():
        if price < 300000:
            clearance = 775
        elif price < 700000:
            clearance = 1550
        elif price < 1800000:
            clearance = 3100
        else:
            clearance = 8530
        custom_services_entry.delete(0, ctk.END)
        custom_services_entry.insert(0, clearance)
    else:
        if price < 300000:
            clearance = 775
        elif price < 700000:
            clearance = 1550
        elif price < 1800000:
            clearance = 3100
        else:
            clearance = 8530
        fiz_custom_services_entry.delete(0, ctk.END)
        fiz_custom_services_entry.insert(0, int(clearance))

space = '\u2008\u2008\u2008\u2008\u2008\u2008\u2008'
current_month = datetime.now().month
current_year = datetime.now().year

vehicle_month_entryed = None
vehicle_year_entryed = None
current_month_entryed = None
current_year_entryed = None

bbr_final_pars = (bbr_pars())
bbr_final_final_pars = (float(bbr_final_pars)/100)
eur_rate, jpy_rate = get_exchange_rates()
jpy_rate = float(jpy_rate/100)

window = ctk.CTk(fg_color='#343535')
window.title('РАСЧЕТ СТОИМОСТИ ПОКУПКИ/ТАМОЖНИ/ДОСТАВКИ АВТОМОБИЛЯ ИЗ ЯПОНИИ')

window.geometry("756x743")  
window.resizable(False, False)

#Чисто декоративный фрейм для создания цветной окантовки
CTkFrame3 = ctk.CTkFrame(window)
CTkFrame3.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

#Размещаем в этот фрейм джипежку
image_label = ctk.CTkLabel(CTkFrame3, text="")
image_label.place(x=0, y=0, relwidth=1, relheight=1)

#Фрейм для ввода основных переменных
CTkFrame = ctk.CTkFrame(CTkFrame3,fg_color='#3D3D3D')
CTkFrame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

#Фрейм для подробного отчета
CTkFrame2 = ctk.CTkFrame(CTkFrame3,fg_color='#3D3D3D')  
CTkFrame2.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', rowspan=2)

legal_check_var = BooleanVar()
legal_checkbox = ctk.CTkCheckBox(CTkFrame, text="РАСЧЕТ ДЛЯ ЮРИДИЧЕСКИХ ЛИЦ", variable=legal_check_var, command=on_legal_checkbox)
legal_checkbox.grid(row=4, column=2, columnspan=2, padx=10, pady=4, sticky='w')

vehicle_auc_price_CTkLabel = ctk.CTkLabel(CTkFrame, text=f"АУКЦИОННАЯ СТОИМОСТЬ{space}")
vehicle_auc_price_CTkLabel.grid(row=0, column=0, padx=10, pady=2, sticky='w')
vehicle_auc_price_entry = ctk.CTkEntry(CTkFrame)
vehicle_auc_price_entry.grid(row=0, column=1, padx=10, pady=4, sticky='w')

motor_volume_CTkLabel = ctk.CTkLabel(CTkFrame, text="ОБЪЕМ МОТОРА")
motor_volume_CTkLabel.grid(row=1, column=0, padx=10, pady=4, sticky='w')
motor_volume_entry = ctk.CTkEntry(CTkFrame)
motor_volume_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')

horse_power_CTkLabel = ctk.CTkLabel(CTkFrame, text="ЛОШАДИНЫХ СИЛ")
horse_power_CTkLabel.grid(row=2, column=0, padx=10, pady=4, sticky='w')
horse_power_entry = ctk.CTkEntry(CTkFrame)
horse_power_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')

years = [
    "2001", "2002", "2003", "2004", "2005", "2006",
    "2007", "2008", "2009", "2010", "2011", "2012",
    "2013", "2014", "2015", "2016", "2017", "2018",
    "2019", "2020", "2021", "2022", "2023", "2024",
    "2025", "2026", "2027", "2028", "2029", "2030",
    "2031", "2032",
]
months = [
    "1", "2", "3", "4", "5", "6",
    "7", "8", "9", "10", "11", "12"
]

year_var = ctk.StringVar(window)
month_var = ctk.StringVar(window)

current_year_CTkLabel = ctk.CTkLabel(CTkFrame, text='ТЕКУЩИЙ ГОД')
current_year_CTkLabel.grid(row=3, column=0, padx=10, pady=4, sticky='w')
current_year_entry = ctk.CTkEntry(CTkFrame)
current_year_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')

current_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="ТЕКУЩИЙ МЕСЯЦ")
current_month_CTkLabel.grid(row=4, column=0, padx=10, pady=4, sticky='w')
current_month_entry = ctk.CTkEntry(CTkFrame)
current_month_entry.grid(row=4, column=1, padx=10, pady=4, sticky='w')

vehicle_year_CTkLabel = ctk.CTkLabel(CTkFrame, text="ГОД ВЫПУСКА АВТО")
vehicle_year_CTkLabel.grid(row=5, column=0, padx=10, pady=4, sticky='w')
vehicle_year_entry = ctk.CTkComboBox(CTkFrame, values=years, state="readonly", variable=year_var)
vehicle_year_entry.grid(row=5, column=1)
vehicle_year_entry["state"] = "readonly"

vehicle_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="МЕСЯЦ ВЫПУСКА АВТО")
vehicle_month_CTkLabel.grid(row=6, column=0, padx=10, pady=4, sticky='w')
vehicle_month_entry = ctk.CTkComboBox(CTkFrame, values=months, state="readonly", variable=month_var)
vehicle_month_entry.grid(row=6, column=1)
vehicle_month_entry["state"] = "readonly"

yen_swift_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="КУРС JPY В BBR БАНКЕ")
yen_swift_rate_CTkLabel.grid(row=0, column=2, padx=10, pady=4, sticky='w')
yen_swift_rate_entry = ctk.CTkEntry(CTkFrame)
yen_swift_rate_entry.grid(row=0, column=3, padx=10, pady=4, sticky='w')

euro_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="КУРС EUR ПО ЦБ")
euro_rate_CTkLabel.grid(row=1, column=2, padx=10, pady=4, sticky='w')
euro_rate_entry = ctk.CTkEntry(CTkFrame)
euro_rate_entry.grid(row=1, column=3, padx=10, pady=4, sticky='w')

yen_central_bank_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="КУРС JPY ПО ЦБ")
yen_central_bank_rate_CTkLabel.grid(row=2, column=2, padx=10, pady=4, sticky='w')
yen_central_bank_rate_entry = ctk.CTkEntry(CTkFrame)
yen_central_bank_rate_entry.grid(row=2, column=3, padx=10, pady=4, sticky='w')

all_summary_Label = ctk.CTkLabel(CTkFrame, text="Итого, ПРИМЕРНАЯ стоимость:")
all_summary_Label.grid(row=5, column=2, columnspan = 2, sticky = 'we')
all_summary_Label["state"] = "readonly"

all_summary_entry = ctk.CTkEntry(CTkFrame)
all_summary_entry.grid(row=6, column=2, columnspan = 2, sticky = 'we')
all_summary_entry["state"] = "readonly"

#Автозаполнение
auto_fill()

#По дефолту задаем расчет на ФИЗ ЛИЦО
legal_checkbox_OFF()

#Расчет таможенной ставки для ФИЗИЧЕСКИХ лиц
def fiz_calculate_custom_rate():
    euro_exchange_rate = float(euro_rate_entry.get())
    yen_exchange_rate = float(yen_central_bank_rate_entry.get())
    engine_volume = int(motor_volume_entry.get())
    car_price = int(vehicle_auc_price_entry.get())
    fiz_rate = 555
    if fiz_age_rank < 2021:
        if fiz_age_rank < 2019:
            if engine_volume < 2300:
                if engine_volume < 1900:
                    if engine_volume < 1600:
                        if engine_volume < 1100:
                            fiz_rate =  3
                        else:
                            fiz_rate = 3.2
                    else:
                        fiz_rate = 3.5
                else:
                    fiz_rate = 4
            else:
                fiz_rate = 5
        else:
            if engine_volume < 2300:
                if engine_volume < 1900:
                    if engine_volume < 1600:
                        if engine_volume < 1100:
                            fiz_rate = 1.5
                        else:
                            fiz_rate = 1.7
                    else:
                        fiz_rate = 2.5
                else:
                    fiz_rate = 2.7
            else:
                fiz_rate = 3
    else:
        if ((car_price + 140000) * (0.54 if car_price < 1300000 else 0.48) * yen_exchange_rate) < (engine_volume * (2.5 if car_price < 1300000 else 3.5) * euro_exchange_rate):
            fiz_rate = 2.5 if car_price < 1300000 else 3.5
        else:
            fiz_rate = 0.54 if car_price < 1300000 else 0.48

    fiz_custom_rate_entry.delete(0, ctk.END)
    fiz_custom_rate_entry.insert(0, fiz_rate)

#Комманда для кнопки которая выводит все расчеты
def calculate_everything():
    if legal_check_var.get():
        legal_checkbox_ON()
        legal_age_rank_check()
        auc_vehicle_price = int(vehicle_auc_price_entry.get())
        auc_vehicle_price_entry.delete(0, ctk.END)
        auc_vehicle_price_entry.insert(0, auc_vehicle_price)
        freight_entry.delete(0, ctk.END)
        freight_entry.insert(0, '60000')
        fob_entry.delete(0, ctk.END)
        fob_entry.insert(0, '60000')
        broker_and_glonas_entry.delete(0, ctk.END)
        broker_and_glonas_entry.insert(0, '100000')
        my_commission_entry.delete(0, ctk.END)
        my_commission_entry.insert(0, '30000')
        japan_comission_for_the_price()
        calculate_legal_custom_rate()
        calculate_excise()
        calculate_bank_fee()
        summary_in_jpy = auc_vehicle_price + int(fob_entry.get()) + int(freight_entry.get()) + int(japan_comission_entry.get())
        summary_in_jp_entry.delete(0, ctk.END)
        summary_in_jp_entry.insert (0, f'{summary_in_jpy}')
        summary_in_jp_rub_entry.delete(0, ctk.END)
        ggg = round(((int(summary_in_jpy) * float(yen_swift_rate_entry.get()))), 2)
        summary_in_jp_rub_entry.insert(0, ggg)
        custom_clearance()
        calculate_util_sbor()
        calculate_duty_for_legal_entity()
        calculate_nds()

        take_to_the_bank_final = (summary_in_jpy * float(yen_swift_rate_entry.get())) + int(bank_comission_entry.get())
        customs_charges_final = float(custom_duty_entry.get()) + float(nds_entry.get()) + int(excise_entry.get()) + int(custom_services_entry.get()) + int(util_sbor_entry.get())
        print(customs_charges_final)
        broker_and_glonass = int(broker_and_glonas_entry.get())
        print(broker_and_glonass)

        take_to_the_bank_entry.delete(0, ctk.END)
        take_to_the_bank_entry.insert(0, take_to_the_bank_final)

        customs_charges_entry.delete(0, ctk.END)
        customs_charges_entry.insert(0, customs_charges_final)

        broker_plus_glonas_final_entry.delete(0, ctk.END)
        broker_plus_glonas_final_entry.insert(0, broker_and_glonass)

        all_summary = int(my_commission_entry.get()) + take_to_the_bank_final + customs_charges_final + broker_and_glonass
        all_summary_entry.delete(0, ctk.END)
        all_summary_entry["state"] = "readonly"
        all_summary_entry.insert(0, f'{space}{space}{round((all_summary), 2)} российских рубля')



    else:
        legal_checkbox_OFF()
        fiz_age_rank_check()
        fiz_auc_vehicle_price = int(vehicle_auc_price_entry.get())
        fiz_auc_vehicle_price_entry.delete(0, ctk.END)
        fiz_auc_vehicle_price_entry.insert(0, fiz_auc_vehicle_price)
        fiz_freight_entry.delete(0, ctk.END)
        fiz_freight_entry.insert(0, '60000')
        fiz_fob_entry.delete(0, ctk.END)
        fiz_fob_entry.insert(0, '60000')
        fiz_my_commission_entry.delete(0, ctk.END)
        fiz_my_commission_entry.insert(0, '30000')
        japan_comission_for_the_price()
        fiz_calculate_custom_rate()
        calculate_bank_fee()
        fiz_summary_in_jpy = fiz_auc_vehicle_price + int(fiz_fob_entry.get()) + int(fiz_freight_entry.get()) + int(fiz_japan_comission_entry.get())
        fiz_summary_in_jp_entry.delete(0, ctk.END)
        fiz_summary_in_jp_entry.insert(0, f'{fiz_summary_in_jpy}')
        fiz_summary_in_jp_rub_entry.delete(0, ctk.END)
        fiz_ggg = round(((int(fiz_summary_in_jpy) * float(yen_swift_rate_entry.get()))), 2)
        fiz_summary_in_jp_rub_entry.insert(0, fiz_ggg)
        custom_clearance()
        calculate_util_sbor()
        calculate_duty_for_fiz_entity()
        fiz_sbkts_entry.delete(0, ctk.END)
        fiz_sbkts_entry.insert(0, '25000')
        fiz_svh_entry.delete(0, ctk.END)
        fiz_svh_entry.insert(0, '30000')
        fiz_svh_lab_parking_entry.delete(0, ctk.END)
        fiz_svh_lab_parking_entry.insert(0, '5000')
        fiz_broker_services_entry.delete(0, ctk.END)
        fiz_broker_services_entry.insert(0, '10000')
        fiz_temp_registrarion_entry.delete(0, ctk.END)
        fiz_temp_registrarion_entry.insert(0, '10000')
        fiz_glonas_entry.insert(0, '0')

        my_commission_final = int(fiz_my_commission_entry.get())
        take_to_the_bank_final = (fiz_summary_in_jpy * float(yen_swift_rate_entry.get())) + int(fiz_bank_comission_entry.get())
        customs_charges_final = float(fiz_custom_duty_entry.get())
        fiz_broker_final = int(fiz_sbkts_entry.get()) \
                         + int(fiz_svh_entry.get()) \
                         + int(fiz_svh_lab_parking_entry.get()) \
                         + int(fiz_broker_services_entry.get()) \
                         + int(fiz_temp_registrarion_entry.get()) \
                         + int(fiz_glonas_entry.get()) 

        fiz_take_to_the_bank_entry.delete(0, ctk.END)
        fiz_take_to_the_bank_entry.insert(0, take_to_the_bank_final)

        fiz_customs_charges_entry.delete(0, ctk.END)
        fiz_customs_charges_entry.insert(0, customs_charges_final)

        fiz_broker_entry.delete(0, ctk.END)
        fiz_broker_entry.insert(0, fiz_broker_final)

        fiz_all_summary = my_commission_final + take_to_the_bank_final + customs_charges_final + fiz_broker_final

        all_summary_entry.delete(0, ctk.END)
        all_summary_entry["state"] = "readonly"
        all_summary_entry.insert(0, f'{space}{space}{round((fiz_all_summary), 2)} российских рубля')
        
calculate_button = ctk.CTkButton(CTkFrame, text="Расчитать ориентировочную стоимость", command = calculate_everything)
calculate_button.grid(row=3, column=2, columnspan=2, padx=10, pady=4, sticky='we')

window.mainloop()
