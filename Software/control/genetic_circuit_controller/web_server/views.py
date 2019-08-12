
from django.http import HttpResponse, JsonResponse
from django.template import loader, Context
from control.check_circuit import get_instance


def circuit(request):
    template = loader.get_template("genetic_circuit_controller/templates/circuit.html")
    response = template.render()
    return HttpResponse(response)


def check_circuit(request):
    checker = get_instance()
    circuit_information = checker.check()
    return JsonResponse(circuit_information)