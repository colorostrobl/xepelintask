from .googleapi import reader, editor, send_email
from django.shortcuts import render
from .forms import TasaEditForm
from .functions import tasa_format_checker

cells = {str(i): 'B' + str(i+2) for i in range(10)}


def home(request):
    results = reader()
    header = results.pop(0)
    show_error = False
    show_success = False

    if request.method == 'POST':
        form = TasaEditForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            tasa = form.cleaned_data['tasa']
            keys = (row[0] for row in results)
            if id in keys and tasa_format_checker(tasa):
                for i in range(len(results)):
                    if results[i][0] == id:
                        cell = cells.get(str(i))
                        result = editor(cell, tasa)
                        if result['updatedCells'] == 1:
                            response = send_email([results[i][0], tasa, results[i][2]])
                            if response.status_code == 200:
                                show_success = True
                results = reader()
                header = results.pop(0)
            else:
                show_error = True
        else:
            show_error = True
    else:
        form = TasaEditForm

    context = {'header': header, 'results': results, 'form': form, 'error': show_error, 'success': show_success}
    return render(request, 'GSheetEditor/gsheet.html', context)

