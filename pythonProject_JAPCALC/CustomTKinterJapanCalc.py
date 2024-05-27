import customtkinter as ctk 
from datetime import datetime
import requests 
from bs4 import BeautifulSoup
from lxml import etree
from tkinter import BooleanVar
from PIL import ImageTk, Image


ctk.set_default_color_theme("green")

def bbr_pars():
    url = "https://bbr.ru"
    response = requests.get(url)

    if response.status_code == 200:
        # Создаем объект BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Преобразуем BeautifulSoup объект в объект lxml для использования XPath
        root = etree.HTML(str(soup))
        # Используем XPath для извлечения курса покупки йен
        result = root.xpath('//*[@id="__next"]/div/main/div/div[3]/div/div[2]/div[4]/div[2]/div[1]/span[1]/text()')
        bbr_pars = str(result[0]) 
        bbr_pars = bbr_pars.replace(',','.')
        return bbr_pars
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
def clear_frame(CTkFrame2):
    for widget in CTkFrame2.winfo_children():
        widget.destroy()   


#Создаем поля с информацией под ЮР ЛИЦО      
def legal_checkbox_ON():

    clear_frame(CTkFrame2)

    auc_vehicle_price_lable = ctk.CTkLabel(CTkFrame2, text='Аукционная стоимость:')
    auc_vehicle_price_lable.grid(row=1, column=0, padx=10, pady=4, sticky='w')
    auc_vehicle_price_entry = ctk.CTkEntry(CTkFrame2)
    auc_vehicle_price_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')

    freight_lable = ctk.CTkLabel(CTkFrame2, text="Фрахт:")
    freight_lable.grid(row=2, column=0, padx=10, pady=4, sticky='w')
    freight_entry = ctk.CTkEntry(CTkFrame2)
    freight_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')


    fob_lable = ctk.CTkLabel(CTkFrame2, text="Фоб:")
    fob_lable.grid(row=3, column=0, padx=10, pady=4, sticky='w')
    fob_entry = ctk.CTkEntry(CTkFrame2)
    fob_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')


    japan_comission_lable = ctk.CTkLabel(CTkFrame2, text= f"Комиссия Японии за стоимость:")
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
    util_sbot_entry = ctk.CTkEntry(CTkFrame2)
    util_sbot_entry.grid(row=1, column=3, padx=10, pady=4, sticky='w')
    
    custom_rate_lable = ctk.CTkLabel(CTkFrame2, text='Таможенная ставка')
    custom_rate_lable.grid(row=2, column=2, padx=10, pady=4, sticky='w')
    custom_rate_entry = ctk.CTkEntry(CTkFrame2)
    custom_rate_entry.grid(row=2, column=3, padx=10, pady=4)


    nds_lable = ctk.CTkLabel(CTkFrame2, text='НДС')
    nds_lable.grid(row=3, column=2, padx=10, pady=4, sticky='w')
    nds_entry = ctk.CTkEntry(CTkFrame2)
    nds_entry.grid(row=3, column=3, padx=10, pady=4, sticky='w')


    custom_duty_lable = ctk.CTkLabel(CTkFrame2, text='Пошлина')
    custom_duty_lable.grid(row=4, column=2, padx=10, pady=4, sticky='w')
    custom_duty_entry = ctk.CTkEntry(CTkFrame2)
    custom_duty_entry.grid(row=4, column=3, padx=10, pady=4, sticky='w')


    excise_lable = ctk.CTkLabel(CTkFrame2, text='Акциз')
    excise_lable.grid(row=5, column=2, padx=10, pady=4, sticky='w')
    excise_entry = ctk.CTkEntry(CTkFrame2)
    excise_entry.grid(row=5, column=3, padx=10, pady=4, sticky='w')

    
    custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Таможенное оформление')
    custom_services_lable.grid(row=6, column=2, padx=10, pady=4, sticky='w')
    custom_services_entry = ctk.CTkEntry(CTkFrame2)
    custom_services_entry.grid(row=6, column=3, padx=10, pady=4, sticky='w')


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

    custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Броке + Глонас')
    custom_services_lable.grid(row=15, column=0, padx=10, pady=4, sticky='w')
    custom_services_entry = ctk.CTkEntry(CTkFrame2)
    custom_services_entry.grid(row=15, column=1, padx=10, pady=4, sticky='w')


