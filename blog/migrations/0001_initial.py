import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='título')),
                ('content', models.TextField(help_text='Aceita HTML, por exemplo as tags p, h3, figure e img.', verbose_name='conteúdo (HTML)')),
                ('pub_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de postagem')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-pub_date'],
            },
        ),
    ]
