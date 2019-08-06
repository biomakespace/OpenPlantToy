from django.http import HttpResponse
from django.template import loader, Context

def circuit(request):
    template = loader.get_template("genetic_circuit_controller/templates/circuit.html")
    response = template.render()
    return HttpResponse(response)
