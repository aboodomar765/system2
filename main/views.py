

from django.db.models import Sum
from .forms import CarForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from .models import Car ,Expense
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('car_list')
        else:
            return render(request, 'main/login.html', {
                'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
            })

    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def car_list(request):
    return render(request, 'main/car_list.html')


def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.delete()
    return redirect('car_list')

def add_car(request):
    form = CarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('car_list')
    return render(request, 'main/add_car.html', {'form': form})

def car_list(request):
    cars = Car.objects.all()

    name = request.GET.get('name')
    chassis = request.GET.get('chassis')
    status = request.GET.get('status')

    if name:
        cars = cars.filter(name__icontains=name)

    if chassis:
        cars = cars.filter(chassis_number__icontains=chassis)

    if status in ['sold', 'unsold']:
        cars = cars.filter(status=status)

    return render(request, 'main/car_list.html', {'cars': cars})



def sell_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        car.sale_date = request.POST.get('sale_date')
        car.sale_price = request.POST.get('sale_price')
        car.status = 'sold'
        car.save()
        return redirect('sold_cars')

    return render(request, 'main/sell_car.html', {'car': car})

def  partial_profit(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == 'POST':
        car. partial_profit = request.POST.get('partial_profit')
        car.save()
        return redirect('sold_cars')

    return render(request, 'main/profit.html', {'car': car})



def sold_cars(request):
    cars = Car.objects.filter(status='sold')

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    if start_date and end_date:
        cars = cars.filter(sale_date__range=[start_date, end_date])
    return render(request, 'main/sold_cars.html', {'cars': cars})




def expense (request):
    # إذا كان المستخدم يرسل بيانات (إضافة مصروف)
    if request.method == 'POST':
        Expense.objects.create(
            description=request.POST.get('description'),
            amount=request.POST.get('amount'),
            expense_date=request.POST.get('expense_date')
        )
        # بعد الحفظ، يفضل عمل redirect لنفس الصفحة لمنع تكرار الإرسال عند التحديث
        return redirect('expense')

    expenses = Expense.objects.all()
    
    return render(request, 'main/expense.html', {
    
        'expenses': expenses # تأكد من أن الاسم هنا 'expenses' بالجمع ليطابق التمبلت
    })




def dashboard (request):
    cars = Car.objects.filter(status='sold')
    expenses = Expense.objects.all()

    start = request.GET.get('start')
    end = request.GET.get('end')

    if start and end:
        cars = cars.filter(sale_date__range=[start, end])
        expenses = expenses.filter(expense_date__range=[start, end])

    total_partial_profit = cars.aggregate(
        Sum('partial_profit')
    )['partial_profit__sum'] or 0

    total_expenses = expenses.aggregate(
        Sum('amount')
    )['amount__sum'] or 0

    net_profit = total_partial_profit - total_expenses

    context = {
        'total_partial_profit': total_partial_profit,
        'total_expenses': total_expenses,
        'net_profit': net_profit,
    }

    return render(request, 'main/dashboard.html', context)




