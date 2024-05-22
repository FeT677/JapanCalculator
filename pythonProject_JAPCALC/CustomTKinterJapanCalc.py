import customtkinter as ctk
from datetime import datetime
import requests
from bs4 import BeautifulSoup


excise_duty_entryed = None
custom_duty_legal_entryed = None
nds_entryed = None
flat_rate_legal_entryed = None
utilization_tax_legal_entryed = None
glonas_entryed = None
temp_registration_entryed = None
broker_price_entryed = None
svh_lab_entryed = None
svh_entryed = None
sbkts_entryed = None
vehicle_month_entryed = None
vehicle_year_entryed = None
current_month_entryed = None
current_year_entryed = None
total_in_japan_rub_entryed = None
total_in_japan_yen_entryed = None
Jap_price_commission_entryed = None
fob_entryed = None
freight_entryed = None
customs_formalities_entryed = None
customs_tariff_entryed = None
custom_duty_entryed = None
bank_transfer_fee_entryed = None
utilization_tax_entryed = None
my_commission_entryed = None
yen_central_bank_rate_entryed = None
yen_swift_rate_entryed = None
euro_rate_entryed = None
horse_power_entryed = None
motor_volume_entryed = None
vehicle_auc_price_entryed = None
broker_and_glonas_entryed = None
customs_formalities_legal_entryed = None

current_month = datetime.now().month
current_year = datetime.now().year

def legal_toggle_entries():
    if var1.get():
        broker_and_glonas_entry.configure(state='normal')
        customs_formalities_legal_entry.configure(state='normal')
        excise_duty_entry.configure(state='normal')
        custom_duty_legal_entry.configure(state='normal')
        nds_entry.configure(state='normal')
        flat_rate_legal_entry.configure(state='normal')
        utilization_tax_legal_entry.configure(state='normal')

        glonas_entry.configure(state='disabled')
        temp_registration_entry.configure(state='disabled')
        broker_price_entry.configure(state='disabled')
        svh_lab_entry.configure(state='disabled')
        svh_entry.configure(state='disabled')
        sbkts_entry.configure(state='disabled')

    else:
        broker_and_glonas_entry.configure(state='disabled')
        customs_formalities_legal_entry.configure(state='disabled')
        excise_duty_entry.configure(state='disabled')
        custom_duty_legal_entry.configure(state='disabled')
        nds_entry.configure(state='disabled')
        flat_rate_legal_entry.configure(state='disabled')
        utilization_tax_legal_entry.configure(state='disabled')

        glonas_entry.configure(state='normal')
        temp_registration_entry.configure(state='normal')
        broker_price_entry.configure(state='normal')
        svh_lab_entry.configure(state='normal')
        svh_entry.configure(state='normal')
        sbkts_entry.configure(state='normal')


    checkbox = ctk.CTkCheckBox(CTkFrame, text="На Юридическое лицо", variable=var1, command=legal_toggle_entries)
    checkbox.grid(row=21, column=2, padx=10, pady=10)

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

