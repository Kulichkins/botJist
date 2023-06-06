
import psycopg2
import telebot

# Параметры подключения к базе данных PostgreSQL
db_host = "localhost"
db_user = "postgres"
db_password = "123"
db_name = "postgres"
db_port = 5432

# Токен доступа к телеграм-боту
bot_token = '5409431088:AAEajmJQDCRgk_Pe3rRQimhW4WrYdczDAzI'

# Создание подключения к базе данных
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

# Создание экземпляра телеграм-бота
bot = telebot.TeleBot(bot_token)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Привет! Я бот, подключенный к базе данных PostgreSQL! Для начала определите свою роль (/admin) или (/client).")

    @bot.message_handler(commands=['client'])
    def handle_start(message):
        bot.reply_to(message,"Какую информцию вы хотите узнать:\nО вашем билете(/tinfo) \nО вашем маршруте(/road) \nО Расписании поездов(/desk)")

        @bot.message_handler(commands=['tinfo'])
        def handle_start(message):
            try:
                bot.reply_to(message, "Введи свой номер билета")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_player_info_input(message):
                    try:
                        pis = int(message.text)

                        # Создание объекта курсора
                        cursor = conn.cursor()

                        # Выполнение
                        cursor.execute(
                            f"""SELECT "Номер_Билета", "ФИО_Пассажира","ID_Станция_Посадки","ID_Станция_Высадки","Номер_Поезда" FROM poezda."Билеты" WHERE "Номер_Билета" = {pis}""")
                        result = cursor.fetchone()

                        cursor.close()
                        if result:
                            # Форматирование информации
                            player_info = f"ID: {result[0]}\nИмя: {result[1]}\nМесто посадки: {result[2]}\nМесто высадки: {result[3]}"

                            # Отправка информации пользователю
                            bot.reply_to(message, player_info)

                    except ValueError:
                        bot.reply_to(message, "Некорректный ввод информации")

                    return
            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при добавлении игрока в базу данных.")

        @bot.message_handler(commands=['road'])
        def handle_start(message):
            try:
                bot.reply_to(message, "Введи номер своего поезда(используя русские буквы)")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_player_info_input(message):
                    try:
                        pid = message.text

                        # Создание объекта курсора
                        cursor = conn.cursor()

                        # Выполнение
                        cursor.execute(
                            f"""SELECT "Номер_Поезда","ID_Станции","Время_прибытия" from poezda."Маршруты" WHERE "Номер_Поезда"= '{pid}' """)
                        result = cursor.fetchone()

                        cursor.close()
                        if result:
                            # Форматирование информации
                            player_info = f"Номер поезда: {result[0]}\nНомер станции: {result[1]}\nВремя отправки: {result[2]}"

                            # Отправка информации пользователю
                            bot.reply_to(message, player_info)

                    except ValueError:
                        bot.reply_to(message, "Некорректный ввод информации")

                    return
            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при добавлении в базу данных.")

        @bot.message_handler(commands=['desk'])
        def handle_start(message):
            try:
                bot.reply_to(message, "Введи номер своего поезда(используя русские буквы)")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_player_info_input(message):
                    try:
                        pig = message.text

                        # Создание объекта курсора
                        cursor = conn.cursor()

                        # Выполнение
                        cursor.execute(
                            f"""SELECT "Номер_поезда","Дата" from poezda."Расписание" WHERE "Номер_поезда" = '{pig}'""")
                        result = cursor.fetchone()

                        cursor.close()
                        if result:
                            # Форматирование информации
                            player_info = f"Номер поезда: {result[0]}\nДата отправки: {result[1]}"

                            # Отправка информации пользователю
                            bot.reply_to(message, player_info)

                    except ValueError:
                        bot.reply_to(message, "Некорректный ввод информации")

                    return
            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при добавлении в базу данных.")

    @bot.message_handler(commands=['admin'])
    def handle_start_8(message):
        bot.reply_to(message,"Выберите опцию: \nДобавить услугу(/addactive),\nДобавить поезд(/addtrain),\nВысчитать среднюю стоимость билета(/avgcost)")

        @bot.message_handler(commands=['addactive'])
        def handle_start_3(message):

            bot.reply_to(message, "Введи новый ID услуги и ее название в формате:\nID,\nИмя услуги")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_info_input_4(message):
                try:
                    info = message.text.split(', ')
                    id_us = int(info[0])
                    name_usl = info[1]

                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение
                    cursor.execute(
                        f"""INSERT INTO poezda."Услуги"("ID_услуги","Название") VALUES ({id_us},'{name_usl}')""")
                    conn.commit()

                    cursor.close()

                    bot.reply_to(message, "Услуга добавлена")
                except ValueError:
                    bot.reply_to(message, "Некорректный ")
                return

        @bot.message_handler(commands=['addtrain'])
        def handle_start_9(message):

            bot.reply_to(message, "Введи новый ID поезда и ее название в формате:\nНомер поезда(пример 117И),\nЛиния(пример Москва-Хабаровск)")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_info_input_4(message):
                try:
                    info = message.text.split(', ')
                    id_tr = info[0]
                    name_road = info[1]

                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение
                    cursor.execute(
                        f"""INSERT INTO poezda."Поезда"("Номер_Поезда","Название") VALUES ('{id_tr}','{name_road}')""")
                    conn.commit()

                    cursor.close()

                    bot.reply_to(message, "Поезд добавлен")
                except ValueError:
                    bot.reply_to(message, "Некорректный ")
                return

        @bot.message_handler(commands=['avgcost'])
        def handle_start_10(message):
            try:
                cursor = conn.cursor()
                cursor.execute("""SELECT AVG("Цена_Места") FROM poezda."Билеты" """)
                result = cursor.fetchone()

                cursor.close()
                if result:

                    player_info = f"Средняя стоимость билета: {round(result[0],0)}"

                # Отправка информации пользователю
                bot.reply_to(message, player_info)

            except ValueError:
                bot.reply_to(message, "Некорректный ввод информации")

    return






# Запуск телеграм-бота
bot.polling()

# Закрытие соединения с базой данных
conn.close()  # 1
