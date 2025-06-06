# Generated by Django 5.2.1 on 2025-05-10 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_common', models.CharField(max_length=255)),
                ('name_official', models.CharField(max_length=255)),
                ('cca2', models.CharField(help_text='2-letter country code ISO 3166-1 alpha-2', max_length=2, unique=True)),
                ('ccn3', models.CharField(blank=True, help_text='3-digit country code ISO 3166-1 numeric', max_length=3, null=True)),
                ('cca3', models.CharField(blank=True, help_text='3-letter country code ISO 3166-1 alpha-3', max_length=3, null=True)),
                ('cioc', models.CharField(blank=True, help_text='3-letter International Olympic Committee code', max_length=3, null=True)),
                ('capital', models.JSONField(blank=True, help_text='List of capital cities', null=True)),
                ('region', models.CharField(blank=True, max_length=100, null=True)),
                ('subregion', models.CharField(blank=True, max_length=100, null=True)),
                ('languages', models.JSONField(blank=True, help_text="Dictionary of languages, e.g., {'eng': 'English'}", null=True)),
                ('currencies', models.JSONField(blank=True, help_text="Dictionary of currencies, e.g., {'USD': {'name': '...', 'symbol': '...'}}", null=True)),
                ('population', models.PositiveIntegerField(blank=True, null=True)),
                ('flag_png_url', models.URLField(blank=True, max_length=500, null=True)),
                ('flag_svg_url', models.URLField(blank=True, max_length=500, null=True)),
                ('flag_alt_text', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name_common'],
            },
        ),
    ]
