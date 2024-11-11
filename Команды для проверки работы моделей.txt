Информация по подготовке скрипта к работе:
• Все необходимые библиотеки для работы скрипта находятся в файле "requirements.txt"
• Проект использует файл ".env" с переменными окружения и СУБД Postgres.
• Для корректной работы необходимо создать свой файл ".env" и поместить в директорию с файлом "manage.py", задать свои переменные окружения по следующему примеру:
	SECRET_KEY_DJANGO = '<Ваш секретный код от DJANGO>'
	NAME = '<Ваше имя базы данных>'
	USER = '<Имя пользователя>'
	PASSWORD = '<Пароль пользователя>'
	HOST =  '<Хост базы данных>'
	PORT = '5432'

Команды для проверки работы моделей в Django shell:
• Создать двух пользователей (с помощью метода User.objects.create_user('username')).
	user1 = User.objects.create_user('Игорь', password='1385', is_superuser=False, is_staff=False)
	user2 = User.objects.create_user('Петя', password='0000', is_superuser=False, is_staff=False)
• Создать два объекта модели Author, связанные с пользователями.
	Два объекта модели Author, создаются автоматически, используется связь один к одному и метод "post_save" при создании объектов встроенной модели User.
	Получаем объекты:
	author1 = Author.objects.get(pk=1)
	author2 = Author.objects.get(pk=2)
• Добавить 4 категории в модель Category. Использую созданный заранее список с категориями и значение по умолчанию 'NEW'.
	category1 = Category.objects.create(name_category='CUL') 
	category2 = Category.objects.create(name_category='POL') 
	category3 = Category.objects.create(name_category='SOC') 
	category4 = Category.objects.create(name_category='TEC')
• Добавить 2 статьи и 1 новость.
	article1 = Post.objects.create(author_post=author1, type_post='AR', title_post='Не самые популярные методы Django ORM',text_post='')
	article2 = Post.objects.create(author_post=author1, type_post='AR', title_post='35 эффектных, забавных и глубоких афоризмов от Оскара Уайльда',text_post='')
	news1 = Post.objects.create(author_post=author1, type_post='NE', title_post='В 11 районах Москвы изменились автобусные и электробусные 			маршруты',text_post='Автобусные и электробусные маршруты изменили в 11 районах Москвы, заявил заммэра столицы по вопросам транспорта и промышленности Максим 	Ликсутов')
• Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
	article1.category_post.add(category4)
	article1.category_post.add(category3)
	article2.category_post.add(category1)
	news1.category_post.add(category1)
	news1.category_post.add(category3)
	news1.category_post.add(category4)
• Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
	comment1 = Comment.objects.create(post_comment=article1, user_comment=author1.user, text_comment='Отлично, буду знать.')
	comment2 = Comment.objects.create(post_comment=article1, user_comment=author2.user, text_comment='Полезно, надо запомнить.')
	comment3 = Comment.objects.create(post_comment=article2, user_comment=author1.user, text_comment='Бесполезно((')
	comment5 = Comment.objects.create(post_comment=news1, user_comment=author1.user, text_comment='Опять что-то поменяли!')
	comment6 = Comment.objects.create(post_comment=news1, user_comment=author2.user, text_comment='Отлично! Станет удобнее добираться до работы')
• Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
	comment1.like()
	comment1.dislike()
	comment2.like()
	comment3.like() 
	comment4.like() 
	comment4.dislike()
	comment3.dislike()
	article1.like()
	article2.like() 
	news1.like()
	news1.dislike()
	article1.dislike()
• Обновить рейтинги пользователей.
	author1.update_rating()
	author2.update_rating()
• Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
	f"Лучший пользователь: {Author.objects.get(user_id=Author.objects.order_by("-rating_user").values_list('user', 'rating_user').first()[0]).user.username} с рейтингом {Author.objects.order_by("-rating_user").values_list('user', 'rating_user').first()[1]}"
• Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
	f"Лучшая статья: дата создания: {datetime.datetime.strftime(Post.objects.order_by("-rating_post").values('time_in_post').first()['time_in_post'], '%d.%m.%Y %H:%M:%S')}, автор: {Author.objects.get(pk=Post.objects.order_by("-rating_post").values('author_post').first()['author_post']).user.username}, рейтинг: {Post.objects.order_by("-rating_post").values('rating_post').first()['rating_post']}, заголовок: {Post.objects.order_by("-rating_post").values('title_post').first()['title_post']}, превью: {Post.objects.order_by("-rating_post").first().preview()}"
• Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
	Post.objects.order_by("-rating_post").first().comment_set.all().values_list('time_in_comment', 'user_comment', 'rating_comment', 'text_comment')