from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Source, UserIncome
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

def search_income(request):
    if request.method =="POST":
        
        search_string = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(amount__istartswith=search_string,owner=request.user) | UserIncome.objects.filter(date__istartswith=search_string,owner=request.user)| UserIncome.objects.filter(description__icontains=search_string,owner=request.user) | UserIncome.objects.filter(incomeSource__icontains=search_string,owner=request.user)
        
        data = income.values()
        return JsonResponse(list(data),safe=False)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income,5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    currency_exists = UserPreferences.objects.filter(user=request.user).exists()
    if currency_exists:
        currency = UserPreferences.objects.get(user=request.user).currency
    else:
        currency = UserPreferences.objects.create(user=request.user, currency='NPR - Nepalese Rupee')
    context={
        'income':income,
        'page_obj':page_obj,
        'currency':currency,
    }
    return render(request,'income/index.html',context)

def add_income(request):
    incomeSource = Source.objects.all()
    context = {
        'incomeSource':incomeSource
    }
    
    if request.method =="POST":
        amount = request.POST['amount']
        date = request.POST['income-date']
        description = request.POST['description']
        incomeSource = request.POST['income-source']

        if not amount:
            messages.error(request,"Amount is Required")
            return render(request,'income/add_income.html',context)
        
        if not description:
            messages.error(request,"Desciption is Required")
            return render(request,'income/add_income.html',context)
        
        if not date:
            messages.error(request,"Date is Required")
            return render(request,'income/add_income.html',context)
        
        UserIncome.objects.create(owner=request.user, amount=amount,date=date,description=description,incomeSource=incomeSource)
        messages.success(request,"Income Saved Successfully!")
        return redirect('income')

    if request.method == "GET":
        return render(request,'income/add_income.html',context)

@login_required(login_url='/authentication/login')
def income_edit(request,id):
    income=UserIncome.objects.get(pk=id)
    incomeSource = Source.objects.all()
    context = {
        'income':income,
        'values':income,
        'incomeSource':incomeSource,
     
    }

    if request.method =='GET':
        return render(request,"income/edit-income.html",context)
    
    if request.method =='POST':

        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income-date']
        incomeSource = request.POST['income-source']

        if not amount:
            messages.error(request,"Amount is Required")
            return render(request,'income/edit-income.html',context)
        
        if not description:
            messages.error(request,"Desciption is Required")
            return render(request,'income/edit-income.html',context)
        
        if not date:
            messages.error(request,"Date is Required")
            return render(request,'income/edit-income.html',context)
        
        income.owner = request.user
        income.amount = amount
        income.date=date
        income.incomeSource = incomeSource
        income.description = description
        income.save()
        messages.info(request,"Income Updated Successfully!")
        return redirect('income')
    
@login_required(login_url='/authentication/login')    
def delete_income(request,id):
    income=UserIncome.objects.get(pk=id)
    income.delete()
    messages.info(request,'Record Removed')
    return redirect('income')


def income_source_summary(request):
    todayDate = datetime.date.today()
    sixmonthAgo = todayDate - datetime.timedelta(days=30*6)
    incomes = UserIncome.objects.filter(owner=request.user,date__gte=sixmonthAgo,date__lte=todayDate)
    finalrep = {}

    def get_source(incomes):
        return incomes.incomeSource
    source_list = list(set(map(get_source,incomes))) #set removes the duplicate

    def get_income_category_amount(category):
        amount = 0
        filtered_by_category = incomes.filter(incomeSource=category)

        for item in filtered_by_category:
            amount+=item.amount
        return amount
    
    for x in incomes:
        for y in source_list:
            finalrep[y]=get_income_category_amount(y)
    return JsonResponse({'income_source_data':finalrep},safe=False)

def incomeStatsView(request):
    return render(request,'income/incomestats.html')


def export_csv(request):
    response = HttpResponse(content_type='text/csv')

    #content-disposition addes meta data within browser and how to handle the file
    response['Content-Disposition']='attachment; filename=Income'+str(datetime.datetime.now())+'.csv' 
    writer = csv.writer(response)
    writer.writerow(['Amount','Description','Category','Date'])

    incomes = UserIncome.objects.filter(owner=request.user)

    for income in incomes:
        writer.writerow([income.amount,income.description,income.incomeSource,income.date])

    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Income'+str(datetime.datetime.now())+'.xls' 

    workbook = xlwt.Workbook(encoding='utf-8')
    workSheet = workbook.add_sheet('Income')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold=True

    columns = ['Amount','Description','Sources','Date']

    for col_num in range(len(columns)):
        workSheet.write(row_num,col_num,columns[col_num],font_style)
    
    font_style=xlwt.XFStyle()
    rows = UserIncome.objects.filter(owner=request.user).values_list('amount','description','incomeSource','date')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            workSheet.write(row_num,col_num,str(row[col_num]),font_style)
        
    workbook.save(response)
    return response

def export_pdf(request):
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition']='inline; attachment; filename=Income'+str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding']='binary'

    income = UserIncome.objects.filter(owner=request.user)
    sum = income.aggregate(Sum('amount')) 
    html_string = render_to_string('income/pdf-output.html',{'income':income,'total':sum['amount__sum']})
    

    html = HTML(string = html_string)
    result = html.write_pdf()


    #using context manager
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response