#Создаем поля с информацией под ЮР ЛИЦО 
def legal_checkbox_OFF():

    clear_frame(CTkFrame2)

    fiz_auc_vehicle_price_lable = ctk.CTkLabel(CTkFrame2, text='Аукционная стоимость:')
    fiz_auc_vehicle_price_lable.grid(row=1, column=0, padx=10, pady=4, sticky='w')
    fiz_auc_vehicle_price_entry = ctk.CTkEntry(CTkFrame2)
    fiz_auc_vehicle_price_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')

    fiz_freight_lable = ctk.CTkLabel(CTkFrame2, text="Фрахт:")
    fiz_freight_lable.grid(row=2, column=0, padx=10, pady=4, sticky='w')
    fiz_freight_entry = ctk.CTkEntry(CTkFrame2)
    fiz_freight_entry.grid(row=2, column=1, padx=10, pady=4, sticky='w')

    fiz_fob_lable = ctk.CTkLabel(CTkFrame2, text="Фоб:")
    fiz_fob_lable.grid(row=3, column=0, padx=10, pady=4, sticky='w')
    fiz_fob_entry = ctk.CTkEntry(CTkFrame2)
    fiz_fob_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')

    fiz_japan_comission_lable = ctk.CTkLabel(CTkFrame2, text= f"Комиссия Японии за стоимость:")
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

    fiz_svh_lab_parking_lable = ctk.CTkLabel(CTkFrame2, text='СВХ, Лабо-я, Стоянка')
    fiz_svh_lab_parking_lable.grid(row=7, column=2, padx=10, pady=4, sticky='w')
    fiz_svh_lab_parking_entry = ctk.CTkEntry(CTkFrame2)
    fiz_svh_lab_parking_entry.grid(row=7, column=3, padx=10, pady=4, sticky='w')

    fiz_broker_services_lable= ctk.CTkLabel(CTkFrame2, text='Услуга брокера')
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

    fiz_custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Моя комиссия')
    fiz_custom_services_lable.grid(row=9, column=0, padx=10, pady=4, sticky='w')
    fiz_custom_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_services_entry.grid(row=9, column=1, padx=10, pady=4, sticky='w')

    fiz_custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Взять с собой в банк')
    fiz_custom_services_lable.grid(row=10, column=0, padx=10, pady=4, sticky='w')
    fiz_custom_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_services_entry.grid(row=10, column=1, padx=10, pady=4, sticky='w')

    fiz_custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Оплата таможни')
    fiz_custom_services_lable.grid(row=11, column=0, padx=10, pady=4, sticky='w')
    fiz_custom_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_services_entry.grid(row=11, column=1, padx=10, pady=4, sticky='w')

    fiz_custom_services_lable = ctk.CTkLabel(CTkFrame2, text='Оплата брокеру')
    fiz_custom_services_lable.grid(row=12, column=0, padx=10, pady=4, sticky='w')
    fiz_custom_services_entry = ctk.CTkEntry(CTkFrame2)
    fiz_custom_services_entry.grid(row=12, column=1, padx=10, pady=4, sticky='w')


#Что делать при нажатии чекбокса ЮР ЛИЦО/ФИЗ ЛИЦО    
def on_legal_checkbox():

    if legal_check_var.get():
        legal_checkbox_ON()
    else:
        legal_checkbox_OFF() 

#Комманда для кнопки которая выводит все расчеты
def calculate_everything():
    age_rank()
    japan_comission_for_the_price()

# Функция вычисления возраста авто в Юридических категориях таможни РФ 
def age_rank():
    vehicle_month_entryed = int(vehicle_month_entry.get())
    vehicle_year_entryed = int(vehicle_year_entry.get())
    current_month_entryed = int(current_month_entry.get())
    current_year_entryed = int(current_year_entry.get())

    vehicle_date_in_months = (vehicle_year_entryed*12)+vehicle_month_entryed
    current_date_in_months = (current_year_entryed*12)+current_month_entryed
    
    vehicle_age_months = current_date_in_months - vehicle_date_in_months

    
    if vehicle_age_months <= 36:
        age_rank = ' до 3-х лет'
    elif vehicle_age_months >=36 and vehicle_age_months <= 60:
        age_rank = ' 3-5 лет'
    elif vehicle_age_months >=60 and vehicle_age_months <= 84:
        age_rank = ' 5-7 лет'
    elif vehicle_age_months >=84:
        age_rank = ' 7+ лет'

    vehicle_age_CTkLabel = ctk.CTkLabel(CTkFrame2, text= f"Возраст авто:{age_rank}")
    vehicle_age_CTkLabel.grid(row=3, column=1, padx=10, pady=4)

# Функция вычисления комиссии Японского брокера за цену на аукционе 
def japan_comission_for_the_price():

    vehicle_auc_price_entryed = int(vehicle_auc_price_entry.get())

    if vehicle_auc_price_entryed > 2999:
        japan_comission_for_the_price = 40
    elif vehicle_auc_price_entryed > 1999:
        japan_comission_for_the_price = 30
    elif vehicle_auc_price_entryed > 999:
        japan_comission_for_the_price = 20
    else:
        japan_comission_for_the_price = 0


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

