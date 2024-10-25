print('начнем дз 8 ')
import sqlite3

# Создаем и подключаемся к базе данных SQLite
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# 1. Создать таблицу countries
cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    )
''')

# 2. Добавить 3 записи в таблицу countries
cursor.executemany('''
    INSERT INTO countries (title) VALUES (?)
''', [('Кыргызстан',), ('Германия',), ('Китай',)])

# 3. Создать таблицу cities
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        area REAL DEFAULT 0,
        country_id INTEGER,
        FOREIGN KEY (country_id) REFERENCES countries(id)
    )
''')

# 4. Добавить 7 городов
cursor.executemany('''
    INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)
''', [
    ('Бишкек', 127, 1),
    ('Ош', 182, 1),
    ('Берлин', 891.8, 2),
    ('Мюнхен', 310.7, 2),
    ('Пекин', 16410.5, 3),
    ('Шанхай', 6340.5, 3),
    ('Гуанчжоу', 7434.4, 3),
])

# 5. Создать таблицу students
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        city_id INTEGER,
        FOREIGN KEY (city_id) REFERENCES cities(id)
    )
''')

# 6. Добавить 15 учеников
cursor.executemany('''
    INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)
''', [
    ('Айбек', 'Асанов', 1),
    ('Жамиля', 'Ахмедова', 2),
    ('Ханс', 'Мюллер', 3),
    ('Лиза', 'Шмитт', 3),
    ('Анна', 'Краус', 4),
    ('Чжан', 'Вей', 5),
    ('Ли', 'Чен', 6),
    ('Фан', 'Юн', 5),
    ('Сун', 'Ли', 7),
    ('Кайрат', 'Беков', 1),
    ('Алия', 'Мусаева', 2),
    ('Макс', 'Маер', 3),
    ('Юли', 'Фишер', 4),
    ('Ван', 'Фей', 5),
    ('Джан', 'Мэн', 6),
])

conn.commit()


# 7. Программа для отображения учеников по выбранному id города
def show_students_by_city():
    while True:
        print(
            "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")

        # 8. Отобразить список городов
        cursor.execute("SELECT id, title FROM cities")
        cities = cursor.fetchall()
        for city in cities:
            print(f"{city[0]} - {city[1]}")

        try:
            city_id = int(input("Введите id города: "))
        except ValueError:
            print("Введите корректный номер.")
            continue

        if city_id == 0:
            break

        # 9. Найти и отобразить учеников по выбранному городу
        cursor.execute('''
            SELECT s.first_name, s.last_name, c.title AS country, ci.title AS city, ci.area
            FROM students s
            JOIN cities ci ON s.city_id = ci.id
            JOIN countries c ON ci.country_id = c.id
            WHERE ci.id = ?
        ''', (city_id,))

        students = cursor.fetchall()
        if students:
            print("\nУченики:")
            for student in students:
                print(
                    f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь: {student[4]}")
            print("\n")
        else:
            print("В этом городе нет учеников.\n")


# Запуск программы
show_students_by_city()

# Закрываем соединение с базой данных
conn.close()