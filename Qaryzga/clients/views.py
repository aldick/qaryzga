from django.shortcuts import render, get_object_or_404, resolve_url, redirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User

from .forms import ClientCreateForm, ClientUpdateForm, ClientSelectForm, ClientLoginForm
from .models import Client
from orders.models import Order

def clients_list_order_view(request, slug):
    clients = Client.objects.filter(is_active=True)
    clients = clients.order_by(slug)
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})

def clients_list_view(request):
    clients = Client.objects.filter(is_active=True)
    return render(request, 'clients/clients_list.html', {
        "section": "clients",
		"clients": clients
	})
    
def clients_detail_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    orders = Order.objects.filter(phone_number=client.phone_number)
    total_sum = sum(order.get_total_cost() for order in orders)
    
    if client.user.is_staff:
        return render(request, 'clients/clients_detail.html', {
            "section": "clients",
            "client": client,
            "orders": orders,
            "total_sum": total_sum
        })
    else:
        return render(request, 'clients/clients_detail_not_staff.html', {
            "section": "clients",
            "client": client,
            "orders": orders,
            "total_sum": total_sum
        })
    
def clients_create_view(request, slug=None):
    
    if request.method == "POST":    
        form = ClientCreateForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            user = User.objects.create_user(client.phone_number, f"{client.name}@balqaimaq.kz", "12345678")
            user.save()
            client.user = user
            client.save()
            
            url = resolve_url("clients_list")
            if slug == "order":
                return redirect(f'../../../orders/create/?phone_number=%2B{form.cleaned_data["phone_number"][1:]}')
    elif 'phone_number' in request.GET:
        phone_number = Client.objects.create(phone_number=request.GET.get("phone_number"))
        form = ClientCreateForm(instance=phone_number)
        phone_number.delete()
        
    else:
        form = ClientCreateForm()
    
    return render(request, "clients/clients_create.html", {
        "section": "clients",
        "form": form,
    })
    
def clients_update_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    if request.method == "POST":    
        form = ClientUpdateForm(instance=client,
                          data=request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=client.user.username)
            user.username = client.phone_number
            user.email = f"{client.name}@balqaimaq.kz"
            user.save()
            client.save()
            
            url = resolve_url("clients_detail", pk)
            return redirect(url)
    else:
        form = ClientUpdateForm(instance=client)
        
    return render(request, "clients/clients_update.html", {
        "section": "clients",
        "form": form,
        "client": client
    })
    
def clients_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not client.is_active:
        raise Http404("Страница не найдена")
    
    if request.method == "POST":
        client.is_active = False
        client.user.is_active = False
        client.save()
        return redirect('clients_list')
    return render(request, "clients/clients_delete.html", {
        'section': "clients",
        "client": client
    })
    
def clients_select_view(request, phone_number=None):
    form = ClientSelectForm()
    clients = Client.objects.filter(phone_number="1")
    if 'phone_number' in request.GET:
        q = request.GET['phone_number']
        print(q)
        if q[0] == "+":
            q = q.replace("+", '', 1)
        elif q[0] == "8":
            q = q.replace("8", '7', 1)
        print(q)
        if len(q) == 11:
            multiple_q = Q(Q(phone_number__icontains=q) | Q(name__icontains=q)) 
            clients = Client.objects.filter(multiple_q).filter(is_active=True)
            
            if clients.exists():
                phone_number = Client.objects.get(phone_number=q)
                form = ClientSelectForm(instance=phone_number)
        # phone_number.delete()
    
    return render(request, "clients/clients_select.html", {
        "section": "orders",
        "clients": clients,
        "form": form,
        "phone_number": request.GET.get('phone_number')
    })
    
def clients_login_view(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd["username"],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    url = resolve_url("clients_detail", user.client.phone_number)
                    return redirect(url)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = ClientLoginForm()
    
    return render(request, "clients/clients_login2.html", {
        "section": "orders",
        "form": form,
    })

def clients_logout_view(request):
    logout(request)
    return redirect('clients_login')