eur_rate, jpy_rate = get_exchange_rates()
jpy_rate = jpy_rate/100
def get_data():
    global excise_duty_entryed, custom_duty_legal_entryed, nds_entryed, flat_rate_legal_entryed, utilization_tax_legal_entryed, glonas_entryed, temp_registration_entryed, broker_price_entryed, svh_lab_entryed, svh_entryed, sbkts_entryed, vehicle_month_entryed, vehicle_year_entryed, current_month_entryed, current_year_entryed, total_in_japan_rub_entryed, total_in_japan_yen_entryed, Jap_price_commission_entryed, fob_entryed, freight_entryed, customs_formalities_entryed, customs_tariff_entryed, custom_duty_entryed, bank_transfer_fee_entryed, utilization_tax_entryed, my_commission_entryed, yen_central_bank_rate_entryed, yen_swift_rate_entryed, euro_rate_entryed, horse_power_entryed, motor_volume_entryed, vehicle_auc_price_entryed, broker_and_glonas_entryed, customs_formalities_legal_entryed

    excise_duty_entryed = float(excise_duty_entry.get())
    custom_duty_legal_entryed = float(custom_duty_legal_entry.get())
    nds_entryed = float(nds_entry.get())
    flat_rate_legal_entryed = float(flat_rate_legal_entry.get())
    utilization_tax_legal_entryed = float(utilization_tax_legal_entry.get())
    glonas_entryed = float(glonas_entry.get())
    temp_registration_entryed = float(temp_registration_entry.get())
    broker_price_entryed = float(broker_price_entry.get())
    svh_lab_entryed = float(svh_lab_entry.get())
    svh_entryed = float(svh_entry.get())
    sbkts_entryed = float(sbkts_entry.get())
    vehicle_month_entryed = float(vehicle_month_entry.get())
    vehicle_year_entryed = float(vehicle_year_entry.get())
    current_month_entryed = float(current_month_entry.get())
    current_year_entryed = float(current_year_entry.get())
    total_in_japan_rub_entryed = float(total_in_japan_rub_entry.get())
    total_in_japan_yen_entryed = float(total_in_japan_yen_entry.get())
    Jap_price_commission_entryed = float(Jap_price_commission_entry.get())
    fob_entryed = float(fob_entry.get())
    freight_entryed = float(freight_entry.get())
    customs_formalities_entryed = float(customs_formalities_entry.get())
    customs_tariff_entryed = float(customs_tariff_entry.get())
    custom_duty_entryed = float(custom_duty_entry.get())
    bank_transfer_fee_entryed = float(bank_transfer_fee_entry.get())
    utilization_tax_entryed = float(utilization_tax_entry.get())
    my_commission_entryed = float(my_commission_entry.get())
    yen_central_bank_rate_entryed = float(yen_central_bank_rate_entry.get())
    yen_swift_rate_entryed = float(yen_swift_rate_entry.get())
    euro_rate_entryed = float(euro_rate_entry.get())
    horse_power_entryed = float(horse_power_entry.get())
    motor_volume_entryed = float(motor_volume_entry.get())
    vehicle_auc_price_entryed = float(vehicle_auc_price_entry.get())
    broker_and_glonas_entryed = float(broker_and_glonas_entry.get())
    customs_formalities_legal_entryed = float(customs_formalities_legal_entry.get())

def auto_fill():
    broker_and_glonas_entry.configure(state='disabled')
    customs_formalities_legal_entry.configure(state='disabled')
    excise_duty_entry.configure(state='disabled')
    custom_duty_legal_entry.configure(state='disabled')
    nds_entry.configure(state='disabled')
    flat_rate_legal_entry.configure(state='disabled')
    utilization_tax_legal_entry.configure(state='disabled')

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
    yen_central_bank_rate_entry.insert(0, jpy_rate)
    yen_central_bank_rate_entry.configure(state='disabled')

    euro_rate_entry.delete(0, ctk.END)
    euro_rate_entry.insert(0, eur_rate)
    euro_rate_entry.configure(state='disabled')

    yen_swift_rate_entry.insert(0, 'Ввести')
    my_commission_entry.insert(0, 30000)
    my_commission_entry.configure(state='disabled')

window = ctk.CTk()
window.title("Расчет стоимости авто из Японии")

window.geometry("912x930")  # Устанавливаем размер окна 800x600 пикселей
window.resizable(True, True)  # Делаем окно нерасширяемым по обеим осям

CTkFrame = ctk.CTkFrame(window)
CTkFrame.grid(row=0, column=0, padx=5, pady=5)

CTkFrame = ctk.CTkFrame(window)
CTkFrame.grid(row=0, column=0, padx=5, pady=5)

var1 = ctk.BooleanVar()

vehicle_auc_price_CTkLabel = ctk.CTkLabel(CTkFrame, text="Аукционная стоимость:", anchor=ctk.N)
vehicle_auc_price_CTkLabel.grid(row=0, column=0, padx=5, pady=5)

vehicle_auc_price_entry = ctk.CTkEntry(CTkFrame)
vehicle_auc_price_entry.grid(row=0, column=1, padx=5, pady=5)

motor_volume_CTkLabel = ctk.CTkLabel(CTkFrame, text="Объем мотора:", anchor=ctk.N)
motor_volume_CTkLabel.grid(row=1, column=0, padx=5, pady=5)

