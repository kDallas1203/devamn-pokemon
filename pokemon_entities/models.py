from django.db import models


class PokemonElementType(models.Model):
    """Стихии"""
    title = models.CharField(max_length=100, verbose_name="Название")
    strong_against = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name="Силен против")

    def __str__(self):
        return self.title


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField(verbose_name='Название на русском', max_length=200)
    title_en = models.CharField(verbose_name='Название на английском', max_length=200, blank=True)
    title_jp = models.CharField(verbose_name='Название на японском', max_length=200, blank=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='images')
    level = models.IntegerField(verbose_name='Уровень', blank=True, null=True)
    health = models.IntegerField(verbose_name='Здоровье', blank=True, null=True)
    strength = models.IntegerField(verbose_name='Сила', blank=True, null=True)
    defence = models.IntegerField(verbose_name='Защита', blank=True, null=True)
    stamina = models.IntegerField(verbose_name='Выносливость', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    previous_evolution = models.ForeignKey('self', null=True, blank=True, related_name='next_evolution',
                                           on_delete=models.SET_NULL,
                                           verbose_name="Из кого эволюционирует")
    element_type = models.ManyToManyField(PokemonElementType, verbose_name="Стихии", blank=True)

    def get_entities(self):
        return PokemonEntity.objects.filter(pokemon=self)

    def get_next_evolution(self):
        return self.next_evolution.all().first()

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Расположение покемона"""
    lat = models.FloatField(verbose_name='Широта', blank=True, null=True)
    lon = models.FloatField(verbose_name='Долгота', blank=True, null=True)
    appeared_at = models.DateTimeField(verbose_name='Дата и время появления', blank=True, null=True)
    disappeared_at = models.DateTimeField(verbose_name='Дата и время исчезновения', blank=True, null=True)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.SET_NULL, verbose_name="Покемон", blank=True, null=True)
