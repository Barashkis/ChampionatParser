# Описание проекта
* * *
Данный репозиторий содержит в себе файлы моего небольшого проекта - парсера сайта championat.com,
на котором публикуются новости спорта.

После запуска парсера будет вам будет предложено выбрать вид спорта и количество страниц с новостями,
которые надо извлечь из сайта.

По итогу будет создана директория *data*, в которую будут помещены HTML-страницы
сайта со всеми новостями (чтобы не долбить сайт постоянными запросами); один *json* файл,
в нем будет содержаться информация о каждой новости (а именно ее заголовок, ссылка на нее, количество комментариев,
тэг и дата публикации).

В данном проекте задействованы такие библиотеки Python (версия 3.8), как:
+ BeautifulSoup4
+ lxml
+ requests
+ json
+ os / shutil / pathlib
+ selenium

Также позже доступен *exe* файл, мало ли кому-нибудь пригодится :)

Всего доступно 2 ветки, в них расположены разные версии парсера: основанный на библиотеке
requests и selenium. Версия на requests парсит несколько страниц, версия
на selenium парсит определенную страницу.

ВАЖНО: в данном скрипте прописана остановка после каждой итерации
(итерация происходит по страницам с новостями): time.sleep(random.randint(2, 4)).
Уберите вызов этой функции, если вы не нуждаетесь в паузе между итерациями. 

Также НЕ СЛЕДУЕТ создавать в папке data какие-либо свои папки либо файлы: при следующем запуске
скрипта все содержимое директории data будет ПЕРЕЗАПИСАНО, то есть папка будет очищена для
последующего помещения в нее свежих запрашиваемых json и html файлов.
* * *
