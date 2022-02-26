import datetime

from django.db.models import Sum
from expenses.models import Expense
from income.models import Income
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response


class ExpenseSummaryStats(ListAPIView):
    def get_category(self, expense):
        return expense.category

    def get_amount_for_category(self, expense_list, category):
        expenses = expense_list.filter(category=category)
        # result = expense.annotate(total_amount=Sum('amount'))
        # print(result)
        # return result
        amount = 0
        for expense in expenses:
            amount += expense.amount

        return {'amount': str(amount)}

    def get(self, request):
        today_date = datetime.date.today()
        year_ago_date = today_date - datetime.timedelta(days=12 * 30)
        expenses = Expense.objects.filter(
            owner=request.user, date__gte=year_ago_date, date__lte=today_date)

        final = {}

        categories = set(map(self.get_category, expenses))

        for expense in expenses:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    expenses, category)

        return Response({'category_data': final}, status=status.HTTP_200_OK)


class IncomeSummaryStats(ListAPIView):
    def get_source(self, income):
        return income.source

    def get_amount_for_source(self, income_list, source):
        income = income_list.filter(source=source)
        amount = 0
        for i in income:
            amount += i.amount

        return {'amount': str(amount)}

    def get(self, request):
        today_date = datetime.date.today()
        year_ago_date = today_date - datetime.timedelta(days=12 * 30)
        income = Income.objects.filter(
            owner=request.user, date__gte=year_ago_date, date__lte=today_date)

        final = {}

        sources = set(map(self.get_source, income))

        for inc in income:
            for source in sources:
                final[source] = self.get_amount_for_source(
                    income, source)

        return Response({'income_source_data': final}, status=status.HTTP_200_OK)
