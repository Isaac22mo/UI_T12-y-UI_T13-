from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages

from users.message import Message

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, 'Registro exitoso. ¡Bienvenido!') 
            return redirect('home')  
        else:
            
            print("Errores en el formulario:")
            for field in form:
                for error in field.errors:
                    print(f"Campo: {field.label}, Error: {error}")
            
            messages.error(request, 'Hubo un error con el formulario. Por favor, inténtalo de nuevo.')  # Mensaje de error
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
        return redirect('home')
    else:
        form = CustomUserLoginForm()
        return render(request, 'login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    message = Message("info", "Se ha cerrado sesión exitosamente", 200, 
                      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR8MIbugIhZBykSmQcR0QPcfnPUBOZQ6bm35w&s")
    
    return render(request, "login.html", {"message": json.dumps(message.to_dict())})


@login_required
def home_view(request):
    return render(request, 'home.html')