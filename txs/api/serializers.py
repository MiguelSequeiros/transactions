from rest_framework import serializers
from txs.models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'charged_transactions',
                  'uncharged_transactions', 'best_day', 'total_sales')


class AbstractSerializer(serializers.Serializer):
    best_seller = CompanySerializer()
    worst_seller = CompanySerializer()
    most_uncharged_seller = CompanySerializer()
    charged_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    uncharged_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

