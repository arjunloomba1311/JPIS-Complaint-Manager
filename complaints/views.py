from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import complaint_info
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail
import numpy as np

#vizualization library
from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.palettes import Magma, Inferno, Plasma, Viridis, Cividis

#analytics library
from scipy import spatial


def home(request):
    return render (request, 'complaints/home.html')


# @login_required(login_url="/accounts/signup")
def create(request):
    if request.method == 'POST':
        if request.POST['description'] and request.POST['title'] and request.POST['room_no']:
                if (int(request.POST['room_no']) > 100) and (int(request.POST['room_no']) < 600):
                    info = complaint_info()
                    info.title = request.POST['title']
                    info.description = request.POST['description']
                    info.room_no = request.POST['room_no']
                    info.pub_date = "2020-12-9"
                    info.issue_type = request.POST['issue_type']
                    info.image = request.FILES['image']
                    info.hunter = request.user
                    info.save()
                    return render(request,'complaints/home.html',{'filled':'Thank you for entering your details'})
                else:
                    return render(request,'complaints/create.html',{'error':"Room number must be between 100 and 600"})
            #Should Ideally take to the user's own page
        else:
            return render(request,'complaints/create.html',{'error':"You can't leave any field empty"})
    return render(request,'complaints/create.html')
# create your views here.

@login_required(login_url="/accounts/signup")
def for_user(request):
    #TODO restrict admins from accessing this link
    info_objs = complaint_info.objects.filter(hunter=request.user).all()
    return render(request, 'complaints/detail.html',{'info_objs':info_objs})

@login_required(login_url="/accounts/signup_admin")
def for_admin(request):
    #TODO restrict students from accessing this link
    total = complaint_info.objects.count()
    complaint_objs = complaint_info.objects.order_by('-pub_date')
    #ordered by most recent item
    return render(request, 'complaints/detail_admin.html',{'complaint_objs':complaint_objs,'count':total})

@login_required(login_url="/accounts/signup_admin")
def specific(request, complaint_id):
    complaint = get_object_or_404(complaint_info, pk = complaint_id)
    issue_types = {1:'Bathroom',2:'Common Room',3:'Electricty',4:'furniture',5:'food',6:'Other'}
    return render(request,'complaints/specific.html', {'complaint':complaint,'issue_types':issue_types})

@login_required(login_url="/accounts/signup_admin")
def approve(request,complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(complaint_info, pk = complaint_id)
        if not complaint.approved == True:
            complaint.approved = True
            complaint.rejected = False
            complaint.pending = False
            complaint.save()
            approved = 'approved'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'done': approved})
        else:
            error = 'aldready approved'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'error': error})

@login_required(login_url="/accounts/signup_admin")
def pending(request,complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(complaint_info, pk = complaint_id)
        if not complaint.pending == True:
            complaint.approved = False
            complaint.rejected = False
            complaint.pending = True
            complaint.save()
            pending = 'set to pending'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'done': pending})
        else:
            error = 'Aldready set to pending'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'error': error})


@login_required(login_url="/accounts/signup_admin")
def rejected(request,complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(complaint_info, pk = complaint_id)
        if not complaint.rejected == True:
            complaint.approved = False
            complaint.rejected = True
            complaint.pending = False
            complaint.save()
            rejected = 'set to rejected'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'done': rejected})
        else:
            error = 'Aldready set to rejected'
            return render(request, 'complaints/specific.html', {'complaint': complaint, 'error': error})

@login_required(login_url="/accounts/signup_admin")
def delete(request, complaint_id):
    if request.method=='POST':
        complaint = get_object_or_404(complaint_info,pk = complaint_id)
        complaint.delete()
        info_objs = complaint_info.objects.filter(hunter=request.user).all()
        return render(request, 'complaints/detail.html',{'info_objs':info_objs})

@login_required(login_url="/accounts/signup")
def rate(request, complaint_id):
    if request.method =='POST':
        info_objs = complaint_info.objects.filter(hunter=request.user).all()
        rating = request.POST['rate']
        if (int(rating) >= 0) and (int(rating) <= 10):
            complaint = get_object_or_404(complaint_info,pk = complaint_id)
            complaint.rating = rating
            complaint.save()
            success = 'Feedback rating added successfully'
            return render(request, 'complaints/detail.html',{'info_objs':info_objs,'success':success})
        else:
            error = 'Invalid rating, please make sure that rating is an integer between 0 and 10'
            return render(request, 'complaints/detail.html',{'info_objs':info_objs,'error':error})
    else:
        return render(request, 'complaints/detail.html',{'info_objs':info_objs})


def complaint_fixer():
    fixer_mail = ""
    return fixer_mail

def cost():
    return None

def email_personel(request,complaint_id):
    if request.method == 'POST':
        complaint = get_object_or_404(complaint_info, pk = complaint_id)
        complaint.mail_sent = True
        complaint.save()
        subject = 'Please check this complaint'
        message = "Below are the relevant details for this student complaint \n Name: Test Complaint \n Room No: 405 \n Posted by: aloomba@jpischool.com \n Date Posted: Dec 9 2020 \n Complaint Description:	The table and piano in the hostel are broken. They need repair \n Issue Type: Furniture"
        from_email = settings.EMAIL_HOST_USER
        to_list = [settings.EMAIL_HOST_USER]
        send_mail(subject,message,from_email, to_list, fail_silently= False)
        email_sent = "The email has been sent to the required personel"
        return render(request, 'complaints/specific.html',{'complaint':complaint, 'done':email_sent})

