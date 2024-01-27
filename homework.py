#Калькулятор денег
#
# Калькулятор денег должен уметь:
# Сохранять новую запись о расходах методом add_record()
# Считать, сколько денег потрачено сегодня методом get_today_stats()
# Определять, сколько ещё денег можно потратить сегодня в рублях, долларах или евро — метод get_today_cash_remained(currency)
# Считать, сколько денег потрачено за последние 7 дней — метод get_week_stats()
import datetime as dt

class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment

class  Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records if record.date == today)

    def get_week_stat(self):
        today = dt.date.today()
        date_week_ago = today - dt.timedelta(days=7)
        return sum(record.amount for record in self.records if date_week_ago < record.date <= today)

    def get_limit_today(self):
        return self.limit - self.get_today_stats()

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        limit_today = self.get_limit_today()
        if limit_today > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {limit_today} кКал'
        else:
            return 'Хватит есть!'


class CashCalculator(Calculator):
    USD_RATE = 89.00
    EURO_RATE = 96.69
    RUB_RATE = 1
    def get_today_cash_remained(self, currency):
        money = {"руб": self.RUB_RATE,
                 "euro": self.EURO_RATE,
                 "usd": self.USD_RATE}
        limit_today = self.get_limit_today()
        limit_today_curr = abs(round(limit_today / money[currency], 2))
        if limit_today > 0:
            return f"На сегодня осталось {limit_today_curr} {currency}"
        elif limit_today == 0:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {limit_today_curr} {currency}'


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date='28.01.2019'))

print(cash_calculator.get_today_cash_remained("руб"))