motor_volume_entry = ctk.CTkEntry(CTkFrame)
motor_volume_entry.grid(row=1, column=1, padx=5, pady=5)

horse_power_CTkLabel = ctk.CTkLabel(CTkFrame, text="Лошадинных сил", anchor=ctk.N)
horse_power_CTkLabel.grid(row=2, column=0, padx=5, pady=5)


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

vehicle_year_CTkLabel = ctk.CTkLabel(CTkFrame, text="Год выпуска авто", anchor=ctk.N)
vehicle_year_CTkLabel.grid(row=3, column=0, padx=5, pady=5)
vehicle_year_entry = ctk.CTkComboBox(CTkFrame)
vehicle_year_entry = ctk.CTkComboBox(CTkFrame, values=years, state="readonly", variable=year_var)
vehicle_year_entry["state"] = "readonly"
vehicle_year_entry.grid(row=3, column=1)

vehicle_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="Месяц выпуска авто", anchor=ctk.N)
vehicle_month_CTkLabel.grid(row=4, column=0, padx=5, pady=5)
vehicle_month_entry = ctk.CTkComboBox(CTkFrame)
vehicle_month_entry = ctk.CTkComboBox(CTkFrame, values=months, state="readonly", variable=month_var)
vehicle_month_entry["state"] = "readonly"
vehicle_month_entry.grid(row=4, column=1) 


horse_power_entry = ctk.CTkEntry(CTkFrame)
horse_power_entry.grid(row=2, column=1, padx=5, pady=5)


euro_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс евро по ЦБ", anchor=ctk.N)
euro_rate_CTkLabel.grid(row=6, column=0, padx=5, pady=5)

euro_rate_entry = ctk.CTkEntry(CTkFrame)
euro_rate_entry.grid(row=6, column=1, padx=5, pady=5)

yen_swift_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс йены в вашем банке", anchor=ctk.N)
yen_swift_rate_CTkLabel.grid(row=5, column=0, padx=5, pady=5)

yen_swift_rate_entry = ctk.CTkEntry(CTkFrame)
yen_swift_rate_entry.grid(row=5, column=1, padx=5, pady=5)

yen_central_bank_rate_CTkLabel = ctk.CTkLabel(CTkFrame, text="Курс йены по ЦБ", anchor=ctk.N)
yen_central_bank_rate_CTkLabel.grid(row=7, column=0, padx=5, pady=5)

yen_central_bank_rate_entry = ctk.CTkEntry(CTkFrame)
yen_central_bank_rate_entry.grid(row=7, column=1, padx=5, pady=5)

my_commission_CTkLabel = ctk.CTkLabel(CTkFrame, text="Моя комиссия", anchor=ctk.N)
my_commission_CTkLabel.grid(row=8, column=0, padx=5, pady=5)

my_commission_entry = ctk.CTkEntry(CTkFrame)
my_commission_entry.grid(row=8, column=1, padx=5, pady=5)

utilization_tax_CTkLabel = ctk.CTkLabel(CTkFrame, text="Утилизационный сбор", anchor=ctk.N)
utilization_tax_CTkLabel.grid(row=9, column=0, padx=5, pady=5)

utilization_tax_entry = ctk.CTkEntry(CTkFrame)
utilization_tax_entry.grid(row=9, column=1, padx=5, pady=5)

bank_transfer_fee_CTkLabel = ctk.CTkLabel(CTkFrame, text="Комиссия за переводы SWIFT", anchor=ctk.N)
bank_transfer_fee_CTkLabel.grid(row=10, column=0, padx=5, pady=5)

bank_transfer_fee_entry = ctk.CTkEntry(CTkFrame)
bank_transfer_fee_entry.grid(row=10, column=1, padx=5, pady=5)

custom_duty_CTkLabel = ctk.CTkLabel(CTkFrame, text="Таможенная пошлина", anchor=ctk.N)
custom_duty_CTkLabel.grid(row=11, column=0, padx=5, pady=5)

custom_duty_entry = ctk.CTkEntry(CTkFrame)
custom_duty_entry.grid(row=11, column=1, padx=5, pady=5)

customs_tariff_CTkLabel = ctk.CTkLabel(CTkFrame, text="Таможенная ставка", anchor=ctk.N)
customs_tariff_CTkLabel.grid(row=12, column=0, padx=5, pady=5)

