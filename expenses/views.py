from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences

import json
from django.http import JsonResponse, HttpResponse

import csv
import xlwt
from weasyprint import HTML
import tempfile
from django.template.loader import render_to_string
from django.db.models import Sum

import datetime
# Create your views here.

def search_expenses(request):
    if request.method =="POST":
        
        search_string = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(amount__istartswith=search_string,owner=request.user) | Expense.objects.filter(date__istartswith=search_string,owner=request.user)| Expense.objects.filter(description__icontains=search_string,owner=request.user) | Expense.objects.filter(category__icontains=search_string,owner=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data),safe=False)



@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency_exists = UserPreferences.objects.filter(user=request.user).exists()
    if currency_exists:
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = UserPreferences.objects.create(user=request.user, currency='CAD - Canadian Dollar')
    context={
        'expenses':expenses,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request,'expenses/index.html',context)

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories':categories
    }
    
    if request.method =="POST":
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense-date']
        category = request.POST['category']

        if not amount:
            messages.error(request,"Amount is Required")
            return render(request,'expenses/add_expense.html',context)
        
        if not description:
            messages.error(request,"Desciption is Required")
            return render(request,'expenses/add_expense.html',context)
        
        if not date:
            messages.error(request,"Date is Required")
            return render(request,'expenses/add_expense.html',context)
        
        Expense.objects.create(owner=request.user, amount=amount,date=date,category=category,description=description)
        messages.success(request,"Expense Saved Successfully!")
        return redirect('expenses')

    if request.method == "GET":
        return render(request,'expenses/add_expense.html',context)

def expense_edit(request,id):
    expense=Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense':expense,
        'values':expense,
        'categories':categories,
     
    }

    if request.method =='GET':
        return render(request,"expenses/edit-expense.html",context)
    
    if request.method =='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense-date']
        category = request.POST['category']

        if not amount:
            messages.error(request,"Amount is Required")
            return render(request,'expenses/edit-expense.html',context)
        
        if not description:
            messages.error(request,"Desciption is Required")
            return render(request,'expenses/edit-expense.html',context)
        
        if not date:
            messages.error(request,"Date is Required")
            return render(request,'expenses/edit-expense.html',context)
        
        expense.owner = request.user
        expense.amount = amount
        expense.date=date
        expense.category = category
        expense.description = description
        expense.save()
        messages.info(request,"Expense Updated Successfully!")
        return redirect('expenses')
        
def delete_expense(request,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.info(request,'Expense Removed')
    return redirect('expenses')

def expense_category_summary(request):
    todayDate = datetime.date.today()
    sixmonthAgo = todayDate - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user,date__gte=sixmonthAgo,date__lte=todayDate)
    finalrep = {}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category,expenses))) #set removes the duplicate

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount+=item.amount
        return amount
    
    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)
    return JsonResponse({'expense_category_data':finalrep},safe=False)

def statsView(request):
    return render(request,'expenses/expensestats.html')

def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    #content-disposition addes meta data within browser and how to handle the file
    response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.csv' 
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount,expense.description,expense.category,expense.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses'+str(datetime.datetime.now())+'.xls' 

    workbook = xlwt.Workbook(encoding='utf-8')
    workSheet = workbook.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['Amount','Description','Category','Date']

    for col_num in range(len(columns)):
        workSheet.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()
    rows = Expense.objects.filter(owner=request.user).values_list('amount','description','category','date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            workSheet.write(row_num,col_num,str(row[col_num]),font_style)
        
    workbook.save(response)
    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition']='inline; attachment; filename=Expenses'+str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    expenses = Expense.objects.filter(owner=request.user)
    sum = expenses.aggregate(Sum('amount')) 
    html_string = render_to_string('expenses/pdf-output.html',{'expenses':expenses,'total':sum['amount__sum']})
    

    html = HTML(string = html_string)
    result = html.write_pdf()


    #using context manager
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response
