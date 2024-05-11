from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from datetime import date
from collections import defaultdict
from decimal import Decimal

# Create your views here.

def index(request):
    return render(request, 'index.html')

#Manager

def est_list(request):
    establishments = Establishment.objects.all()
    if request.method == 'POST':
        establishment_form = EstablishmentForm(request.POST, request.FILES)
        if establishment_form.is_valid():
            establishment_form.save()
            return redirect('est')
    else:
        establishment_form = EstablishmentForm()
    context = {
        'establishment_form': establishment_form,
        'establishments': establishments
    }
    return render(request, 'est.html', context)

def establishment_edit(request, pk):
    establishment = get_object_or_404(Establishment, pk=pk)
    if request.method == "POST":
        form = EstablishmentForm(request.POST, request.FILES, instance=establishment)
        if form.is_valid():
            establishment = form.save()
            return redirect('est')
    else:
        form = EstablishmentForm(instance=establishment)
    return render(request, 'est_edit.html', {'form': form})

def delete_est(request, pk):
    estabs = get_object_or_404(Establishment, pk=pk)
    estabs.delete()
    return redirect('est')

def establishment_detail(request, establishment_id):
    establishment = get_object_or_404(Establishment, id=establishment_id)
    couriers = EstCouriers.objects.filter(establishment=establishment)

    if request.method == 'POST':
        courier_form = EstCouriersForm(request.POST)
        if courier_form.is_valid():
            # Сохраняем значение заведения вручную
            est_courier = courier_form.save(commit=False)
            est_courier.establishment = establishment
            est_courier.save()
            return redirect('establishment_detail', establishment_id=establishment_id)
    else:
        courier_form = EstCouriersForm()

    context = {
        'establishment': establishment,
        'couriers': couriers,
        'courier_form': courier_form,
    }
    return render(request, 'establishment_detail.html', context)

def couriers(request):
    courier_list = Courier.objects.all()
    if request.method == 'POST':
        form = CourierForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'], email=form.cleaned_data['email'], password=form.cleaned_data['password'])
            courier = form.save(commit=False)
            courier.user = user
            courier.save()
            return redirect('couriers')
    else:
        form = CourierForm()
    context = {'form': form, 'courier_list': courier_list}
    return render(request, 'couriers.html', context)

def couriers_edit(request, pk):
    couriers = get_object_or_404(Courier, pk=pk)
    if request.method == "POST":
        form = CourierForm(request.POST, request.FILES, instance=couriers)
        if form.is_valid():
            couriers = form.save()
            return redirect('couriers')
    else:
        form = CourierForm(instance=couriers)
    return render(request, 'couriers_edit.html', {'form': form})

def delete_courier(request, pk):
    cours = get_object_or_404(Courier, pk=pk)
    cours.delete()
    return redirect('couriers')

def show_route_map(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.route_link:
        return redirect(order.route_link)

    geolocator = ArcGIS(timeout=5)
    location_origin = geolocator.geocode(order.origin)
    location_destination = geolocator.geocode(order.destination)

    G = ox.graph_from_place('Караганда, Карагандинская область, Казахстан', network_type='walk')
    node_origin = ox.distance.nearest_nodes(G, location_origin.longitude, location_origin.latitude)
    node_destination = ox.distance.nearest_nodes(G, location_destination.longitude, location_destination.latitude)
    shortest_path = nx.shortest_path(G, node_origin, node_destination, weight='length')

    m = folium.Map(location=[location_origin.latitude, location_origin.longitude], zoom_start=14)
    folium.Marker(location=[location_origin.latitude, location_origin.longitude], popup="Отправление", icon=folium.Icon(color='red')).add_to(m)
    folium.Marker(location=[location_destination.latitude, location_destination.longitude], popup="Назначение", icon=folium.Icon(color='blue')).add_to(m)
    route_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in shortest_path]
    folium.PolyLine(locations=route_coordinates, color='blue').add_to(m)

    map_html = m._repr_html_()
    return render(request, 'show_route_map.html', {'map_html': map_html})

def schedule(request):
    establishments = Establishment.objects.all()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = ScheduleForm()
    return render(request, 'schedule.html', {'form': form, 'establishments': establishments})

def view_schedule(request, establishment_id):
    establishment = Establishment.objects.get(id=establishment_id)
    schedule = Schedule.objects.filter(est=establishment)
    return render(request, 'view_schedule.html', {'establishment': establishment, 'schedule': schedule})

