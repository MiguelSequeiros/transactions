from datetime import datetime
from django.db.models import Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.decorators import api_view
from txs.api.serializers import CompanySerializer, AbstractSerializer, MonthAbstractSerializer
from txs.models import Company, Transaction
from copy import copy


class Abstract:
    """
    Class to handle abstracts
    """
    best_seller = None
    worst_seller = None
    most_uncharged_seller = None
    charged_amount = 0
    uncharged_amount = 0


class MonthAbstract:
    """
    Class to handle month abstracts
    """
    last_month_txs_charged = 0
    past_month_txs_charged = 0
    txs_charged_variation = 0


def get_charged_and_uncharged_amounts(transactions):
    """
    Calculates the charged and uncharged amount of a list of transactions.
    O(n)
    """
    charged_amounts = 0
    uncharged_amounts = 0
    for transaction in transactions:
        if transaction.charged:
            charged_amounts += transaction.price
        else:
            uncharged_amounts += transaction.price
    return charged_amounts, uncharged_amounts


@api_view(['GET'])
def abstract(request):
    """
    API endpoint that expose a main abstract
    """
    abstract = Abstract()

    all_companies = Company.objects.all()
    n = all_companies.count()

    # order by total sales property
    first_list = sorted(all_companies, key=lambda c: c.total_sales)
    abstract.best_seller = first_list[n-1]
    abstract.worst_seller = first_list[0]

    # order by uncharged_transactions property
    second_list = sorted(all_companies, key=lambda c: c.uncharged_transactions)
    abstract.most_uncharged_seller = second_list[n-1]
    abstract.charged_amount, abstract.uncharged_amount = get_charged_and_uncharged_amounts(
        Transaction.objects.all())

    return Response(data=AbstractSerializer(abstract).data, status=HTTP_200_OK)


class CompanyView(ListAPIView, RetrieveAPIView):
    """
    API endpoint that expose company abstract
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'


@api_view(['GET'])
def monthAbstract(request):
    """
    API endpoint that returns the sum of prices for the last and past month transactions
    This also shows the variation in percentage between the last and past month transactions
    """
    current_month = datetime.now().month
    past_mont = current_month - 1 if current_month != 1 else 12
    current_year = datetime.now().year
    past_year = current_year - 1 if current_month == 1 else current_year

    abstract = MonthAbstract()

    last_month_txs = Transaction.objects.filter(
        date__month=current_month, date__year=current_year)
    abstract.last_month_txs_charged = last_month_txs.filter(
        approved=True, state='closed').aggregate(charged=Sum('price'))['charged'] or 0
    past_month_txs = Transaction.objects.filter(
        date__month=past_mont, date__year=past_year)
    abstract.past_month_txs_charged = past_month_txs.filter(
        approved=True, state='closed').aggregate(charged=Sum('price'))['charged'] or 0

    if abstract.past_month_txs_charged != 0:
        abstract.txs_charged_variation = (
            ((abstract.last_month_txs_charged - abstract.past_month_txs_charged)/abstract.past_month_txs_charged)*100)
    else:
        txs_charged_variation = 0

    return Response(data=MonthAbstractSerializer(abstract).data, status=HTTP_200_OK)
