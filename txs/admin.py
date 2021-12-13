# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from txs.models import Company, Transaction

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'company', 'price', 'date', 'state')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')