# UI Element Classifier and Code Generator

Проект для автоматичного розпізнавання UI-елементів на зображеннях та генерації відповідного HTML/CSS коду.

## Зміст
- [Опис](#опис)
- [Вимоги](#вимоги)
- [Встановлення](#встановлення)
- [Запуск проекту](#запуск-проекту)
- [Структура проекту](#структура-проекту)
- [Використання](#використання)
- [Тестування](#тестування)
- [Розгортання](#розгортання)
- [Ліцензія](#ліцензія)

---

## Опис
Цей проект використовує нейромережу для класифікації UI-елементів (наприклад, кнопок, полів вводу, карток) на зображеннях. Після розпізнавання система генерує відповідний HTML/CSS код, який можна використовувати у веб-додатках. Проект включає:
- Навчання та оптимізацію моделі.
- API на FastAPI для інтеграції.
- Веб-інтерфейс для завантаження зображень та перегляду результату.

---

## Вимоги
- Python 3.8+
- Бібліотеки: див. [requirements.txt](requirements.txt)

---

## Встановлення
1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/your-username/ui2html.git
   cd ui2html
Створіть віртуальне середовище:

python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
Встановіть залежності:

pip install -r requirements.txt
### (Якщо виникають проблеми з встановленням бібліотек - виконайте окремо pip install numpy==1.26.4 )
Запуск проекту
1. Запуск сервера FastAPI
uvicorn api.main:app --reload
Сервер буде доступний за адресою: http://localhost:8000.

2. Веб-інтерфейс
Відкрийте у браузері: http://localhost:8000/static/index.html.

Структура проекту
Copy
ui2html/
├── api/               # Код FastAPI
│   ├── main.py
│   └── utils/         # Допоміжні модулі
├── dataset/           # Тренувальні дані
├── models/            # Збережені моделі
├── scripts/           # Скрипти для обробки даних та навчання
├── static/            # Веб-сторінки та стилі
├── requirements.txt
└── README.md
Використання
Завантажте зображення через веб-інтерфейс (формат: PNG/JPEG).

Отримайте результат:

Інтерактивний елемент (наприклад, кнопка).

HTML/CSS код для копіювання.

Приклад відповіді API:

json
Copy
{
  "element": "button",
  "code": "<button class='neu-button'>Click</button><style>.neu-button { ... }</style>"
}
Тестування
1. Через веб-інтерфейс
Відкрийте http://localhost:8000/static/index.html і завантажте зображення.

2. Через cURL
bash
Copy
curl -X POST -F "file=@test_image.png" http://localhost:8000/convert/
3. Через Postman
Відправте POST-запит на /convert/ з файлом у тілі запиту.

Розгортання
Для публічного доступу використовуйте хостинги на кшталт Heroku або Render:

Створіть Procfile:
web: uvicorn api.main:app --host=0.0.0.0 --port=${PORT:-8000}
Налаштуйте змінні середовища та деплойте проект.

Ліцензія
MIT License. Деталі див. у файлі LICENSE.

---