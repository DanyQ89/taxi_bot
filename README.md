Основной функционал:

 1. Главное меню:
 • Кнопки: “Заказать такси”, “Стать водителем”, “Пополнить баланс” (если пользователь уже является водителем), “Обратная связь”.
 2. Заказать такси:
 • Шаг 1: Пассажир нажимает “Заказать такси”.
 • Шаг 2: Бот предлагает выбрать населенный пункт из списка кнопок.
 • Шаг 3: Бот предлагает выбрать “Откуда” из последних трех адресов или ввести новый адрес.
 • Шаг 4: Бот предлагает выбрать “Куда” из последних трех адресов или ввести новый адрес.
 • Шаг 5: Бот предлагает выбрать количество пассажиров с помощью кнопок.
 • Шаг 6: Бот предлагает выбрать стоимость с помощью кнопок.
 • Шаг 7: Пассажир вводит номер телефона.
 • Шаг 8: Бот подтверждает и отправляет заказ в приватный чат водителей.
 3. Стать водителем:
 • Водитель вводит команду /register_driver для регистрации.
 • Бот сохраняет данные водителя и добавляет его в приватный чат.
 4. Пополнить баланс:
 • Если пользователь уже является водителем, кнопка “Пополнить баланс” выводит сообщение с инструкциями о том, как пополнить баланс.
 5. Обратная связь:
 • Пользователь может отправить сообщение администратору через бот.

Функционал для пассажиров:

 1. Создание заказа:
 • Пассажир вводит данные последовательно: населенный пункт, “Откуда”, “Куда”, количество пассажиров, стоимость, номер телефона.
 • Бот парсит сообщения и отправляет заказ в приватный чат водителей.
 2. Подтверждение заказа:
 • После успешного парсинга и отправки заказа, пассажиру отправляется сообщение о том, что его заказ принят в обработку.
 3. Уведомления:
 • Пассажир получает уведомление, когда водитель принимает его заказ, сколько у водителя уже пассажиров, и когда водитель набирает новых пассажиров.
 4. Быстрый набор:
 • При заказе такси пассажиру предлагаются кнопки с последними тремя адресами для быстрого набора.

Функционал для водителей:

 1. Регистрация водителя:
 • Водитель вводит команду /register_driver для регистрации.
 • Бот сохраняет данные водителя и добавляет его в приватный чат.
 2. Приватный чат для водителей:
 • Заказы, отправленные пассажирами, публикуются в приватном чате для водителей.
 • Водитель видит только те заказы, которые соответствуют количеству свободных мест в его машине и фильтру по населенным пунктам.
 3. Фильтрация заказов по населенным пунктам:
 • В чате для водителей должна быть возможность фильтровать заказы по населенным пунктам с помощью кнопок с названиями населенных пунктов.
 4. Принятие заказа:
 • В каждом сообщении с заказом в приватном чате водителей должна быть кнопка “Принять заказ”. При нажатии на кнопку водитель подтверждает принятие заказа.
 5. Уведомления и управление поездкой:
 • После принятия заказа водителю отправляется сообщение с данными заказа и кнопкой “Я еду”.
 • При нажатии кнопки “Я еду” пассажиру отправляется уведомление о выезде, указывая количество пассажиров у водителя.
 • При нажатии кнопки “Завершить поездку” пассажиру отправляется уведомление о завершении поездки.
 6. Удаление сообщения:
 • Сообщение с принятым заказом должно содержать неактивную кнопку “Заказ принят” и удаляться через 20 минут.
 7. Баланс водителя:
 • У каждого водителя должен быть баланс, с которого изымается определенная сумма за каждого пассажира. Водитель может пополнить баланс через инструкцию, доступную через кнопку “Пополнить баланс”.

Админ панель:

 1. Просмотр статистики: Возможность просматривать статистику заказов и активности водителей.
 2. Управление водителями:
 • Добавление и удаление водителей.
 • Управление балансом водителей (добавление и снятие средств).
 • Просмотр баланса водителей.
 3. Обратная связь: Возможность просматривать и отвечать на сообщения от пользователей.