customs_tariff_entry = ctk.CTkEntry(CTkFrame)
customs_tariff_entry.grid(row=12, column=1, padx=5, pady=5)

customs_formalities_CTkLabel = ctk.CTkLabel(CTkFrame, text="Таможенное оформление", anchor=ctk.N)
customs_formalities_CTkLabel.grid(row=13, column=0, padx=5, pady=5)

customs_formalities_entry = ctk.CTkEntry(CTkFrame)
customs_formalities_entry.grid(row=13, column=1, padx=5, pady=5)

freight_CTkLabel = ctk.CTkLabel(CTkFrame, text="Фрахт", anchor=ctk.N)
freight_CTkLabel.grid(row=14, column=0, padx=5, pady=5)

freight_entry = ctk.CTkEntry(CTkFrame)
freight_entry.grid(row=14, column=1, padx=5, pady=5)

fob_CTkLabel = ctk.CTkLabel(CTkFrame, text="Фоб", anchor=ctk.N)
fob_CTkLabel.grid(row=15, column=0, padx=5, pady=5)

fob_entry = ctk.CTkEntry(CTkFrame)
fob_entry.grid(row=15, column=1, padx=5, pady=5)

Jap_price_commission_CTkLabel = ctk.CTkLabel(CTkFrame, text="Коммисия Японии за цену", anchor=ctk.N)
Jap_price_commission_CTkLabel.grid(row=16, column=0, padx=5, pady=5)

Jap_price_commission_entry = ctk.CTkEntry(CTkFrame)
Jap_price_commission_entry.grid(row=16, column=1, padx=5, pady=5)

total_in_japan_yen_CTkLabel = ctk.CTkLabel(CTkFrame, text="Расходы по японии (YEN)", anchor=ctk.N)
total_in_japan_yen_CTkLabel.grid(row=17, column=0, padx=5, pady=5)

total_in_japan_yen_entry = ctk.CTkEntry(CTkFrame)
total_in_japan_yen_entry.grid(row=17, column=1, padx=5, pady=5)

total_in_japan_rub_CTkLabel = ctk.CTkLabel(CTkFrame, text="Расходы по японии (RUB)", anchor=ctk.N)
total_in_japan_rub_CTkLabel.grid(row=18, column=0, padx=5, pady=5)

total_in_japan_rub_entry = ctk.CTkEntry(CTkFrame)
total_in_japan_rub_entry.grid(row=18, column=1, padx=5, pady=5)


current_year_CTkLabel = ctk.CTkLabel(CTkFrame, text="Текущий год", anchor=ctk.N)
current_year_CTkLabel.grid(row=0, column=3, padx=5, pady=5)

current_year_entry = ctk.CTkEntry(CTkFrame)
current_year_entry.grid(row=0, column=4, padx=5, pady=5)

current_month_CTkLabel = ctk.CTkLabel(CTkFrame, text="Текущий месяц", anchor=ctk.N)
current_month_CTkLabel.grid(row=1, column=3, padx=5, pady=5)

current_month_entry = ctk.CTkEntry(CTkFrame)
current_month_entry.grid(row=1, column=4, padx=5, pady=5)


sbkts_CTkLabel = ctk.CTkLabel(CTkFrame, text="СБКТС", anchor=ctk.N)
sbkts_CTkLabel.grid(row=4, column=3, padx=5, pady=5)

sbkts_entry = ctk.CTkEntry(CTkFrame)
sbkts_entry.grid(row=4, column=4, padx=5, pady=5)

svh_CTkLabel = ctk.CTkLabel(CTkFrame, text="СВХ", anchor=ctk.N)
svh_CTkLabel.grid(row=5, column=3, padx=5, pady=5)

svh_entry = ctk.CTkEntry(CTkFrame)
svh_entry.grid(row=5, column=4, padx=5, pady=5)

svh_lab_CTkLabel = ctk.CTkLabel(CTkFrame, text="СВХ лаборатория", anchor=ctk.N)
svh_lab_CTkLabel.grid(row=6, column=3, padx=5, pady=5)

