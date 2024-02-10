from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import Stream, Course, Location,College,CollegeCourse,Enquiry,CourseType
from django.http import JsonResponse

from django.contrib.staticfiles import finders
import json
from django.db.models import Min, Max

def get_course_prices(request):
    if request.method == 'GET':
        course_id = request.GET.get('course_id')

        if course_id:
            # Fetch minimum and maximum prices for the selected course from colleges
            prices = CollegeCourse.objects.filter(course_id=course_id).aggregate(min_price=Min('price'), max_price=Max('price'))
            return JsonResponse({'min_price': prices['min_price'], 'max_price': prices['max_price']})

    return JsonResponse({'error': 'Invalid request'}, status=400)



def index(request):
    streams = Stream.objects.all()
    course_types = CourseType.objects.all()
    courses = Course.objects.all()
    locations = Location.objects.all()

    return render(request, 'index.html', {
        'streams': streams,
        'course_types': course_types,
        'courses': courses,
        'locations': locations,
    })


def college_list(request):
    if request.method == 'GET':
        stream_id = request.GET.get('stream')
        course_type_id = request.GET.get('type')
        course_id = request.GET.get('course')
        location_id = request.GET.get('location')

        # Check if any of the required parameters is missing
        if not stream_id or not course_type_id or not location_id:
            message = "Please select values for Stream, Course Type, and Location."
            return render(request, 'college.html', {'message': message})

        # Filter colleges based on selected values
        colleges = College.objects.filter(
            collegecourse__course__stream_id=stream_id,
            collegecourse__course__course_type_id=course_type_id,
            location_id=location_id
        )

        # If course_id is provided, further filter colleges
        if course_id:
            colleges = colleges.filter(collegecourse__course_id=course_id)
            selected_course = Course.objects.get(id=course_id)
        else:
            selected_course = None

        selected_course_type = CourseType.objects.get(id=course_type_id) if course_type_id else None

        colleges_count = colleges.count()

        # Check if no colleges are found
        if colleges_count == 0:
            message = "No colleges found based on the provided criteria."
            return render(request, 'college.html', {'message': message})

        return render(request, 'college.html', {
            'colleges': colleges,
            'colleges_count': colleges_count,
            'selected_course': selected_course,
            'selected_course_type': selected_course_type,
        })

# def college_list(request):
#     if request.method == 'GET':
#         stream_id = request.GET.get('stream')
#         course_type_id = request.GET.get('type')
#         course_id = request.GET.get('course')
#         location_id = request.GET.get('location')

#         # Check if any of the required parameters is missing
#         if not stream_id or not course_type_id or not location_id:
#             message = "Please select values for Stream, Course Type, and Location."
#             return render(request, 'college.html', {'message': message})

#         # Filter colleges based on selected values
#         colleges = College.objects.filter(
#             collegecourse__course__stream_id=stream_id,
#             collegecourse__course__course_type_id=course_type_id,
#             location_id=location_id
#         )

#         # If course_id is provided, further filter colleges
#         if course_id:
#             colleges = colleges.filter(collegecourse__course_id=course_id)
#             selected_course = Course.objects.get(id=course_id)
#         else:
#             selected_course = None

#         selected_course_type = CourseType.objects.get(id=course_type_id) if course_type_id else None

        

#         colleges_count = colleges.count()

#         return render(request, 'college.html', {
#             'colleges': colleges,
#             'colleges_count': colleges_count,
#             'selected_course': selected_course,
#             'selected_course_type': selected_course_type,
           
#         })


# def college_list(request):
#     if request.method == 'GET':
#         stream_id = request.GET.get('stream')
#         course_type_id = request.GET.get('type')
#         course_id = request.GET.get('course')
#         location_id = request.GET.get('location')

#         # Check if any of the required parameters is missing
#         if not stream_id or not course_type_id or not location_id:
#             message = "Please select values for Stream, Course Type, and Location."
#             return render(request, 'college.html', {'message': message})

#         # Filter colleges based on selected values
#         colleges = College.objects.filter(
#             collegecourse__course__stream_id=stream_id,
#             collegecourse__course__course_type_id=course_type_id,
#             location_id=location_id
#         )

#         # If course_id is provided, further filter colleges
#         if course_id:
#             colleges = colleges.filter(collegecourse__course_id=course_id)
#             selected_course = Course.objects.get(id=course_id)
#         else:
#             selected_course = None

#         selected_course_type = CourseType.objects.get(id=course_type_id) if course_type_id else None

#         colleges_count = colleges.count()

#         return render(request, 'college.html', {
#             'colleges': colleges,
#             'colleges_count': colleges_count,
#             'selected_course': selected_course,
#             'selected_course_type': selected_course_type,
#         })







def college_details(request, college_id, selected_course_id):
    college = get_object_or_404(College, id=college_id)
    selected_course = None
    college_course_details = None
    course_type = None

    if selected_course_id:
        selected_course = get_object_or_404(Course, id=selected_course_id)
        college_course_details = get_object_or_404(CollegeCourse, college=college, course=selected_course)
        course_type = selected_course.course_type

    context = {
        'college': college,
        'selected_course': selected_course,
        'college_course_details': college_course_details,
        'course_type': course_type,
    }
    return render(request, 'college_details.html', context)


def college_detail(request,college_id):
    college = get_object_or_404(College, id=college_id)
    college_courses = CollegeCourse.objects.filter(college=college)

    # Extracting unique streams and course types from college courses
    streams = set(course.course.stream for course in college_courses)
    course_types = set(course.course.course_type for course in college_courses)

    context = {
        'college': college,
        'college_courses': college_courses,
        'streams': streams,
        'course_types': course_types,
    }

    return render(request,'college_description.html', context)





def contact(request, college_id, college_course_details_id):

   

    with open("static/countrycodes.json") as json_file:
            country_codes = json.load(json_file)


    college = get_object_or_404(College, id=college_id)
    college_course_details = get_object_or_404(CollegeCourse, id=college_course_details_id)

    context = {
        'college': college,
        'college_course_details': college_course_details,
        'country_codes': country_codes,
    }
    return render(request, 'contact.html', context)




def submit_enquiry(request):
    if request.method == 'POST':
        college_id = request.POST.get('college_id')
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country')

        college = get_object_or_404(College, id=college_id)
        course = get_object_or_404(Course, id=course_id)

        # Fetch the CollegeCourse details based on college and course
        college_course_details = get_object_or_404(CollegeCourse, college=college, course=course)

        # Create an Enquiry instance and save it to the database
        enquiry = Enquiry(
            course=course,
            college=college,
            location=college.location,
            price=college_course_details.price,
            name=name,
            email=email,
            country_code=country_code,
            phone=phone,
            status=1,  # Set default status to 'Pending'
            note='',  
        )
        enquiry.save()

        # Redirect to a thank you page or another appropriate page
        return redirect('thank_you_page')

    # Handle invalid request method (GET or other)
    return redirect('error_page')


def thank_you_page(request):
    return render(request, 'thank_you.html')


def error_page(request):
    return render(request, 'error.html')



