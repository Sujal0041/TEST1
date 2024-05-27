from django.views.generic.edit import CreateView
from .models import FinanceTransaction, Wallet
from django.http import JsonResponse
from .serializers import FinanceTransactionSerializer, WalletSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics
from django.db import models
from category.models import Category
from goals.models import Goal
from django.http import Http404


class TransactionCreateView(APIView):
    def post(self, request):
        data = request.data

        print(data)
        data.update({"user": self.request.user.id})
        
       
        categories = Category.objects.values_list('id', flat=True)
        
      
        category_id = data.get('category')
        if category_id not in categories:
          
            last_category_id = Category.objects.latest('id').id
            print("KANSDLKAN",last_category_id)
            print("KANSDLKAN",category_id)
            category_id -= last_category_id
        
    
        goals = Goal.objects.all()
        
    
        for goal in goals:
            print("Goal", goal.id)
            print("Category",category_id)
            if goal.id == category_id:
               
                print(goal.remaining_amount)
                goal.remaining_amount -= data.get('amount')
                print(data.get('amount'))
                goal.save()

                
                data['category'] = 12
                break
        
        
     
        serializer = FinanceTransactionSerializer(data=data)
        if serializer.is_valid():
            transaction = serializer.save()
           
            wallet = transaction.wallet
            if transaction.type == 'income':
                wallet.amount += transaction.amount
            elif transaction.type == 'expense':
                wallet.amount -= transaction.amount
            wallet.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAllTransactionsView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        print(request.user)
        transactions = FinanceTransaction.objects.filter(user=request.user)
        serializer = FinanceTransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

class WalletListCreateView(APIView):
    def post(self, request):
        try:
            user = request.user
            data = request.data
            data.update({'user': user.id})
            print(data)
            serializer = WalletSerializer(data=data)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)  # Print serializer errors for debugging
            import traceback
            traceback.print_exc()  # Print traceback for debugging
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetAllWalletsView(generics.ListAPIView):
    serializer_class = WalletSerializer

    def get_queryset(self):
        user = self.request.user
        print(user)
        queryset = Wallet.objects.filter(user=user)
        return queryset
    

class WalletCategoryTransactionTotal(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        user = self.request.user
        wallet_id = self.kwargs['wallet_id']
        category_id = self.kwargs['category_id']
        queryset = FinanceTransaction.objects.filter(wallet_id=wallet_id, category_id=category_id, user_id=user.id)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total = queryset.aggregate(models.Sum('amount'))['amount__sum'] or 0
        data = {'total': total}
        return Response(data)
    
class TransactionUpdateView(APIView):
    def get_object(self, pk):
        try:
            return FinanceTransaction.objects.get(pk=pk)
        except FinanceTransaction.DoesNotExist:
            raise Http404

    def patch(self, request, pk, format=None):
        transaction = self.get_object(pk)
        original_amount = transaction.amount
        original_type = transaction.type
        serializer = FinanceTransactionSerializer(transaction, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_transaction = serializer.save()

            # Update the wallet based on the changes in the transaction
            wallet = updated_transaction.wallet
            if original_type == 'income':
                wallet.amount -= original_amount
            elif original_type == 'expense':
                wallet.amount += original_amount

            if updated_transaction.type == 'income':
                wallet.amount += updated_transaction.amount
            elif updated_transaction.type == 'expense':
                wallet.amount -= updated_transaction.amount

            wallet.save()
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        transaction = self.get_object(pk)
        wallet = transaction.wallet

        # Adjust wallet balance before deleting the transaction
        if transaction.type == 'income':
            wallet.amount -= transaction.amount
        elif transaction.type == 'expense':
            wallet.amount += transaction.amount

        transaction.delete()
        wallet.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

class WalletDeleteView(APIView):
    def get_object(self, pk):
        try:
            return Wallet.objects.get(pk=pk, user=self.request.user)
        except Wallet.DoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        wallet = self.get_object(pk)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WalletUpdateView(APIView):
    def get_object(self, pk):
        try:
            return Wallet.objects.get(pk=pk, user=self.request.user)
        except Wallet.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        wallet = self.get_object(pk)
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
