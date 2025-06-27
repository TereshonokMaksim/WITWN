# World IT Web Network - Соціальна мережа


<input value = "literally_what" style = "position:fixed;right:20px;top:20px;">

---

## Навігація по файлу

- [Мета проекту / Purpose of this application](#мета-розробки-цього-додатку)
- [Склад команди / Team compostion](#склад-команди)
- [Технології проекта / Project's technologies](#технології-проекту)
- [Інструкції по роботі / Instructions for launching](#інструкції-по-запуску-проекту)
- [Файлова структура / File structure](#файлова-структура-проекту)
- [Структура головних додатків / Structure of main applications](#додатки)
- [Особливості роботи проекту / Features of the project](PLACEHOLDER)
- [Посилання на додаткові ресурси / Links to additional resources](PLACEHOLDER)
- [Висновок з роботи / Conclusion of work](PLACEHOLDER)

---

## Мета розробки цього додатку:
### Цей проект дозволяє звичайним користувачам обмінюватися інформацією без перешкод - зображеннями, текстами, тощо
### Для тих, хто хоче розгортати цей проект, він може сподобатись потенційно великими можливостями монетизації
### А для нас, як для розробників, це була практика по новим [технологіям](#технології-проекту)

---

## Склад команди:
* [Терешонок Максим](https://github.com/TereshonokMaksim) - Тімлід
* [Агеєв Данило](https://github.com/Ageev-Danilo)
* [Науменко Нікіта](https://github.com/Naumenko0Nikita)

---

## Технології проекту
### Python 
#### Головна мова програмування у проекті - Відповідає повністю за бекенд
_Далі йде список фреймворків/бібліотек, котрі були використані на бекенді_
1. Django - Фреймворк для створення бекенду. У цьому проекті виконував роль шаблонізатору веб сторінок, створенню ендпоінтів та легкої роботи з базою даних.
2. Pillow (PIL) - Необхідна бібліотека для роботи з медіа файлами користувачів.
3. channels - Бібліотека, яка відповідає за створення асинхроних веб-сокетів на стороні бекенду та правильній його роботі.
4. daphne - Бібліотека, що відповідає за налаштовування асинхронної роботи Django (бекенду).
### SQL
#### Мова для роботи з реляційними базами даних. Тісно співпрацює с Django.
### HTML
#### Мова-конструктор на якій написані структури веб сторінок. Велика частина контенту до них додається за допомогою шаблонізатору Django та роботи JS.
### CSS
#### Мова для створення стилей для сторінок в HTML. 
### JS
#### Мова для створення інтерактивності на стороні фронтенду (клієнта). У нашому проекті вона використувалася для відкриття форм, створення вебсокет зв'язку, пінгу і так далі.
### Git
#### Система для керування версіями проекту та роботи учасників.
### Figma
#### Інструмент, який використовувся для створення дизайну та планів роботи учасників команди.

---

## Інструкції по запуску проекту
<details>
<summary>Інструкція по запуску проекту на локальному хості</summary>

### Як запустити проект ЛОКАЛЬНО / how to launch project LOCALLY

1. >Переконайтесь, що ви маєте версію Python >=3.11 з встановленим PIP (Package Installer for Python) / Make sure you have Python version >3.11 with PIP (Package Installer for Python) installed
2. >Встановіть цей проект собі на комп'ютер. Для цього, наведіться на зелену кнопку "<> Code" та натисність на найнижчу відкриту кнопку "Download ZIP" / Install this project on your computer. To do this, hover over the green "<> Code" button and click on the lowest open button "Download ZIP"
3. >Розархівуйте встановлену ZIP папку / Unzip the installed ZIP folder
4. >Відкрийте командний рядок у себе на комп'ютері та перейдіть у папку с проектом. Для цього відкрийте командний рядок у цій самий папці, або перейдіть у неї користуючись командою cd / Open a command prompt on your computer and navigate to the project folder. To do this, open a command prompt in the same folder, or navigate to it using the cd command.
5. >Коли ви перейшли у WITWN, напишіть цю команду / When you are in WITWN, write this command:
```bash
    pip install -f requirements.txt
    # Це встановить всі залежності у проекта (всі бібліотеки, які потрібні для нормальної роботи програми) / This will install all dependencies for the project (all libraries that are required for the program to work properly)
```
6. >Перейдіть у папку WITWN так, щоб вам був доступний файл manage.py (все ще за допомогою команди "cd") / Go to the WITWN folder so that you have access to the manage.py file (still using the "cd" command)
7. >Створіть базу даних проекту / Create a project database:
```bash
    python manage.py migrate
    # Це проведе міграції бази даних - створить всі моделі проекту та зробе його базу даних працюючою / This will perform database migrations - create all project models and make its database working
```
i. >Якщо ви маєте помилку (багато незрозумілого тексту) після використання цієї команди, використайте її ще раз, після виконання наступної команди / If you get an error (a lot of garbled text) after using this command, use it again, after running the following command:
```bash
    python manage.py makemigrations
    # Це створить міграції для бази даних. / This will create migrations for the database.
```
8. >Запустість проект / Run project:
```bash
    python manage.py runserver
    # Це запустить проект локально / This will run project locally
```
i. Якщо виникають помилки, переконайтеся, що ви не пропустили минулих пунктів / If errors occur, make sure you haven't missed any previous points.
#### Для продовження налаштування проекту, відкрийте інструкцію по обслуговуванню проекта / To continue configuring the project, open the project maintenance manual.

</details>

<details>
<summary>Інструкція по розгортанню проекту на Railway</summary>

### Це інструкція по розгортанню проекту на платформі Railway, з іншими платформами ця інструкція буде іншою

1. >Для цього вам знадобиться акаунт GitHub (набагато спрощує роботу), тому якщо ви не маєте акаунту GitHub, будь ласка, створіть зараз. Якщо ви маєте акаунт, ідіть до наступного пункту
2. >Встановіть цей проект за допомого "Code <>" або склонуйте, щоб створити с ним репозиторій на вашому акаунті
3. >Коли ви маєте цей проект на репозиторії, зайдіть у файл settings.py (що знаходиться у WITWN папці) та додайте у ALLOWED_HOSTS і CSRF_TRUSTED_ORIGINS домен вашого сайту.
4. >Перевірте змінну (константу) DEBUG у settings.py, якщо вона True то змініть обов'язково на False, щоб зробити ваш сайт безпечним від найлегших спроб взлому.
5. >Далі, створіть акаунт (якщо не маєте) на [Railway](https://railway.com/) та додайте підключення до вашого GitHub акаунту. 
6. >Після цього, зайдіть у deploy та помістить туди свій репозиторій. Він буде автоматично оновлюватись якщо ви зробите деякі зміни до свого репозиторію на GitHub.
7. >Додайте змінну у ваш деплой DJANGO_SETTINGS_MODULE та ставте значення "WITWN.settings"
8. >Далі, зайдіть у налаштування вашого деплою та ставте свій домен (або згенеруйте та замініть значення у ALLOWED_HOSTS i CSRF_TRUSTED_ORIGINS)
9. >Перейдіть на ваш домен. Якщо воно не працює, то перевірте виконання всіх пунктів. Якщо воно все ще не працює, то, можливо воно не встигло завантажитись, але якщо воно завантажилось та не працює, то це проблема у проекті.

</details>

---

## Файлова структура проекту
<details>
<summary>Розгорнути діаграму файлової структури проекту</summary>

```mermaid
%%{ init : { "theme" : "default", "flowchart" : { "curve" : "linear" } }}%%

flowchart LR

    A(WITWN_main) --> L(WITWN)
    A(WITWN_main) --> K(core_app)
    A(WITWN_main) --> J(chat_app)
    A(WITWN_main) --> I(user_app)
    A(WITWN_main) --> H(friends_app)
    A(WITWN_main) --> G(media)
    A(WITWN_main) --> F(templates)
    A(WITWN_main) --> E(Static Base)
    A(WITWN_main) --> D([db.sqlite3])
    A(WITWN_main) --> C([manage.py])


    LA(WITWN dummy):::hidden --> DB([asgi.py])
    LA(WITWN dummy):::hidden --> DC([settings.py])
    LA(WITWN dummy):::hidden --> DD([urls.py])
    LA(WITWN dummy):::hidden --> DE([wsgi.py])

    L --> LA

    KA(core_app dummy):::hidden --> KB(migrations)
    KA(core_app dummy):::hidden --> KC(Static Base)
    KA(core_app dummy):::hidden --> KD(templates/home)
    KA(core_app dummy):::hidden --> KE([apps.py])
    KA(core_app dummy):::hidden --> KF([urls.py])
    KA(core_app dummy):::hidden --> KG([utils.py])
    KA(core_app dummy):::hidden --> KH([views.py])

    KDA(core_app_htmls dummy):::hidden --> KDB([publications.html])
    KDA(core_app_htmls dummy):::hidden --> KDC([albums.html])
    KDA(core_app_htmls dummy):::hidden --> KDD([settings.html])
    KDA(core_app_htmls dummy):::hidden --> KDE(post_tags)

    KD --> KDA
    K --> KA


    JA(chat_app dummy):::hidden --> JB(migrations)
    JA(chat_app dummy):::hidden --> JC(Static Base)
    JA(chat_app dummy):::hidden --> JD(templates)
    JA(chat_app dummy):::hidden --> JE([admin.py])
    JA(chat_app dummy):::hidden --> JF([models.py])
    JA(chat_app dummy):::hidden --> JG([urls.py])
    JA(chat_app dummy):::hidden --> JH([views.py])
    JA(chat_app dummy):::hidden --> JI([forms.py])
    JA(chat_app dummy):::hidden --> JJ([consumers.py])
    JA(chat_app dummy):::hidden --> JK([routing.py])

    JDA(chat_app_htmls dummy):::hidden --> JDC([chats.html])

    JD --> JDA
    J --> JA


    IA(user_app dummy):::hidden --> IB(migrations)
    IA(user_app dummy):::hidden --> IC(Static Base)
    IA(user_app dummy):::hidden --> ID(templates)
    IA(user_app dummy):::hidden --> IE([admin.py])
    IA(user_app dummy):::hidden --> IF([models.py])
    IA(user_app dummy):::hidden --> IG([urls.py])
    IA(user_app dummy):::hidden --> IH([views.py])
    IA(user_app dummy):::hidden --> II([utils.py])
    IA(user_app dummy):::hidden --> IJ([forms.py])

    IDA(user_app_htmls dummy):::hidden --> IDB([confirmation.html])
    IDA(user_app_htmls dummy):::hidden --> IDC([login.html])
    IDA(user_app_htmls dummy):::hidden --> IDD([reg.html])
    IDA(user_app_htmls dummy):::hidden --> IDE([reg_success.html])
    IDA(user_app_htmls dummy):::hidden --> IDF(user_base)

    ID --> IDA
    I --> IA


    G(media) --> GA(images)
    GA(images) --> GB(avatars)
    GA(images) --> GB(group_avatars)
    GA(images) --> GB(messages)
    GA(images) --> GB(posts)


    F(templates) --> FA([base.html])
    F(templates) --> FA([main_base.html])


    EY(Static Base) --> EYA(css)
    EY(Static Base) --> EYB(js)
    EY(Static Base) --> EYC(images)
    EY(Static Base) --> EYD(fonts)

    EYA(css) --> EYAA([base_style.css])
    EYA(css) --> EYAA([base_main_page.css])
    EYA(css) --> EYAA([font_loader.css])
    EYB(js) --> EYBA([loader.js])
    EYC(images) --> EYCA(any images for web page)
    EYD(fonts) --> EYDA(Only in global static app, fonts)

    classDef hidden display: none

```

</details>

---

## Додатки

<details>

<summary>Пояснення до структури папки додатків</summary>

*app - Папка у якій створен веб додаток і його базові складові (інші є у папці static та templates) / The folder in which the web application and its basic components are created (others are in the static and templates folder)

    admin.py - Відповідає за реєстрацію моделі для адмін сторінки (а також за її оформлення) / Responsible for registering the model for the page admin (as well as for its design)

    apps.py - Відповідає за головну інформацію додатку для роботи Django фреймворка / Responsible for the main information of the application for the Django framework to work

    models.py - Відповідає за моделі (таблиці) у базі даних / Responsible for models (tables) in the database

    urls.py - Відповідає за встановлення посилання до сторінок, а також функцій, котрі їх оброблюють / Responsible for establishing links to pages, as well as the functions that process them

    forms.py - Відповідає за створення та перевірку на правильність форм, які пізніше використовуються для будування сторінки в html 

    consumers.py - Відповідає за створення класів вебсокетів, які активно утримують зв'язок з клієнтом на протязі усього сеансу

    routing.py - Відповідає за створення шляхів до вище споменутих вебсокетів

    views.py - Відповідає за створення ендпоінтів - функцій та класів у котрих вказано яку відповідь треба дати на запит від клієнта (користувача або JS)

    templates - Папка у якій зберігаються усі веб сторінки даного додатку / Folder in which all web pages of this application are stored

        *.html - Відповідає за конструкцію веб сторінки / Responsible for the design of the web page


project - Папка, у якій створено всі складові фундаменту проекту / Folder in which all components of the foundation of the project are created

    asgi.py - Відповідає за асинхрону роботу вебсокетів з бекендом Django

    settings.py - Відповідає за налаштування роботи бекенду / Responsible for configuring the backend

    urls.py - Відповідає за налаштування веб адресів сторінок та media файлів / Responsible for setting web addresses of pages and media files

    wsgi.py - Відповідає за синхрону роботу Django (http запити, тощо)


static - Папка у якій зберігаються усі статичні файли (js/css/картинки) / Folder in which all static files (js/css/images) are stored


    *_app - Папка яка відповідає за статичні файли вказаного додатка / The folder responsible for the static files of the specified application

        js - Папка, у якій зберігаються усі js скрипти / The folder where all js scripts are stored

            script.js - Файл з скриптом додатку / Application script file

        css - Папка, у якій зберігаються усі css стилі / The folder where all css styles are stored

            styles.css - Файл з стилями додатку / Application styles file

        images - Папка, у якій зберігаються усі зображення що НЕ змінюються протягом використання сайту

        fonts - Папка, у якій зберігаються усі шрифти / The folder where all fonts are stored
            
            *.ttf - Файл з інформацією про шрифт / Font information file


media -  Папка, у якій зберігаються усі файли, що додали користувачи (дивиться нижче). Файли також мають спеціфічну назву, яка потрібна для уникнення конфліктів про файли с однаковими назвами.

    images - Всі зображення в папці media.

        avatars - Папка, у якій зберігаються всі аватари користувачів

        group_avatars - Папка, у якій зберігаються всі аватари чат-груп

        messages - Папка, у якій зберігаються всі зображення що користувачи надіслали у повідомленнях у чатах (групових та персональних)

        posts - Папка, у якій зберігаються усі зображення, що користувачи надіслали у своїх постах (пости могуть мати багато зображень)


manage.py - Файл, який користується для роботи вас з цим проектом / The file that you use to work with this project

README.md - Файл, котрий ви зараз читаєте. Створенний для пояснювання проекту для оточуючих. / The file you are currently reading. Created to explain the project to others. 

Procfile - Файл, у якому вказані інструкції по запуску проекту для серверу Railway

requirements.txt - Файл, у якому вказані всі модулі, бібліотеки, та фреймворки, що потрібно встановити заради роботи проекту

.gitignore - Файл, у якому написані всі шляхи/імена файлів що потрібно ігнорувати перед публікацією свого репозиторію цього проекту
</details>


<details>

<summary>Натисніть, щоб побачити пояснення до додатків цього веб додатку / Click to see the explanations of the applications of this web application</summary>
<!-- NO LONGER TODO :) -->

### Home app (у коді просто home_app / in the code just home_app)
- Цей додаток відповідає за домашню сторінку, а саме за першу сторінку, що побачить користувач коли перейде на цей вебсайт / This application is responsible for the homepage, namely the first page that the user will see when they go to this website.
- Також, саме на сторінці, за яку відповідає цей додаток, користувач може оформити підписку / Also, it is on the page for which this application is responsible that the user can subscribe.

### Contacts app (у коді просто contacts_app / in the code it's just contacts_app)
- Цей додаток відповідає всього за одну сторінку, а саме за сторінку контактів / This application is responsible for only one page, namely the contacts page.
- Якщо ви хочете встановити свої контактні дані на сторінку, будь ласка, переглянте HTML шаблон у сторінці templates, та замініть потрібні посилання / If you want to set your contact details on the page, please review the HTML template in the templates page, and replace the necessary links.

### User app (у коді просто user_app)
- Цей додаток відповідає за всю роботу з системою користувачів, а також підписок / This application is responsible for all work with the user system, as well as subscriptions
- У цьому додатку є 2 сторінки - сторінка реєстрації та авторизації / This application has 2 pages - registration and authorization page
- Після реєстрації користувачу на пошту приходе повідомлення про підтвердження своєї пошти, тому одна пошта може бути тільки на один акаунт, так само як і логін / After registration, the user receives a confirmation message to their email, so one email can only be used for one account, as well as a login.
- Цей додаток містить дві моделі бази даних - Subscription та Account / This application contains two database models - Subscription and Account

### QRCode App (у коді просто qrcode_app / in the code just qrcode_app)
- Цей додаток відповідає за всю роботу з QR кодами, а саме їх створювання та управління / This application is responsible for all work with QR codes, namely their creation and management.
- При створенні QR коду, є можливість обрати колір, зображення та форму "квадратиків", докладніше у [Особливостях роботи додатків](#особливості-роботи-додатків--features-of-the-applications) / When creating a QR code, you can choose the color, image, and shape of the "squares", for more details see [Features of the applications](#особливості-роботи-додатків--features-of-the-applications)
- Всі свої QR коди користувач може побачити на сторінці My QR Codes, де він може їх завантажити або видалити с серверу, звільнивши собі місце під інший QR код. Коли його QR коди деактивовані, він може про це дізнатися по пункту Active у детальному перегляді QR коду або просто по затемненню QR коду. / The user can see all his QR codes on the My QR Codes page, where he can download or delete them from the server, freeing up space for another QR code. When his QR codes are deactivated, he can find out about it by clicking the Active item in the detailed view of the QR code or simply by darkening the QR code.
- Цей додаток містить одну модель бази даних - QRCode, яка має індивідуальний показ на сторінці адмінстрації, бо звичайний, котрий дає Django, не дуже зрозумілий / This application contains one database model - QRCode, which has an individual display on the administration page, because the regular one provided by Django is not very clear.

</details>

---

## Особливості додатків

<details>
    <summary>Детальні особливості додатків</summary>

</details>