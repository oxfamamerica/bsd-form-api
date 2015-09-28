# BSD Form API
An example of using the new Blue State Digital form api found at: 

http://tools.bluestatedigital.com/kb/entry/new-signup-api/

# Requirements

- Python 2.7+
- Django 1.7+

#Use case 1

##Send data in a model to BSD via the admin.

- Setup your model so it looks something like this:
```
from django.db import models

class Example(models.Model):
    '''
    An example of a model whose data we will need to send to BSD
    '''
    email = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    saved_on_bsd = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Example"
        verbose_name_plural = "Examples"
        ordering = ("-id",)

```

- Setup the field mappings in settings so it looks like this:
```
OA_BSD_FIELDS = {
    "change_registrations": {
        "bsd_url": "https://secure2.oxfamamerica.org/page/sapi/bsd-testing",
        "fields": {
            "first_name": "firstname",
            "last_name": "lastname",
            "email": "email",
            "school_name": "custom-754",
        }
    }
}
```
You are mapping the model field name to the BSD form field name.

- Setup your admin.py so it looks like this:

```
import traceback
from django.contrib import admin
from example.models import Example
from django.conf import settings
from django.contrib import messages


class ExampleAdmin(admin.ModelAdmin):

    actions = ["update_bsd"]
    search_fields = ["first_name","last_name","email"]
    list_display = ('id','first_name','last_name','email','saved_on_bsd')
    list_display_links = ('id',)

    def update_bsd(self, request, queryset):
        bsd_fields = settings.OA_BSD_FIELDS["change_registrations"]
        for example in queryset:
            try:

      	        data = {}
                for key in bsd_fields["fields"].keys():
                    try:
                        data[bsd_fields["fields"][key]] = getattr(example,key,None)
                    except Exception as e:
                        print traceback.format_exc()

                res = requests.post(bsd_fields['bsd_url'],data=data)
                res_json = res.json()
                if res_json["status"] == "success":
                    example.saved_on_bsd = True
                    example.save()

            except Exception as e:
                print traceback.format_exc()

admin.site.register(Example, ExampleAdmin)
```

- Now go to http://your-url/admin/example/ - select the entries of data you want to submit and then select the "Update BSD" action. Your data will be sent to BSD and if it successfull then the "saved_on_bsd" field will be set to True.

#Use case 2

##Forward data from a form straight to BSD - without saving it locally.

- Setup your model so it looks like the 'Use case 1' above.

- Setup your field mappings settings so it looks like the 'Use case 1' above.

- Setup your forms.py so it looks something like this.

```
from django import forms

from .models import Example

class ExampleForm(forms.ModelForm):

    class Meta:
        model = Example
        fields = ('first_name', 
                  'last_name', 
                  'email',
                  'school_name')
        
```

- Setup your views.py so it looks something like this:

```
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
```

- Setup your urls.py so it looks something like this:

```
from django.conf.urls import include, url
from example import views

urlpatterns = [
    url(r'^example-form/', views.example),
]

```

- Finally setup your form template so it looks something like this:

```
{% if messages %}
<div class="alert alert-dismissable" data-alert="alert">
<div class='messages {% for message in messages %}messages-{{message.tags}}{% endfor %}'>
    {% for message in messages %}
        {{message|safe}}
    {% endfor %}
</div>

</div>
{% endif %}

<form action="" method="post">{% csrf_token %}
{{ form.as_p }}
<input type="submit" value="Submit" />
</form>
```

- Now go to http://your-url/example-form/ - submit a form and you should see it populate your BSD form
