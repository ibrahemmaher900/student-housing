from django.core.management.base import BaseCommand
from apartments.models import University

class Command(BaseCommand):
    help = 'إنشاء الجامعات الأولية'

    def handle(self, *args, **options):
        universities = [
            {'name': 'جامعة القاهرة', 'city': 'القاهرة', 'image': 'جامعة-القاهرة.jpg'},
            {'name': 'جامعة عين شمس', 'city': 'القاهرة', 'image': 'جامعة-عين-شمس.jpg'},
            {'name': 'جامعة الإسكندرية', 'city': 'الإسكندرية', 'image': 'جامعة-الإسكندرية.jpg'},
            {'name': 'جامعة المنصورة', 'city': 'المنصورة', 'image': 'جامعة-المنصورة.jpg'},
            {'name': 'جامعة أسيوط', 'city': 'أسيوط', 'image': 'جامعة-أسيوط.jpg'},
            {'name': 'جامعة طنطا', 'city': 'طنطا', 'image': 'default-university.jpg'},
            {'name': 'جامعة الزقازيق', 'city': 'الزقازيق', 'image': 'default-university.jpg'},
            {'name': 'جامعة المنيا', 'city': 'المنيا', 'image': 'default-university.jpg'},
            {'name': 'جامعة بنها', 'city': 'بنها', 'image': 'default-university.jpg'},
            {'name': 'جامعة الفيوم', 'city': 'الفيوم', 'image': 'default-university.jpg'},
        ]

        for uni_data in universities:
            university, created = University.objects.get_or_create(
                name=uni_data['name'],
                defaults={
                    'city': uni_data['city'],
                    'image': uni_data['image']
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'تم إنشاء جامعة: {university.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'الجامعة موجودة بالفعل: {university.name}')
                )

        self.stdout.write(
            self.style.SUCCESS('تم الانتهاء من إنشاء الجامعات')
        )