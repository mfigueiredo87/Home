from django.shortcuts import render
from django.contrib import admin

from .models import *
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.db.models import Q

from .models import Student
# Create your views here.

def add_student(request):
    
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        student_id = request.POST.get("student_id")
        gender = request.POST.get("gender")
        date_of_birth = request.POST.get("date_of_birth")
        student_class = request.POST.get("student_class")
        religion = request.POST.get("religion")
        joining_date = request.POST.get("joining_date")
        mobile_number = request.POST.get("mobile_number")
        admission_number = request.POST.get("admission_number")
        section = request.POST.get("section")
        student_image = request.FILES.get("student_image")
        
        #retrieve parent information
        father_name = request.POST.get("father_name")
        father_occupation = request.POST.get("father_occupation")
        father_mobile = request.POST.get("father_mobile")
        father_email = request.POST.get("father_email")
        mother_name = request.POST.get("mother_name")
        mother_occupation = request.POST.get("mother_occupation")
        mother_mobile = request.POST.get("mother_mobile")
        mother_email = request.POST.get("mother_email")
        present_address = request.POST.get("present_address")
        permanent_address = request.POST.get("permanent_address")
       
 
        # verificar se já existe um estudante com este nome e todos os campos unicos
        # if Student.objects.filter(first_name=first_name, last_name=last_name, student_id=student_id, admission_number=admission_number).exists():

        #     messages.error(
        #         request,
        #         'Já existe um estudante com este nome e sobrenome.'
        #     )

        #     return redirect('add_student')
        
        # validar apenas os campos unicos nao podem ser iguais
        if Student.objects.filter(
            Q(student_id=student_id) |
            Q(admission_number=admission_number)
        ).exists():

            messages.error(
                request,
                'Já existe um estudante com este ID ou número de matrícula.'
        )

        return redirect('add_student')
        
        #guardar as informacoes dos parentes
        parent = Parent.objects.create(
            father_name=father_name,
            father_occupation=father_occupation,
            father_mobile=father_mobile,
            father_email=father_email,
            mother_name=mother_name,
            mother_occupation=mother_occupation,
            mother_mobile=mother_mobile,
            mother_email=mother_email,
            present_address=present_address,
            permanent_address=permanent_address
        )
        
        # guardar as informacoes do estudante
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            student_id=student_id,
            gender=gender,
            date_of_birth=date_of_birth,
            student_class=student_class,
            religion=religion,
            joining_date=joining_date,
            mobile_number=mobile_number,
            admission_number=admission_number,
            section=section,
            student_image=student_image,
            parent=parent
        )
    # exibindo as mensagens
        messages.success(request, "Estudante adicionado com sucesso!")
        # return render(request, "student_list")
  
        # Process the form data and save the new student
        
    return render(request, "students/add-student.html")


def student_list(request):
    return render(request, "students/students.html")

def edit_student(request, student_id):
    return render(request, "students/edit-student.html", {"student_id": student_id})

def view_student(request, student_id):
    return render(request, "students/student-detail.html")