from django.contrib import admin
from django.db import models
from .models import Student, Hostel, Room, Utilities, Complaint, UserActivityLog
from django.http import HttpResponse
from django.utils.xmlutils import SimplerXMLGenerator
from django.utils.safestring import mark_safe



from django.http import HttpResponse
from django.contrib import admin
import logging
import xml.etree.ElementTree as ET





@admin.register(admin.models.LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    actions = ['download_logs']

    def download_logs(self, request, queryset):
        # Get the log entries
        log_entries = queryset.all()

        # Create the root element of the XML document
        root = ET.Element("logs")

        # Iterate over the log entries and create XML elements
        for log_entry in log_entries:
            log_element = ET.SubElement(root, "log")
            ET.SubElement(log_element, "action_time").text = str(log_entry.action_time)
            ET.SubElement(log_element, "user").text = str(log_entry.user)
            ET.SubElement(log_element, "content_type").text = str(log_entry.content_type)
            ET.SubElement(log_element, "object_id").text = str(log_entry.object_id)
            ET.SubElement(log_element, "object_repr").text = str(log_entry.object_repr)
            ET.SubElement(log_element, "action_flag").text = str(log_entry.action_flag)
            ET.SubElement(log_element, "change_message").text = str(log_entry.change_message)

        # Create the XML tree and write it to a file-like object
        tree = ET.ElementTree(root)
        file_obj = HttpResponse(content_type='application/xml')
        tree.write(file_obj, encoding='utf-8', xml_declaration=True)

        # Set the filename for the downloaded file
        file_name = 'hostel_allocation_log.xml'
        file_obj['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return file_obj
    download_logs.short_description = "Download Logs as XML"




# Register your models here.
#admin.site.register(Student)
admin.site.register(Hostel)







@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    readonly_fields = ('room_no',)

    actions = ['download_room_data']

    def download_room_data(self, request, queryset):
        # Create the root element of the XML document
        root = ET.Element("rooms")

        # Iterate over the selected rooms
        for room in queryset:
            room_element = ET.SubElement(root, "room")
            ET.SubElement(room_element, "hostel").text = str(room.hostel)
            ET.SubElement(room_element, "room_no").text = str(room.room_no)
            ET.SubElement(room_element, "capacity").text = str(room.capacity)
            ET.SubElement(room_element, "availability").text = str(room.availability)

            # Retrieve the students in the room
            students = room.students_in_room.all()
            students_element = ET.SubElement(room_element, "students")
            for student in students:
                student_element = ET.SubElement(students_element, "student")
                ET.SubElement(student_element, "username").text = str(student.username)
                ET.SubElement(student_element, "email").text = str(student.email)

        # Create the XML tree and write it to a file-like object
        tree = ET.ElementTree(root)
        file_obj = HttpResponse(content_type='application/xml')
        tree.write(file_obj, encoding='utf-8', xml_declaration=True)

        # Set the filename for the downloaded file
        file_name = 'room_data.xml'
        file_obj['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return file_obj

    download_room_data.short_description = "Download Room Data as XML"




admin.site.register(Utilities)
admin.site.register(Complaint)
admin.site.register(UserActivityLog)




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    actions = ['download_students', 'remove_students_from_rooms']

    def remove_students_from_rooms(self, request, queryset):
        # Update the Student model
        queryset.update(hostel=None, room_for_student=None)

        # Update the Hostel model
        Hostel.objects.update(room_availability=models.F('total_rooms'))

        # Update the Room model
        Room.objects.update(availability=models.F('capacity'))
        for room in Room.objects.all():
            room.students_in_room.clear()

        # Update the Utilities model
        Utilities.objects.all().update(
            fan=True, bed=True, mattress=True,
            pillows=True, wardrobe=True, book_rack=True,
            tables=True, chairs=True, wall_socket=True,
            tiles=True, paint=True, window=True,
            waste_bin=True, door=True, door_lock=True,
            bulb=True, wiring=True, shower=True,
            towel_holder=True, tap=True, water_closet=True,
            TV=True, decoder=True, other=True
            )

        # Delete all objects from the Complaint model
        Complaint.objects.all().delete()

        self.message_user(request, 'Students removed from rooms and related models updated.')

    remove_students_from_rooms.short_description = 'Remove all students from rooms and update related models'


    def download_students(self, request, queryset):
        # Create the root element of the XML document
        root = ET.Element("students")

        # Iterate over the student queryset and create XML elements
        for student in queryset:
            student_element = ET.SubElement(root, "student")
            ET.SubElement(student_element, "user").text = str(student.user)
            ET.SubElement(student_element, "profile_pic").text = str(student.profile_pic)
            ET.SubElement(student_element, "gender").text = str(student.gender)
            ET.SubElement(student_element, "matric_number").text = str(student.matric_number)
            ET.SubElement(student_element, "department").text = str(student.department)
            ET.SubElement(student_element, "college").text = str(student.college)
            ET.SubElement(student_element, "room_capacity_preference").text = str(student.room_capacity_preference)
            ET.SubElement(student_element, "hostel").text = str(student.hostel)
            ET.SubElement(student_element, "room_for_student").text = str(student.room_for_student)

        # Create the XML tree and write it to a file-like object
        tree = ET.ElementTree(root)
        file_obj = HttpResponse(content_type='application/xml')
        tree.write(file_obj, encoding='utf-8', xml_declaration=True)

        # Set the filename for the downloaded file
        file_name = 'student_data.xml'
        file_obj['Content-Disposition'] = f'attachment; filename="{file_name}"'

        return file_obj
    download_students.short_description = "Download Student Data as XML"



