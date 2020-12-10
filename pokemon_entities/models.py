from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(verbose_name='Название на русском', max_length=200)
    title_en = models.CharField(verbose_name='Название на английском', max_length=200, blank=True, null=True)
    title_jp = models.CharField(verbose_name='Название на японском', max_length=200, blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='images')
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    previous_evolution = models.ForeignKey('self', null=True, blank=True, related_name='next_evolution',
                                           on_delete=models.CASCADE,
                                           verbose_name="Предыдущая эволюция")

    def get_entities(self):
        return PokemonEntity.objects.filter(pokemon=self)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Расположение покемона"""
    lat = models.FloatField(verbose_name='Широта', blank=True, null=True)
    lon = models.FloatField(verbose_name='Долгота', blank=True, null=True)
    appeared_at = models.DateTimeField(verbose_name='Дата и время появления', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Дата и время исчезновения', blank=True, null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name="Покемон", blank=True, null=True)