@login_required(login_url="/accounts/signup_admin")
def mail_sent(request):
    complaint_objs = complaint_info.objects.order_by('-pub_date')
    return render(request, 'complaints/mail.html',{'complaint_objs':complaint_objs})

@login_required(login_url="/accounts/signup")
def history(request):
    complaint_objs = complaint_info.objects.order_by('-pub_date')
    return render(request, 'complaints/history.html', {'complaint_objs':complaint_objs})

def most_common_complaint(type):
    if len(type) > 0:
        c = 0 # this is simply a counter to store frequencies in the loop
        val = type[0]
        for i in type:
            freq = type.count(i)
            if (freq > c):
                c = freq
                val = i
        return val
    else:
        return 0

def vizualization(type):
    if len(type) > 0:
        values_arr = ["None", 'Bathroom','Common Room','Electricity','Furniture','Food','Other']
        names = list()
        for i in range(len(type)):
            names.append(type[i])
        counts = list()
        for i in type:
            counts.append(type.count(i))
        title = "Count of all item types of Complaints"
        plot = figure(
        title = title,
        x_axis_label= 'issue_type',
        y_axis_label= 'count',
        plot_width = 800,
        plot_height = 400,
        )
        plot.vbar(x = names,top = counts,width = 0.4)
        script, div = components(plot)
        return script, div

def recommendation_problem(type_arr, rating_arr):
     #cosine and euclidian/spacial distance between 2 complaint types for multiple users
     #if users are very similar then that's interesting because then most users face a problem
     #with that specific complaint type

         # Issue types:
         # 1: Bathroom
         # 2: Common_Room
         # 3: Electricity
         # 4: Furniture
         # 5: Food
         # 6: Other

    from scipy import spatial

    #explanation of code given below:-
    #The overall ratings for each issue type would be stored wherein each issue type ratings would be a 1-D array inside
    # a larger 2-D array.
    # The issue type an integer from 1-6 (-1) is taken as the appropriate index to add
    # the relavent rating value.

    overall_ratings = [[],[],[],[],[],[]]
    output = []
    if len(type_arr) > 0:
        for i in range(len(type_arr)):
            index = type_arr[i] - 1
            overall_ratings[index].append(rating_arr[i])

    # Now, the cosine similarity will be taken for all the ratings of each issue type 2 values at a time:
        Flag = True
        for i in range(len(overall_ratings)):
            if len(overall_ratings[i]) < 3:
                Flag = False

        if Flag == True:
            for i in range(len(type_arr)):
                avg_similarities = []
                for c in range(2,len(overall_ratings[i])):
                    similarities = []
                    val1 = overall_ratings[i][c-1]
                    val2 = overall_ratings[i][c-2]
                    arr_1 = [val1, val2]
                    for k in range(c+1,len(overall_ratings[i])):
                        valA = overall_ratings[i][k-1]
                        valB = overall_ratings[i][k]
                        arr_2 = [valA,valB]
                        similarity = spatial.distance.cosine(arr_1,arr_2)
                        similarities.append(similarity)
                mean = np.mean(similarities)
                avg_similarities.append(mean)

            avg_ratings = []

            for i in range(len(type_arr)):
                avg_ratings.append(np.mean(overall_ratings[i]))


            for i in range(len(avg_ratings)):
                if (avg_ratings[i] < 5) and (avg_similarities < 0.2):
                    output.append(i)
        return output
    else:
        return output

@login_required(login_url="/accounts/signup_admin")
def analytics_system(request):
    type_arr = []
    rej_arr = []
    accept_arr = []

    rating_arr = []
    for complaint in complaint_info.objects.all():
        type_arr.append(complaint.issue_type)
        rating_arr.append(complaint.rating)
        if complaint.rejected == True:
            rej_arr.append(complaint.issue_type)
        elif complaint.approved == True:
            accept_arr.append(complaint.issue_type)


    most_frequent_accept_num = most_common_complaint(accept_arr)
    most_frequent_num =  most_common_complaint(type_arr)
    most_frequent_rej_num = most_common_complaint(rej_arr)

    values_arr = ["None", 'Bathroom','Common Room','Electricity','Furniture','Food','Other']
    most_common = values_arr[most_frequent_num]
    most_rej = values_arr[most_frequent_rej_num]
    most_accept = values_arr[most_frequent_accept_num]

    problem_in_type = recommendation_problem(type_arr, rating_arr)

    script, div = vizualization(type_arr)

    output_dict = {'most_common':most_common, 'most_rej':most_rej,
    'most_accept':most_accept,'script':script,'div':div, 'problem': problem_in_type}
    return render(request, 'complaints/analytics.html', output_dict)

def admin_costs(request):
    return render (request, 'complaints/admin_costs.html')

def costs(request):
    return render(request, 'complaints/studentcosts.html')

#somehow combine these three functions