svh_lab_entry = ctk.CTkEntry(CTkFrame)
svh_lab_entry.grid(row=6, column=4, padx=5, pady=5)

broker_price_CTkLabel = ctk.CTkLabel(CTkFrame, text="Комиссия брокера", anchor=ctk.N)
broker_price_CTkLabel.grid(row=7, column=3, padx=5, pady=5)

broker_price_entry = ctk.CTkEntry(CTkFrame)
broker_price_entry.grid(row=7, column=4, padx=5, pady=5)

temp_registration_CTkLabel = ctk.CTkLabel(CTkFrame, text="Временная регистрация", anchor=ctk.N)
temp_registration_CTkLabel.grid(row=8, column=3, padx=5, pady=5)

temp_registration_entry = ctk.CTkEntry(CTkFrame)
temp_registration_entry.grid(row=8, column=4, padx=5, pady=5)

glonas_CTkLabel = ctk.CTkLabel(CTkFrame, text="Глонас", anchor=ctk.N)
glonas_CTkLabel.grid(row=9, column=3, padx=5, pady=5)

glonas_entry = ctk.CTkEntry(CTkFrame)
glonas_entry.grid(row=9, column=4, padx=5, pady=5)

utilization_tax_legal_CTkLabel = ctk.CTkLabel(CTkFrame, text="Утиль сбор для ЮР", anchor=ctk.N)
utilization_tax_legal_CTkLabel.grid(row=10, column=3, padx=5, pady=5)

utilization_tax_legal_entry = ctk.CTkEntry(CTkFrame)
utilization_tax_legal_entry.grid(row=10, column=4, padx=5, pady=5)

flat_rate_legal_CTkLabel = ctk.CTkLabel(CTkFrame, text="Единая ставка для ЮР", anchor=ctk.N)
flat_rate_legal_CTkLabel.grid(row=11, column=3, padx=5, pady=5)

flat_rate_legal_entry = ctk.CTkEntry(CTkFrame)
flat_rate_legal_entry.grid(row=11, column=4, padx=5, pady=5)

nds_CTkLabel = ctk.CTkLabel(CTkFrame, text="НДС", anchor=ctk.N)
nds_CTkLabel.grid(row=12, column=3, padx=5, pady=5)

nds_entry = ctk.CTkEntry(CTkFrame)
nds_entry.grid(row=12, column=4, padx=5, pady=5)

custom_duty_legal_CTkLabel = ctk.CTkLabel(CTkFrame, text="Таможенная пошлина для ЮР", anchor=ctk.N)
custom_duty_legal_CTkLabel.grid(row=13, column=3, padx=5, pady=5)

custom_duty_legal_entry = ctk.CTkEntry(CTkFrame)
custom_duty_legal_entry.grid(row=13, column=4, padx=5, pady=5)

excise_duty_CTkLabel = ctk.CTkLabel(CTkFrame, text="Акциз для ЮР", anchor=ctk.N)
excise_duty_CTkLabel.grid(row=14, column=3, padx=5, pady=5)

excise_duty_entry = ctk.CTkEntry(CTkFrame)
excise_duty_entry.grid(row=14, column=4, padx=5, pady=5)

customs_formalities_legal_CTkLabel = ctk.CTkLabel(CTkFrame, text="Таможенное оформление для ЮР", anchor=ctk.N)
customs_formalities_legal_CTkLabel.grid(row=15, column=3, padx=5, pady=5)

customs_formalities_legal_entry = ctk.CTkEntry(CTkFrame)
customs_formalities_legal_entry.grid(row=15, column=4, padx=5, pady=5)

broker_and_glonas_CTkLabel = ctk.CTkLabel(CTkFrame, text="Брокер и глонас для ЮР", anchor=ctk.N)
broker_and_glonas_CTkLabel.grid(row=16, column=3, padx=5, pady=5)

broker_and_glonas_entry = ctk.CTkEntry(CTkFrame)
broker_and_glonas_entry.grid(row=16, column=4, padx=5, pady=5)


calculate_button = ctk.CTkButton(CTkFrame, text="Рассчитать", command=get_data)
calculate_button.grid(row=20, column=2, padx=5, pady=5)

legal_toggle_entries()

auto_fill()

window.mainloop()






