from django.shortcuts import render, redirect, get_object_or_404
from email import message
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from hostel import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Student, Hostel, Room, Utilities, Complaint, UserActivityLog, CommunityMessage, HostelCommunityMessage
from .forms import ProfileForm, ComplaintForm, CommunityMessageForm, StudentEditForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader





# Create your views here.

def home(request):
    if request.user.is_authenticated:
        user_profile = Student.objects.filter(user=request.user).first()
        
        has_profile = user_profile is not None

        if has_profile:
            profile = Student.objects.get(user=request.user)
            room = profile.room_for_student
            utilities = Utilities.objects.filter(room=room)
            roommates = Student.objects.filter(room_for_student=room).exclude(user=request.user)
            return render(request, 'home.html', {'has_profile': has_profile, 'profile': profile, 'utilities': utilities, 'roommates': roommates})
        else:
            return render(request, 'home.html', {'has_profile': has_profile})
    
    else:
        return render(request, 'home.html')
    
    


#student 
def create_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user

                activity_log = UserActivityLog(user=request.user, activity="Profile was created")
                activity_log.save()

                #get department value
                department = form.cleaned_data['department']
                if department == "medicine and surgery" or department == "dentistry" or department == "pharmacy" or department == "optometry" or department == "nursing" or department == "medical laboratory science" or department == "pharmacology" or department == "anatomy" or department == "physiology" or department == "public and community health": 
                    college = "college of medical and health sciences"
                elif department == "energy and petroleum studies" or department == "petrochemical and industrial chemistry" or department == "chemistry" or department == "biochemistry" or department == "microbiology":
                    college = "college of natural and applied sciences"
                elif department == "intelligence and security studies" or department == "international relations and strategic studies" or department == "business administration" or department == "public administration" or department == "political science" or department == "sociology" or department == "marketing" or department == "mass communication" or department == "accounting" or department == "economics" or department == "finance":
                    college = "college of management and social sciences"
                elif department == "ll.b. law":
                    college = "college of law"
                elif department == "computer science" or department == "telecommunication technology" or department == "software engineering" or department == "cyber security" or department == "information systems" or department == "information technology":
                    college = "college of computing and telecommunication"
                

                profile.college = college
                profile.save()
                return redirect('home')
        else:
            form = ProfileForm()
        return render(request, 'uploadprof.html', {'form': form})
    else:
        return render(request, '404.html')



def edit_student(request):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            student = request.user.student
            if request.method == 'POST':
                form = StudentEditForm(request.POST, request.FILES, instance=student)
                if form.is_valid():
                    form.save()
                    return redirect('profile')
            else:
                form = StudentEditForm(instance=student)
            return render(request, 'edit_student.html', {'form': form})
        else:
            return redirect('login')
    else:
        return render(request, '404.html')


#authentication
def signup(request):
    
    
    if request.method == "POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
    
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request, "Email already exists")
            return redirect('home')
        
         
        if password != password2:
            messages.error(request, "Passwords do not match!")  
            return redirect('home')
         

    
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        
        
        myuser.save()    
        
        messages.success(request, "Your Account has been created successfully.")
        return redirect('signin')  
        
       
    
    return render(request, 'signup.html')


