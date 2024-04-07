from typing import Any
from django.db import models
from uuid import uuid4

# Create your models here.


class Address(models.Model):
    __name__ = 'Адрес'
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    zipCode = models.CharField('Почтовый индекс', max_length=100,
                               null=True)
    country = models.CharField('Страна', max_length=100, null=True)
    region = models.CharField('Регион, область', max_length=100, null=True)
    city = models.CharField('Город', max_length=100, null=True)
    street = models.CharField('Улица', max_length=100, null=True)
    house = models.CharField('Номер дома', max_length=100, null=True)
    apartment = models.CharField('Номер квартиры, офиса и т.д.',
                                 max_length=100, null=True)
    createAt = models.DateTimeField('Дата создания',
                                    auto_now=True, null=False)
    updateAt = models.DateTimeField('Дата обновления',
                                    auto_now=True, null=False)


class JobType(models.TextChoices):
    main = 'main', 'Основная работа'
    part_time = 'part-time', 'Частичная занятость'


class Job(models.Model):
    __name__ = 'Работа'
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    type = models.CharField('Тип работы', choices=JobType,
                            max_length=100, null=True)
    dateEmp = models.DateField('Дата трудоустройства', null=True)
    dateDismissal = models.DateField('Дата увольнения', null=True)
    monIncome = models.DecimalField('Доход в месяц', max_digits=10,
                                    decimal_places=2, null=True)
    tin = models.CharField('ИНН', max_length=100, null=True)
    factAddress = models.ForeignKey(Address, null=True,
                                    on_delete=models.SET_NULL,
                                    related_name='factAddress')
    jurAddress = models.ForeignKey(Address, null=True,
                                   on_delete=models.SET_NULL,
                                   related_name='jurAddress')
    phoneNumber = models.CharField('Номер телефона', max_length=20, null=True)
    createAt = models.DateTimeField(
        'Дата создания', auto_now=True, null=False)
    updateAt = models.DateTimeField(
        'Дата обновления', auto_now=True, null=False)


class Passport(models.Model):
    __name__ = 'Паспорт'
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    series = models.CharField('Серия', max_length=10, null=False)
    number = models.CharField('Номер', max_length=10, null=False)
    giver = models.CharField('Кем выдан', max_length=100, null=False)
    dateIssued = models.DateTimeField('Дата выдачи', null=False)
    createAt = models.DateTimeField(
        'Дата создания', auto_now=True, null=False)
    updateAt = models.DateTimeField(
        'Дата обновления', auto_now=True, null=False)


class Child(models.Model):
    __name__ = 'Ребенок'
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    name = models.CharField('Имя', max_length=100, null=True)
    surname = models.CharField('Фамилия', max_length=100, null=True)
    patronymic = models.CharField('Отчество', max_length=100, null=True)
    dob = models.DateTimeField('День рождения', null=True)


class CommunicationType(models.TextChoices):
    email = 'email', 'Электронная почта'
    phone = 'phone', 'Мобильный телефон'


class Communication(models.Model):
    __name__ = 'Средство связи'
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    type = models.CharField('Тип', choices=CommunicationType,
                            null=False, max_length=100)
    value = models.CharField('Значение средства связи',
                             max_length=20, null=False)


class Document(models.Model):
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)


class EducationType(models.TextChoices):
    secondary = 'secondary', 'Среднее'
    secondarySpecial = 'secondarySpecial', 'Среднее специальное'
    incompleteHigher = 'incompleteHigher', 'Незаконченное высшее'
    higher = 'higher', 'Высшее'
    twoOrMoreHigher = 'twoOrMoreHigher', 'Два и более высших образований'
    academicDegree = 'academicDegree', 'Академическая степень'


class Client(models.Model):
    id = models.UUIDField('Идентификатор', primary_key=True,
                          null=False, default=uuid4)
    name = models.CharField('Имя', max_length=100, null=True)
    surname = models.CharField('Фамилия', max_length=100, null=True)
    patronymic = models.CharField('Отчество', max_length=100, null=True)
    dob = models.DateTimeField('День рождения')
    passport = models.OneToOneField(Passport, null=True,
                                    on_delete=models.SET_NULL)
    children = models.ManyToManyField(
        Child, related_name='children', blank=True)
    documentIds = models.ManyToManyField(
        Document, blank=True, related_name='documents')
    livingAddress = models.OneToOneField(Address, null=True,
                                         on_delete=models.SET_NULL,
                                         related_name='livingAddress')
    regAddress = models.OneToOneField(Address, null=True,
                                      on_delete=models.SET_NULL,
                                      related_name='regAddress')
    jobs = models.ManyToManyField(Job, blank=True, related_name='jobs')
    typeEducation = models.CharField('Тип образования',
                                     choices=EducationType, max_length=100)
    monIncome = models.DecimalField('Суммарный доход в месяц', max_digits=10,
                                    decimal_places=2, null=True)
    monExpenses = models.DecimalField('Суммарный расход в месяц', max_digits=10,
                                      decimal_places=2, null=True)
    communications = models.ManyToManyField(
        Communication, blank=True, related_name='communications')
    createAt = models.DateTimeField(
        'Дата создания', auto_now=True, null=False)
    updateAt = models.DateTimeField(
        'Дата обновления', auto_now=True, null=False)
    spouse = models.OneToOneField(
        'self', null=True, related_name='client_spouse', on_delete=models.SET_NULL)
