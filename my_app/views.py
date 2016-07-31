from __future__ import unicode_literals
from django.shortcuts import render
from models import ToDoList
from forms import ToDoForm
from django.shortcuts import redirect

def to_do_function(request):
    if request.method == 'POST':
        form = ToDoForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if request.POST.get('work_id') is not None:
                if request.POST.get('cancel') is None:
                    work_id_update = request.POST.get('work_id')
                    new_work_title = request.POST.get('work_title')
                    work_id_status = request.POST.get('status')
                    if work_id_status is not None:
                        work_id_status = int(work_id_status.encode())
                        work = ToDoList.objects.filter(id=work_id_status)
                        status_work = work.get().status
                        if status_work == 0:
                            work.update(status=1)
                    ToDoList.objects.filter(id=work_id_update).update(work_title=new_work_title)
                return redirect(to_do_table)
            else:
                if request.POST.get('cancel') is not None:
                    return redirect(to_do_table)
                elif ToDoList.objects.filter().count() > 0:
                    list_works = ToDoList.objects.filter()
                    last_number = 0
                    for item in list_works:
                        if item.number > last_number:
                            last_number = item.number
                    work = ToDoList.objects.create(work_title=data['work_title'])
                    ToDoList.objects.filter(id = work.id).update(number=(last_number + 1))
                else:
                    work = ToDoList.objects.create(work_title=data['work_title'])
                    ToDoList.objects.filter(work_title=work.work_title).update(number=1)
            return redirect(to_do_table)
        else:
            if request.POST.get('cancel') is not None:
                return redirect(to_do_table)
            context = {'to_do_form': form}
            return render(request, 'to_do_form.html', context)
    else:
        context = {'to_do_form':ToDoForm()}
        return render(request, 'to_do_form.html', context)

def to_do_table(request):
    list_works = ToDoList.objects.filter()
    if request.method == 'POST':
        work_id_up = request.POST.get('lift_up')
        work_id_down = request.POST.get('put_down')
        work_id_delete = request.POST.get('delete')
        work_id_update = request.POST.get('update')
        work_id_status = request.POST.get('status')
        if work_id_up is not None:
            work_id_up = int(work_id_up.encode())
            work = ToDoList.objects.filter(id=work_id_up)
            number_work = work.get().number
            if number_work != 1:
                ToDoList.objects.filter(number=number_work - 1).update(number=number_work)
                work.update(number=(number_work - 1))
                new_list_works = sorted(list_works, key=lambda ToDoList:ToDoList.number)
                context = {'works': new_list_works}
                return render(request, 'to_do_list.html', context)
        elif work_id_down is not None:
            work_id_down = int(work_id_down.encode())
            work = ToDoList.objects.filter(id=work_id_down)
            number_work = work.get().number
            if number_work != ToDoList.objects.count():
                ToDoList.objects.filter(number=number_work + 1).update(number=number_work)
                work.update(number=(number_work + 1))
                new_list_works = sorted(list_works, key=lambda ToDoList: ToDoList.number)
                context = {'works': new_list_works}
                return render(request, 'to_do_list.html', context)
        elif work_id_delete is not None:
            work_id_delete = int(work_id_delete.encode())
            work = ToDoList.objects.filter(id=work_id_delete)
            number_work = work.get().number
            if number_work != ToDoList.objects.count():
                work_list = ToDoList.objects.filter(number__gt=number_work)
                for item in work_list:
                    ToDoList.objects.filter(id = item.id).update(number=item.number-1)
            work.delete()
            new_list_works = sorted(list_works, key=lambda ToDoList: ToDoList.number)
            context = {'works': new_list_works}
            return render(request, 'to_do_list.html', context)
        elif work_id_update is not None:
            work_id_update = int(work_id_update.encode())
            work_title = ToDoList.objects.filter(id=work_id_update).get().work_title
            context = {'to_do_form': ToDoForm(),'work_id': work_id_update, 'work_title': work_title}
            return render(request, 'to_do_form.html', context)
        elif work_id_status is not None:
            work_id_status = int(work_id_status.encode())
            work = ToDoList.objects.filter(id=work_id_status)
            status_work = work.get().status
            if status_work == 0:
                work.update(status=1)
            else:
                work.update(status=0)
            new_list_works = sorted(list_works, key=lambda ToDoList: ToDoList.number)
            context = {'works': new_list_works}
            return render(request, 'to_do_list.html', context)
        new_list_works = sorted(list_works, key=lambda ToDoList: ToDoList.number)
        context = {'works': new_list_works}
        return render(request, 'to_do_list.html', context)
    else:
        new_list_works = sorted(list_works, key=lambda ToDoList: ToDoList.number)
        context = {'works': new_list_works}
        return render(request, 'to_do_list.html', context)
