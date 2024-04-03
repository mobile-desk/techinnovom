from django import forms
from .models import Student, Utilities, CommunityMessage
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic', 'gender', 'matric_number', 'department', 'room_capacity_preference']


    # Image field
    profile_pic = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control'
        })
    )


    #ChoiceField
    CHOICES = (
        ('female', 'Female'),
        ('male', 'Male'),
    )

    gender = forms.ChoiceField(
       choices=CHOICES,
       widget=forms.Select(attrs={
        'class': 'form-control'
        }))





    #numberfield


    room_capacity_preference = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        }),
        validators=[MinValueValidator(2), MaxValueValidator(8)]  # Set the minimum and maximum values here
    )


    # Charfield


    matric_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_matric_number(self):
        matric_number = self.cleaned_data.get('matric_number')

        matric_number = matric_number.strip().upper()
        # Add your validation logic here
        # For example, to check if the matric number starts with "AB" and has 8 digits:
        if not matric_number.startswith('NUO/'):
            raise forms.ValidationError('Invalid matric number.')

        return matric_number





    COURSECHOICES = (
        ('medicine and surgery', 'Medicine and Surgery'),
        ('dentistry', 'Dentistry'),
        ('pharmacy', 'Pharmacy'),
        ('optometry', 'Optometry'),
        ('nursing', 'Nursing'),
        ('medical laboratory science', 'Medical Laboratory Science'),
        ('pharmacology', 'Pharmacology'),
        ('anatomy', 'Anatomy'),
        ('physiology', 'Physiology'),
        ('public and community health', 'Public and Community Health'),
        #college of natural and applied sciences
        ('energy and petroleum studies', 'Energy and Petroleum Studies'),
        ('petrochemical and industrial chemistry', 'Petrochemical and Industrial Chemistry'),
        ('chemistry', 'Chemistry'),
        ('biochemistry', 'Biochemistry'),
        ('microbiology', 'Microbiology'),
        #college of management and social sciences
        ('intelligence and security studies', 'Intelligence and Security Studies'),
        ('international relations and strategic studies', 'International Relations and Strategic Studies'),
        ('business administration', 'Business Administration'),
        ('public administration', 'Public Administration'),
        ('political science', 'Political Science'),
        ('sociology', 'Sociology'),
        ('marketing', 'Marketing'),
        ('mass communication', 'Mass Communication'),
        ('accounting', 'Accounting'),
        ('economics', 'Economics'),
        ('finance', 'Finance'),
        #college of law
        ('ll.b. law', 'LL.B. Law'),
        #college of computing and telecommunication
        ('computer science', 'Computer Science'),
        ('telecommunication technology', 'Telecommunication Technology'),
        ('software engineering', 'Software Engineering'),
        ('cyber security', 'Cyber Security'),
        ('information systems', 'Information Systems'),
        ('information technology', 'Information Technology')
    )

    department = forms.ChoiceField(
       choices=COURSECHOICES,
       widget=forms.Select(attrs={
        'class': 'form-control'
        }))



class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['profile_pic', 'gender', 'matric_number', 'room_capacity_preference']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'matric_number': forms.TextInput(attrs={'class': 'form-control'}),
            'room_capacity_preference': forms.NumberInput(attrs={'class': 'form-control'}),
        }
       





class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Utilities
        fields = ['utility', 'note']


    #ChoiceField
    CHOICES = (
        ('fan', 'Fan'),
        ('bed', 'Bed'),
        ('mattress', 'Mattress'),
        ('pillows', 'Pillows'),
        ('wardrobe', 'Wardrobe'),
        ('book_rack', 'Book Rack'),
        ('tables', 'Tables'),
        ('chairs', 'Chairs'),
        ('wall_socket', 'Wall Socket'),
        ('tiles', 'Tiles'),
        ('paint', 'Paint'),
        ('window', 'Window'),
        ('waste_bin', 'Waste Bin'),
        ('door', 'Door'),
        ('door_lock', 'Door Lock'),
        ('bulb', 'Bulb'),
        ('wiring', 'Wiring'),
        ('shower', 'Shower'),
        ('towel_holder', 'Towel Holder'),
        ('tap', 'Tap'),
        ('water_closet', 'Water Closet'),
        ('TV', 'TV'),
        ('decoder', 'Decoder'),
        ('other', 'Others')
    )

    utility = forms.ChoiceField(
       choices=CHOICES,
       widget=forms.Select(attrs={
        'class': 'form-control'
        }))


    # Charfield
    note = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )


class CommunityMessageForm(forms.ModelForm):
    class Meta:
        model = CommunityMessage
        fields = ['message']


    # Charfield
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control'
        })
    )