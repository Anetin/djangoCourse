from django.shortcuts import render

# Create your views here.
from .models import UserMessage
def getform(request):
    message = None
    all_message = UserMessage.objects.filter(name='1212')
    if all_message:
        message = all_message[0]
    # all_message = UserMessage.objects.all()
    # for message in all_message:
    #     print message.name

    # if request.method == "POST":
    #     name = request.POST.get('name', '')
    #     message =request.POST.get('message', '')
    #     address = request.POST.get('address', '')
    #     email = request.POST.get('email', '')
    #
    #     user_message = UserMessage()
    #     user_message.name = name
    #     user_message.message = message
    #     user_message.address = address
    #     user_message.email = email
    #     user_message.object_id = "2132143"
    #     user_message.save()

    return render(request, 'message_form.html', {
        "message": message
    })