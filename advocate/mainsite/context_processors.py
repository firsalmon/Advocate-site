from .forms import LeadForm

def lead_form_processor(request):
    return {
        'form': LeadForm()
    }