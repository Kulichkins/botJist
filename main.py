
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
    bot.reply_to(message,
                 "Привет! Я бот, подключенный к базе данных PostgreSQL! Для начала определите свою роль (/admin) или (/client).")

    @bot.message_handler(commands=['client'])
    def handle_start(message):

        bot.reply_to(message,
                     "Введите свой номер билета")

        @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
        def handle_player_info_input(message):
            try:
                player_info = message.text.split(', ')
                pid = int(player_info[0])

                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение INSERT-запроса для добавления нового игрока
                cursor.execute(
                    f"""SELECT "Номер_Билета", "ФИО_Пассажира","ID_Станция_Посадки","ID_Станция_Высадки" FROM poezda."Билеты" WHERE "Номер_Билета" = {pid} """)

                result = cursor.fetchall()


                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Ваши данные:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except ValueError:
                bot.reply_to(message, "Некорректный ввод информации")

            return


        # Пример запроса к базе данных
        @bot.message_handler(commands=['ticket'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM Человек')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Люди в нашем царстве:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

        @bot.message_handler(commands=['inventory'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM инвентарь')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Шмотки нищеты:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

        @bot.message_handler(commands=['cash'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Выполнение запроса к базе данных
                cursor.execute('SELECT * FROM баланс')
                result = cursor.fetchall()

                cursor.close()

                formatted_result = ''
                for row in result:
                    formatted_row = ', '.join(str(value) for value in row)
                    formatted_result += f"- {formatted_row}\n"

                # Отправка форматированного вывода пользователю
                if formatted_result:
                    bot.reply_to(message, f"Монеты:\n{formatted_result}")
                else:
                    bot.reply_to(message, "Представление пустое.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

    @bot.message_handler(commands=['procedures'])
    def handle_start(message):
        bot.reply_to(message,
                     "Я могу вывести хранимые процедуры: вместимость всех стадионов Канады(/Canadaarena) и количество игроков, вес которых больше или равен числу введенному пользователем(/playerwght). Также можно с помощью процедуры изменять вес игроков по ID(/update_weight)")

        @bot.message_handler(commands=['update_weight'])
        def handle_update_weight(message):
            try:
                # Запрашиваем у пользователя идентификатор игрока
                bot.reply_to(message, "Введите идентификатор игрока:")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_player_id_input(message):
                    try:
                        player_id = int(message.text)

                        # Запрашиваем у пользователя новый вес
                        bot.reply_to(message, "Введите новый вес игрока:")

                        @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                        def handle_weight_input(message):
                            try:
                                weight = int(message.text)

                                # Создание объекта курсора
                                cursor = conn.cursor()

                                # Вызов хранимой процедуры для обновления веса игрока
                                procedure_name = 'update_player_weight'
                                cursor.execute(f"CALL {procedure_name}({player_id}, {weight})")

                                # Применение изменений в базе данных
                                conn.commit()

                                cursor.close()

                                bot.reply_to(message, "Вес игрока успешно обновлен.")
                            except ValueError:
                                bot.reply_to(message, "Некорректный ввод веса.")

                            except Exception as e:
                                bot.reply_to(message, "Произошла ошибка при обновлении данных.")

                        bot.register_next_step_handler(message, handle_weight_input)

                    except ValueError:
                        bot.reply_to(message, "Некорректный идентификатор игрока.")

                    except Exception as e:
                        bot.reply_to(message, "Произошла ошибка при обновлении данных.")

                bot.register_next_step_handler(message, handle_player_id_input)

            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при обновлении данных.")

        @bot.message_handler(commands=['Canadaarena'])
        def handle_get_data(message):
            try:
                # Создание объекта курсора
                cursor = conn.cursor()

                # Вызов хранимой процедуры
                procedure_name = 'get_capacitycanada_sum1'
                cursor.execute("CALL get_capacitycanada_sum1(NULL)")

                # Получение результата процедуры
                result = cursor.fetchone()

                cursor.close()

                # Отправка результата пользователю
                if result is not None:
                    result_string = str(result)[1:-1]  # Удаление первой и последней скобки
                    result_string = result_string.replace(',', '')  # Удаление запятых
                    bot.reply_to(message, result_string)
                else:
                    bot.reply_to(message, "No data found.")
            except Exception as e:
                bot.reply_to(message, "An error occurred while fetching data.")

        @bot.message_handler(commands=['playerwght'])
        def handle_get_data(message):
            try:
                # Запрашиваем у пользователя ввод веса
                bot.reply_to(message, "Введите вес:")

                @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
                def handle_weight_input(message):
                    try:
                        weight = int(message.text)

                        # Создание объекта курсора
                        cursor = conn.cursor()

                        # Вызов хранимой процедуры
                        procedure_name = 'get_playerwght_count'
                        cursor.execute(f"CALL get_playerwght_count({weight}, NULL)")

                        # Получение результата процедуры
                        result = cursor.fetchone()

                        cursor.close()

                        # Отправка результата пользователю
                        if result is not None:
                            result_string = str(result)[1:-1]  # Удаление первой и последней скобки
                            result_string = result_string.replace(',', '')  # Удаление запятых
                            bot.reply_to(message, result_string)
                        else:
                            bot.reply_to(message, "Данные не найдены.")
                    except ValueError:
                        bot.reply_to(message, "Некорректный ввод веса.")
                    except Exception as e:
                        bot.reply_to(message, "Произошла ошибка при получении данных.")
            except Exception as e:
                bot.reply_to(message, "Произошла ошибка при получении данных.")
            # Обработчик команды /addplayer

    @bot.message_handler(commands=['addplayer'])
    def handle_add_player(message):
        try:
            # Запрашиваем у пользователя ввод информации о новом игроке
            bot.reply_to(message, "Введите информацию о новом игроке в формате: \nID игрока, \nИмя, \nНик")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_info_input(message):
                try:
                    player_info = message.text.split(', ')
                    pid = int(player_info[0])
                    name = player_info[1]
                    nik = player_info[2]


                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение INSERT-запроса для добавления нового игрока
                    cursor.execute(
                        f"insert into Человек (id,Имя,ник) values ({pid},'{name}','{nik}');")

                    conn.commit()

                    cursor.close()

                    bot.reply_to(message, "Новый игрок успешно добавлен в базу данных.")
                except ValueError:
                    bot.reply_to(message, "Некорректный ввод информации о новом игроке.")

                return
        except Exception as e:
            bot.reply_to(message, "Произошла ошибка при добавлении игрока в базу данных.")

    # Обработчик команды /playerinfo
    @bot.message_handler(commands=['playerinfo'])
    def handle_player_info(message):
        try:
            # Запрашиваем у пользователя ввод ID игрока
            bot.reply_to(message, "Введите ID игрока:")

            @bot.message_handler(func=lambda msg: msg.chat.id == message.chat.id)
            def handle_player_id_input(message):
                try:
                    player_id = int(message.text)

                    # Создание объекта курсора
                    cursor = conn.cursor()

                    # Выполнение запроса к базе данных для получения информации об игроке
                    cursor.execute(f"SELECT * FROM Человек WHERE id_player = {player_id}")
                    result = cursor.fetchone()
                    cursor.execute(f"SELECT * FROM Человек WHERE id_player = {player_id}")
                    result = cursor.fetchone()
                    cursor.execute(f"SELECT * FROM Человек WHERE id_player = {player_id}")
                    result = cursor.fetchone()

                    cursor.close()

                    if result:
                        # Форматирование информации об игроке
                        player_info = f"ID: {result[0]}\nИмя: {result[1]}\nДата рождения: {result[2]}\nГород рождения: {result[3]}\nАмплуа: {result[4]}\nРост: {result[5]}\nВес: {result[6]}\nID команды: {result[7]}\nЗарплата: {result[8]}\nУчастие в национальной сборной: {result[9]}"

                        # Отправка информации об игроке пользователю
                        bot.reply_to(message, player_info)

                    else:
                        bot.reply_to(message, "Игрок с указанным ID не найден.")
                except ValueError:
                    bot.reply_to(message, "Некорректный ввод ID игрока.")
                except Exception as e:
                    bot.reply_to(message, "Произошла ошибка при получении информации об игроке.")
                finally:
                    return  # Return to the start function

        except Exception as e:
            bot.reply_to(message, "Произошла ошибка при получении информации об игроке.")


# Запуск телеграм-бота
bot.polling()

# Закрытие соединения с базой данных
conn.close()  # 1
