# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.db.models import Sum
from django.db.models.aggregates import Count
from django.db.models.functions import TruncDate

# Create your models here.


class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    @property
    def charged_transactions(self):
        return self.transactions.filter(approved=True, state='closed').aggregate(Count('id'))['id__count'] or 0

    @property
    def uncharged_transactions(self):
        return self.transactions.exclude(approved=True, state='closed').aggregate(Count('id'))['id__count'] or 0

    @property
    def total_sales(self):
        return self.transactions.filter(approved=True, state='closed').aggregate(Sum('price'))['price__sum'] or 0

    @property
    def best_day(self):
        return self.transactions.all().annotate(day=TruncDate('date')).values(
            'day').annotate(f=Count('id')).values('day', 'f').order_by('-f')[0]


def get_real_price(price):
    # here we can add some logic to convert the price
    return price


TX_STATE_CHOICES = (
    ('pending', 'Pending'),
    ('closed', 'Closed'),
    ('reversed', 'Reversed'),
)


class Transaction(models.Model):
    """
    Transaction model
    """
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    company = models.ForeignKey(
        Company, on_delete=models.PROTECT, related_name='transactions')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    state = models.CharField(
        max_length=8, choices=TX_STATE_CHOICES, default='pending')
    approved = models.BooleanField(default=False)

    @property
    def charged(self):
        return self.approved and self.state == 'closed'

    @property
    def real_price(self):
        return get_real_price(self.price)
