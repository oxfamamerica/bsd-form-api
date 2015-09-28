import traceback, csv, copy, uuid, requests
from django.http import HttpResponse
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
