from django.contrib import admin


from .models import Stream,Course,Location,College,CollegeCourse,Enquiry,CourseType

# Register your models here.


admin.site.register(Stream)
admin.site.register(Course)
admin.site.register(Enquiry)
admin.site.register(Location)
admin.site.register(College)
admin.site.register(CollegeCourse)
admin.site.register(CourseType)