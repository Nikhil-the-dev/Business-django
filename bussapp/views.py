from django.shortcuts import render,redirect
from .models import Vehicle,Register,Vehicle_list
from django.contrib import messages
from django.db.models import Q
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import openpyxl

def records_pdf_download_view(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_on = request.GET.get('filter') == 'on'

    records = Vehicle.objects.all()

    if query:
        records = records.filter(Vehicle_number__icontains=query)
    if filter_on and start_date and end_date:
        records = records.filter(Fuel_date__range=[start_date, end_date])

    context = {'record': records}
    return render(request, 'bussapp/records_pdf_download.html', context)


def records_generate_pdf(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_on = request.GET.get('filter') == 'on'

    records = Vehicle.objects.all()

    if query:
        records = records.filter(Vehicle_number__icontains=query)

    if filter_on and start_date and end_date:
        records = records.filter(Fuel_date__range=[start_date, end_date])

    # ✅ Calculate totals ONLY from filtered records
    total_fuel_ltr = sum(r.Fuel_Ltr for r in records)
    total_fuel_price = sum(r.Total_fuel_price for r in records)

    context = {
        'record': records,
        'total_fuel_ltr': total_fuel_ltr,
        'total_fuel_price': total_fuel_price
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fuel_records.pdf"'

    template = get_template('bussapp/records_pdf_template.html')
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had errors <pre>' + html + '</pre>')
    return response

def records_generate_excel(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_on = request.GET.get('filter') == 'on'

    records = Vehicle.objects.all()

    if query:
        records = records.filter(Vehicle_number__icontains=query)
    if filter_on and start_date and end_date:
        records = records.filter(Fuel_date__range=[start_date, end_date])

    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fuel Records"

    # Header
    headers = ["Vehicle Number", "Date", "Total Fuel (Ltr)", "Fuel Rate", "Total Amount", "Remark"]
    ws.append(headers)

    # Data rows
    for r in records:
        ws.append([
            r.Vehicle_number,
            r.Fuel_date.strftime('%Y-%m-%d'),
            r.Fuel_Ltr,
            r.Fuel_rate_per_ltr,
            r.Total_fuel_price,
            r.Remark
        ])

    # Set the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=fuel_records.xlsx'

    wb.save(response)
    return response

def vehicles_pdf_download_view(request):
    query = request.GET.get('q', '')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    filter_on = request.GET.get('filter') == 'on'

    records = Vehicle_list.objects.all()

    if query:
        records = records.filter(Vehicle_number__icontains=query)
    if filter_on and start_date and end_date:
        records = records.filter(Fuel_date__range=[start_date, end_date])

    context = {'record': records}
    return render(request, 'bussapp/vehicles_pdf_download.html', context)

def vehicles_generate_pdf(request):
    records = Vehicle_list.objects.all()
    template_path = 'bussapp/vehicles_pdf_template.html'
    context = {'record': records}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="vehicle_list.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had errors <pre>' + html + '</pre>')
    return response

def vehicles_generate_excel(request):
    records = Vehicle_list.objects.all()
    # Create workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Vehicle List"

    # Header
    headers = ["Vehicle Number", "Date"]
    ws.append(headers)

    # Data rows
    for r in records:
        ws.append([
            r.Add_vehicle_numbers,
            r.Date.strftime('%Y-%m-%d')
        ])

    # Set the HTTP response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Vehicle_list.xlsx'

    wb.save(response)
    return response

def register(request):
    fullname = request.POST.get('fullname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        reg_data = Register(Fullname = fullname, Email = email, Password = password)
        reg_data.save()
        if reg_data.id:  # This checks if the object has been saved successfully
            messages.success(request, 'Registered successfully')
            return redirect('/')
        else:
            messages.error(request, 'Registration failed. Please try again.')
            return redirect('/')
    return render(request,'bussapp/register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate input data
        if not email or not password:
            messages.error(request, "Please Enter Login Credential's.")
            return redirect('/')
        fetch_data = Register.objects.filter(Email=email).first()
        
        # Compare the plain text password
        if fetch_data and fetch_data.Password == password:
            request.session['fullname'] = fetch_data.Fullname
            request.session['email'] = fetch_data.Email
            return redirect('/home')
        else:
            messages.error(request,'Incorrect Email And Password')
            return redirect('/')
    return render(request,'bussapp/login.html')

def home(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    return render(request,'bussapp/home.html')

def add_vehicle(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    if request.method == 'POST':
        vehicle_numbers = request.POST.get('Vehicle_number')

        # Correct variable is vehicle_numbers, not Vehicle_number (which is a model)
        if not vehicle_numbers:
            messages.error(request, 'Please enter a vehicle number.')
            return redirect('/add_vehicle')

        # Save the vehicle number
        vehicle_data = Vehicle_list(Add_vehicle_numbers=vehicle_numbers)
        vehicle_data.save()

        if vehicle_data.id:
            messages.success(request, 'Vehicle number added successfully.')
            return redirect('/add_vehicle')         
        else:
            messages.error(request, 'Failed to add vehicle number.')
            return redirect('/add_vehicle')
    return render(request, 'bussapp/add_vehicle.html')

def vehicle_list(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    vehicle_list = Vehicle_list.objects.all()
    return render(request,'bussapp/vehicle_list.html',{'vehicle_list':vehicle_list})

def update_vehicle(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    
    id = request.GET.get('q')
    vehicle_id = Vehicle_list.objects.get(id=id)
    if request.method == 'POST':
        vehicle_id.Add_vehicle_numbers = request.POST.get('Vehicle_number')
        vehicle_id.save()
        messages.success(request,"Update successfully")
        return redirect('/vehicle_list')
    return render(request,'bussapp/update_vehicle.html',{'vehicle':vehicle_id})

def delete_vehicle(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    
    id = request.GET.get('q')
    vehicle_id = Vehicle_list.objects.get(id=id)
    if request.method == 'POST':
        vehicle_id.delete()
        messages.success(request,"Delete successfully")
        return redirect('/vehicle_list')
    return render(request,'bussapp/delete_vehicle.html',{'vehicle':vehicle_id})

def enter_data(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    Record = Vehicle_list.objects.all()
    
    if request.method == 'POST':
        
        Vehicle_number = request.POST.get('vehicle_number')
        Fuel_Ltr = request.POST.get('fuel_ltr')
        Fuel_rate_per_ltr = request.POST.get('fuel_rate_per_ltr')
        Total_fuel_price = request.POST.get('total_fuel_price')
        Remark = request.POST.get('remark')

        Data = Vehicle(Vehicle_number = Vehicle_number, Fuel_Ltr = Fuel_Ltr, Fuel_rate_per_ltr = Fuel_rate_per_ltr,
                       Total_fuel_price =Total_fuel_price,Remark = Remark)
        Data.save()
        if Data.id:  # This checks if the object has been saved successfully
            messages.success(request, 'Entered successfully')
            return redirect('/enter_data')
        else:
            messages.error(request, 'Data Entry Failed. Please try again.')
            return redirect('/enter_data')
    return render(request,'bussapp/enter_data.html',{'record':Record})

def view_records(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    Record = Vehicle.objects.all()
    return render(request,'bussapp/view_records.html',{'record':Record})

def update_record(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    id = request.GET.get('q')
    Record = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        Record.Vehicle_number = request.POST['vehicle_number']
        Record.Fuel_Ltr = request.POST['fuel_ltr']
        Record.Fuel_rate_per_ltr = request.POST['fuel_rate_per_ltr']
        Record.Total_fuel_price = request.POST['total_fuel_price']
        Record.Remark = request.POST['remark']
        Record.save()
        messages.success(request,"Update successfully")
        return redirect('/view_records')
    return render(request,'bussapp/update_record.html',{'record':Record})

def delete_record(request):
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    if not session_fullname or not session_email:
        return redirect('/')
    id = request.GET.get('q')
    Record = Vehicle.objects.get(id=id)
    if request.method == 'POST':
        Record.delete()
        messages.success(request,"Delete successfully")
        return redirect('/view_records')
    return render(request,'bussapp/delete_record.html',{'record':Record})

def multiple_records_delete(request):
    if request.method == "POST":
        ids = request.POST.getlist('selected_items')
        if ids:
            # Delete the selected records
            Vehicle.objects.filter(id__in=ids).delete()

        # After deletion, redirect to the same filtered view
        q = request.POST.get('q', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        mode = request.POST.get('mode', 'select')  # Assuming 'select' mode by default
        messages.success(request, 'Selected Data Deleted')
        # Build the URL with query parameters preserved
        redirect_url = f"/view_records?q={q}&start_date={start_date}&end_date={end_date}&mode={mode}"

        # Redirect to the filtered records page
        return redirect(redirect_url)
    
def multiple_vehicles_delete(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_items')
        Vehicle_list.objects.filter(id__in=selected_ids).delete()
        messages.success(request, 'Selected Data Deleted')
        return redirect('/vehicle_list')  # or redirect back to current page with params
    

def search(request):
    # Get session variables
    session_fullname = request.session.get('fullname')
    session_email = request.session.get('email')
    
    # Check if session variables are missing, redirect if so
    if not session_fullname or not session_email:
        return redirect('/')

    # Get the search query from the form
    query = request.GET.get('q', '')
    
    # if not query:
    #     return redirect('/view_records')
    
    # Get the start and end dates from the GET request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Construct the filter query
    filter_conditions = Q()

    if query:
        filter_conditions &= (Q(Vehicle_number__icontains=query))

    if start_date:
        filter_conditions &= Q(Fuel_date__gte=start_date)

    if end_date:
        filter_conditions &= Q(Fuel_date__lte=end_date)

    # Apply the filters to the Vehicle model
    records = Vehicle.objects.filter(filter_conditions).order_by('-Fuel_date')

    # Render the template with filtered records
    return render(request, 'bussapp/view_records.html', {'record': records})

def vehicle_search(request):
    # Check session for authentication
    if not request.session.get('fullname') or not request.session.get('email'):
        return redirect('/')

    # Get search input
    query = request.GET.get('q', '').strip()

    # Only search by Add_vehicle_numbers (case-insensitive partial match)
    if query:
        vehicle_list = Vehicle_list.objects.filter(Add_vehicle_numbers__icontains=query).order_by('Date')
    else:
        vehicle_list = Vehicle_list.objects.all().order_by('Date')

    return render(request, 'bussapp/vehicle_list.html', {'vehicle_list': vehicle_list,'query': query,})


def logout(request):
    if request.method == 'POST':
        if 'fullname' in request.session:
            del request.session['fullname']
        if 'email' in request.session:
            del request.session['email']
        messages.success(request,"Logout Succcessfull")
        return redirect('/')