def schedule_edit(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    if request.method == "POST":
        form = ScheduleForm(request.POST, request.FILES, instance=schedule)
        if form.is_valid():
            schedule = form.save()
            return redirect('schedule')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request, 'schedule_edit.html', {'form': form})

def delete_schedule(request, pk):
    schedule = get_object_or_404(Schedule, pk=pk)
    schedule.delete()
    return redirect('schedule')

def order(request):
    orders = Order.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            return redirect('orders')
    else:
        form = OrderForm()
    context = {'orders': orders,
               'form': form}
    return render(request, 'orders.html', context)

def order_detail(request, order_id):
    orders = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'orders': orders})

def delete_order(request, order_id):
    orders = get_object_or_404(Order, pk=order_id)
    orders.delete()
    return redirect('orders')

def salary_calculator(request):
    if request.method == 'POST':
        form = SalaryCalculatorForm(request.POST)
        if form.is_valid():
            courier = form.cleaned_data['courier']
            schedule = Schedule.objects.filter(courier=courier)
            salary_list = []
            for item in schedule:
                working_hours = (item.end_time.hour - item.start_time.hour) + (item.end_time.minute - item.start_time.minute) / 60
                salary = working_hours * form.cleaned_data['money_per_hour']
                salary_list.append((item.date, working_hours, salary))
            return render(request, 'setsalary.html', {'form': form, 'salary_list': salary_list})
    else:
        form = SalaryCalculatorForm()
    return render(request, 'setsalary.html', {'form': form})


#Courier

def dashboard(request):
    current_courier = request.user.courier
    establishment_ids = EstCouriers.objects.filter(courier=current_courier).values_list('establishment_id', flat=True)
    orders = Order.objects.filter(sender_id__in=establishment_ids, status='Обработан')
    return render(request, 'dashboard.html', {'orders': orders})

def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 'Доставляется'  # Меняем статус заказа на "Доставляется"
    order.courier = request.user.courier  # Привязываем заказ к текущему курьеру
    order.save()
    return redirect('dashboard')

def myorders(request):
    courier_orders = Order.objects.filter(courier=request.user.courier)
    return render(request, 'myorders.html', {'courier_orders': courier_orders})

def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('myorders')
    else:
        form = OrderStatusForm(instance=order)
    return render(request, 'update_order_status.html', {'form': form, 'order': order})

def in_progress_orders(request):
    orders = Order.objects.all()
    form = OrderStatusFilterForm(request.GET)
    if form.is_valid():
        status = form.cleaned_data['status']
        orders = orders.filter(status=status)
    return render(request, 'inprogress.html', {'orders': orders, 'form': form})

def mysalary(request):
    if request.method == 'POST':
        form = SetSalaryForm(request.POST)
        if form.is_valid():
            courier = request.user.courier
            schedule = Schedule.objects.filter(courier=courier)
            salary_list = []
            for item in schedule:
                working_hours = Decimal((item.end_time.hour - item.start_time.hour) + (item.end_time.minute - item.start_time.minute) / 60)
                salary = working_hours * form.cleaned_data['money_per_hour']
                salary_list.append({
                    'date': item.date,
                    'working_hours': working_hours,
                    'salary': salary,
                })
            return render(request, 'mysalary.html', {'form': form, 'salary_list': salary_list})
    else:
        form = SetSalaryForm()
    return render(request, 'mysalary.html', {'form': form})

def courier_establishments(request):
    current_courier = request.user.courier
    establishments = EstCouriers.objects.filter(courier=current_courier).values_list('establishment', flat=True)
    establishments = Establishment.objects.filter(id__in=establishments)
    return render(request, 'myest.html', {'establishments': establishments})

def courier_schedule(request):
    current_courier = request.user.courier
    if request.method == 'POST':
        form = EstablishmentChoiceForm(request.POST)
        if form.is_valid():
            establishment_id = form.cleaned_data['establishment']
            courier_schedule = Schedule.objects.filter(courier=current_courier, est_id=establishment_id)
            return render(request, 'myschedule.html', {'form': form, 'courier_schedule': courier_schedule})
    else:
        form = EstablishmentChoiceForm()
    return render(request, 'myschedule.html', {'form': form})