window = ctk.CTk(fg_color='#281b22')
window.title('РАСЧЕТ СТОИМОСТИ АВТО ИЗ ЯПОНИИ')

window.geometry("740x715")  
window.resizable(False, False)


CTkFrame = ctk.CTkFrame(window,fg_color='#3D3D3D')
CTkFrame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


CTkFrame2 = ctk.CTkFrame(window,fg_color='#3D3D3D')  
CTkFrame2.grid(row=1, column=0, padx=10, pady=0, sticky='nsew')


legal_check_var = BooleanVar()
legal_checkbox = ctk.CTkCheckBox(CTkFrame, text="Для ЮР лица", variable=legal_check_var, command=on_legal_checkbox)
legal_checkbox.grid(row=6, column=3, padx=10, pady=4, sticky='w')


vehicle_auc_price_CTkLabel = ctk.CTkLabel(CTkFrame, text=f"Аукционная стоимость:{space}{space}")
vehicle_auc_price_CTkLabel.grid(row=0, column=0, padx=10, pady=2, sticky='w')
vehicle_auc_price_entry = ctk.CTkEntry(CTkFrame)
vehicle_auc_price_entry.grid(row=0, column=1, padx=10, pady=4, sticky='w')


motor_volume_CTkLabel = ctk.CTkLabel(CTkFrame, text="Объем мотора:")
motor_volume_CTkLabel.grid(row=1, column=0, padx=10, pady=4, sticky='w')
motor_volume_entry = ctk.CTkEntry(CTkFrame)
motor_volume_entry.grid(row=1, column=1, padx=10, pady=4, sticky='w')


horse_power_CTkLabel = ctk.CTkLabel(CTkFrame, text="Лошадинных сил")
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

current_year_CTkLabel = ctk.CTkLabel(CTkFrame, text="Текущий год")
current_year_CTkLabel.grid(row=3, column=0, padx=10, pady=4, sticky='w')
current_year_entry = ctk.CTkEntry(CTkFrame)
current_year_entry.grid(row=3, column=1, padx=10, pady=4, sticky='w')


current_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="Текущий месяц")
current_month_CTkLabel.grid(row=4, column=0, padx=10, pady=4, sticky='w')
current_month_entry = ctk.CTkEntry(CTkFrame)
current_month_entry.grid(row=4, column=1, padx=10, pady=4, sticky='w')

vehicle_year_CTkLabel = ctk.CTkLabel(CTkFrame, text="Год выпуска авто")
vehicle_year_CTkLabel.grid(row=5, column=0, padx=10, pady=4, sticky='w')
vehicle_year_entry = ctk.CTkComboBox(CTkFrame, values=years, state="readonly", variable=year_var)
vehicle_year_entry.grid(row=5, column=1)
vehicle_year_entry["state"] = "readonly"


vehicle_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="Месяц выпуска авто")
vehicle_month_CTkLabel.grid(row=6, column=0, padx=10, pady=4, sticky='w')
vehicle_month_entry = ctk.CTkComboBox(CTkFrame, values=months, state="readonly", variable=month_var)
vehicle_month_entry.grid(row=6, column=1)
vehicle_month_entry["state"] = "readonly"


yen_swift_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс йены в вашем банке")
yen_swift_rate_CTkLabel.grid(row=0, column=2, padx=10, pady=4, sticky='w')
yen_swift_rate_entry = ctk.CTkEntry(CTkFrame)
yen_swift_rate_entry.grid(row=0, column=3, padx=10, pady=4, sticky='w')


euro_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс евро по ЦБ")
euro_rate_CTkLabel.grid(row=1, column=2, padx=10, pady=4, sticky='w')
euro_rate_entry = ctk.CTkEntry(CTkFrame)
euro_rate_entry.grid(row=1, column=3, padx=10, pady=4, sticky='w')


yen_central_bank_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс йены по ЦБ")
yen_central_bank_rate_CTkLabel.grid(row=2, column=2, padx=10, pady=4, sticky='w')
yen_central_bank_rate_entry = ctk.CTkEntry(CTkFrame)
yen_central_bank_rate_entry.grid(row=2, column=3, padx=10, pady=4, sticky='w')


calculate_button = ctk.CTkButton(CTkFrame, text="Расчитать", command = calculate_everything)
calculate_button.grid(row=6, column=2, padx=10, pady=4, sticky='we')

#Автозаполнение
auto_fill()

#По дефолту задаем расчет на ФИЗ ЛИЦО
legal_checkbox_OFF()

window.mainloop()








