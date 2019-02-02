from django.shortcuts import render_to_response, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views import generic
from .forms import GroupForm

# Create your views here.

def logout(req):
    return render_to_response('accounts/logout.html')

# https://stackoverflow.com/questions/51250903/how-to-assign-group-to-user-from-a-registration-form-for-user-in-django
def select_group(req):
    tmpl = loader.get_template('accounts/select_group.html')
    if req.method == 'POST':

        form = GroupForm(req.POST)

        if form.is_valid():
            group = Group.objects.get(id=req.POST['user_groups'])
            user = req.user
            user.groups.add(group)

            group_form = 'loans:' + group.name + '_form'

            print ("REDIRECTING TO " + group_form)
            return redirect(group_form)

    else:
        form = GroupForm()


    context = {
        'form': form
    }

    return HttpResponse(tmpl.render(context, req))


# NOTE: only admin user can create accounts for now
#class Register(generic.CreateView):
#    form_class = UserCreationForm
#    success_url = reverse_lazy('login')
#    template_name = 'registration/register.html'



# validate login/username