def signin(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            activity_log = UserActivityLog(user=request.user, activity="Signed in")
            activity_log.save()
            return redirect('home')
            
        else:
            messages.error(request, "Login Error")
            return redirect('home')    
    
    return render(request, 'signin.html')

def signout(request):
    activity_log = UserActivityLog(user=request.user, activity="Signed Out")
    activity_log.save()
    logout(request)
    messages.success(request, "Successfully Logged Out ")
    return redirect('home')


#allocation

def allocate_hostel(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Student.objects.get(user=user)
        gender = profile.gender
        capacity_pref = profile.room_capacity_preference
        hostels = Room.objects.filter(hostel__gender=gender).order_by('capacity')
        
        allocated_hostel = None
        allocated_room = None

        for hostel in hostels:
            if hostel.availability > 0 and hostel.capacity == capacity_pref:
                allocated_hostel = hostel.hostel
                allocated_room = hostel
                break
            elif hostel.availability > 0 and hostel.capacity <= capacity_pref:
                allocated_hostel = hostel.hostel
                allocated_room = hostel
                break
            elif hostel.availability > 0 and hostel.capacity >= capacity_pref:
                allocated_hostel = hostel.hostel
                allocated_room = hostel
                break
            else:
                pass

        if allocated_hostel and allocated_room:
            profile.hostel = allocated_hostel
            profile.room_for_student = allocated_room
            allocated_room.students_in_room.add(user)
            allocated_room.availability -= 1
            allocated_room.save()

            if allocated_room.availability == 0:
                allocated_room.hostel.room_availability -= 1
                allocated_room.hostel.save()



            activity_log = UserActivityLog(user=request.user, activity="Hostel allocated successfully")
            activity_log.save()

            profile.save()
            return redirect('home')

        return render(request, 'profile.html', {'profile': profile, 'allocated_hostel': allocated_hostel, 'allocated_room': allocated_room})
    else:
        return render(request, '404.html')
    

def create_complaint(request):
    if request.user.is_authenticated:
        user = request.user
        room = user.student.room_for_student

        if room is not None:
            if request.method == 'POST':
                form = ComplaintForm(request.POST)
                if form.is_valid():
                    user = request.user
                    room = user.student.room_for_student
                    utility = form.cleaned_data['utility']
                    note = form.cleaned_data['note']

                    # Check if a complaint with the same utility and room exists and is unresolved
                    existing_complaint = Complaint.objects.filter(room=room, utility=utility, resolved=False).first()

                    if existing_complaint:
                        existing_utility = existing_complaint.utility  # Retrieve the existing utility value
                        activity_log = UserActivityLog(user=request.user, activity=f"A complaint for the utility '{existing_utility}' from this room already exists.")
                        activity_log.save()
                        messages.error(request, f"A complaint for the utility '{existing_utility}' from this room already exists.")
                        return redirect('home')


                    # Create the complaint object
                    #complaint = Complaint.objects.create(user=user, utility=utility, note=note)

                    # Check if Utilities object exists for the user's room
                    utilities, created = Utilities.objects.get_or_create(room=room)


                    # Update the corresponding utility value for the user's room
                    #utilities = Utilities.objects.filter(room=room)
                    #for util in utilities:
                    #    setattr(util, utility, False)
                    #    util.save()

                    setattr(utilities, utility, False)
                    utilities.save()

                    

                    # Get the room associated with the selected utility
                    selected_utility = Utilities.objects.get(room=room)
                    assigned_room = selected_utility.room


                    # Create the complaint object and assign the room
                    complaint = Complaint.objects.create(user=user, utility=utility, note=note, room=assigned_room)


                    activity_log = UserActivityLog(user=request.user, activity=f"You created a complaint about your {utility}")
                    activity_log.save()


                    # Redirect to a success page
                    messages.success(request, "Your complaint has been received successfully")
                    return redirect('home')
            else:
                form = ComplaintForm()

            return render(request, 'create_complaint.html', {'form': form})
        else:
            messages.error(request, "You have not been assigned a room yet.")
            return redirect('home')
    else:
        return render(request, '404.html')


def user_activity_log(request):
    if request.user.is_authenticated:
        user = request.user
        activity_log = UserActivityLog.objects.filter(user=user).order_by('-timestamp')
        return render(request, 'activity_log.html', {'activity_log': activity_log})
    else:
        return render(request, '404.html')

def download_activity_log(request):
    user = request.user
    logs = UserActivityLog.objects.filter(user=user)

    # Generate XML content
    template = loader.get_template('activity_log.xml')
    context = {'logs': logs}
    xml_content = template.render(context)

    # Create the HTTP response with the XML content and appropriate headers
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename="activity_log.xml"'
    return response



def community(request):
    if request.user.is_authenticated:
        user = request.user
        student = Student.objects.get(user=user)
        college = student.college

        if request.method == 'POST':
            form = CommunityMessageForm(request.POST)
            if form.is_valid():
                message = form.cleaned_data['message']
                CommunityMessage.objects.create(sender=user, receiver_college=college, message=message)
                return redirect('community')

        else:
            form = CommunityMessageForm()

        messages = CommunityMessage.objects.filter(receiver_college=college).order_by('-timestamp')

        context = {'form': form, 'messages': messages}
        return render(request, 'community.html', context)
    else:
        return render(request, '404.html')


def hostel_community(request):
    if request.user.is_authenticated:
        messages = HostelCommunityMessage.objects.all()
        return render(request, 'hostelcommunity.html', {'messages': messages})
    else:
        return render(request, '404.html')

def post_message(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            message = request.POST.get('message')
            hostel = request.user.student.hostel
            HostelCommunityMessage.objects.create(user=request.user, hostel=hostel, message=message)
            return redirect('hostel_community')
        else:
            return render(request, 'post_message.html')
    else:
        return render(request, '404.html')


def userprofile(request, user_id):
    if request.user.is_authenticated:
        user = get_object_or_404(User, id=user_id)
        student = user.student
        context = {'user': user, 'student': student}
        return render(request, 'userprofile.html', context)

    else:
        return render(request, '404.html')

