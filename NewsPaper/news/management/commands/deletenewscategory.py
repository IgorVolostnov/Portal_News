import logging
from django.core.management.base import BaseCommand
from ..list_post import Generator

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Удалить все новости по заданной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все посты в категории {options["category"]}? yes/no')
        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        else:
            generator_data = Generator()
            check_done = generator_data.delete_post_by_category(my_category=options['category'])
            if check_done:
                self.stdout.write(self.style.SUCCESS(f'Успешно удалены все посты из категории: {options['category']}'))
            else:
                self.stdout.write(self.style.ERROR(f'Не найдена категория: {options['category']}'))