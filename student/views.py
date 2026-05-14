from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden
from rest_framework.fields import SlugField

from .models import Parent, Student


def add_student(request):

    if request.method == "POST":

        # =========================
        # Informações do estudante
        # =========================

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

        # =========================
        # Informações dos pais
        # =========================

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

        # =========================
        # Validar campos únicos
        # =========================

        if Student.objects.filter(student_id=student_id).exists():

            messages.error(
                request,
                "Já existe um estudante com este ID."
            )

            return redirect("add_student")

        if Student.objects.filter(
            admission_number=admission_number
        ).exists():

            messages.error(
                request,
                "Já existe um estudante com este número de matrícula."
            )

            return redirect("add_student")

        try:

            # =========================
            # Guardar dados dos pais
            # =========================

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

            # =========================
            # Criar estudante
            # =========================

            student = Student(
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

            # =========================
            # Salvar estudante
            # =========================

            student.save()

            messages.success(
                request,
                "Estudante adicionado com sucesso!"
            )

            return redirect("student_list")

        except Exception as e:

            messages.error(
                request,
                f"Erro ao salvar o estudante: {e}"
            )

            return redirect("add_student")

    return render(
        request,
        "students/add-student.html"
    )


def student_list(request):

    student_list = Student.objects.select_related("parent").all()

    context = {
        'student_list': student_list,
    }

    return render(
        request,
        "students/students.html",
        context
    )


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import Student


def edit_student(request, slug):

    # =========================
    # Buscar estudante
    # =========================

    student = get_object_or_404(
        Student,
        slug=slug
    )

    parent = student.parent

    # =========================
    # Actualizar estudante
    # =========================

    if request.method == "POST":

        try:

            # =========================
            # Dados do estudante
            # =========================

            student.first_name = request.POST.get(
                "first_name"
            )

            student.last_name = request.POST.get(
                "last_name"
            )

            student.student_id = request.POST.get(
                "student_id"
            )

            student.gender = request.POST.get(
                "gender"
            )

            student.date_of_birth = request.POST.get(
                "date_of_birth"
            )

            student.student_class = request.POST.get(
                "student_class"
            )

            student.religion = request.POST.get(
                "religion"
            )

            student.joining_date = request.POST.get(
                "joining_date"
            )

            student.mobile_number = request.POST.get(
                "mobile_number"
            )

            student.admission_number = request.POST.get(
                "admission_number"
            )

            student.section = request.POST.get(
                "section"
            )

            # =========================
            # Actualizar imagem
            # =========================

            if request.FILES.get("student_image"):

                student.student_image = request.FILES.get(
                    "student_image"
                )

            # =========================
            # Dados dos pais
            # =========================

            parent.father_name = request.POST.get(
                "father_name"
            )

            parent.father_occupation = request.POST.get(
                "father_occupation"
            )

            parent.father_mobile = request.POST.get(
                "father_mobile"
            )

            parent.father_email = request.POST.get(
                "father_email"
            )

            parent.mother_name = request.POST.get(
                "mother_name"
            )

            parent.mother_occupation = request.POST.get(
                "mother_occupation"
            )

            parent.mother_mobile = request.POST.get(
                "mother_mobile"
            )

            parent.mother_email = request.POST.get(
                "mother_email"
            )

            parent.present_address = request.POST.get(
                "present_address"
            )

            parent.permanent_address = request.POST.get(
                "permanent_address"
            )

            # =========================
            # Salvar alterações
            # =========================

            parent.save()
            student.save()

            messages.success(
                request,
                "Estudante actualizado com sucesso!"
            )

            return redirect("student_list")

        except Exception as e:

            messages.error(
                request,
                f"Erro ao actualizar estudante: {e}"
            )

            return redirect(
                "edit_student",
                slug=student.slug
            )

    context = {
        "student": student,
        "parent": parent
    }

    return render(
        request,
        "students/edit-student.html",
        context
    )           

def view_student(request, slug):
    student = get_object_or_404(Student, student_id = slug)
    context = {
        'student': student
    }
    return render(request, "students/student-details.html", context)

from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect

from .models import Student


def delete_student(request, slug):

    # =========================
    # Permitir apenas POST
    # =========================

    if request.method != "POST":

        return HttpResponseForbidden(
            "Método não permitido."
        )

    try:

        # =========================
        # Buscar estudante
        # =========================

        student = get_object_or_404(
            Student,
            slug=slug
        )

        student_name = (
            f"{student.first_name} "
            f"{student.last_name}"
        )

        # =========================
        # Apagar estudante
        # =========================

        student.delete()

        # =========================
        # Notificação
        # =========================

        # create_notification(
        #     request.user,
        #     f"Deleted student: {student_name}"
        # )

        messages.success(
            request,
            f"Estudante {student_name} removido com sucesso!"
        )

        return redirect("student_list")

    except Exception as e:

        messages.error(
            request,
            f"Erro ao remover estudante: {e}"
        )

        return redirect("student_list")