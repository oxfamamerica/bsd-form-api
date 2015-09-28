import traceback, requests
from .models import Example
from .forms import ExampleForm
from django.shortcuts import render
from django.conf import settings
from django.contrib import messages


def example(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)

        if form.is_valid():
            #Under normal circumstances we may be saving this form to the db
            #but instead we are going to send it along to BSD

            #example = Example()
            #example.first_name = form.cleaned_data.get('first_name')
            #example.last_name = form.cleaned_data.get('last_name')
            #example.email = form.cleaned_data.get('email')
            #example.school_name = form.cleaned_data.get('school_name')
            #example.save()

            try:
                bsd_fields = settings.OA_BSD_FIELDS["change_registrations"]

      	        data = {}
                for key in bsd_fields["fields"].keys():
                    try:
                        data[bsd_fields["fields"][key]] = form.cleaned_data.get(key)
                    except Exception as e:
                        print traceback.format_exc()

                res = requests.post(bsd_fields['bsd_url'],data=data)
                res_json = res.json()
                if res_json["status"] == "success":
                    messages.success(request,"Form successfully saved on BSD",extra_tags="success")
                else:
                    messages.error(request,res.text,extra_tags="error")

            except Exception as e:
                print traceback.format_exc()

    else:        
        form = ExampleForm()

    context_data = {'form': form}
    return render(request, 'form.html', context_data)
