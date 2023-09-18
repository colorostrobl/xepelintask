from .googleapi import reader, editor
from django.shortcuts import render, redirect
from .forms import TasaEditForm

cells = {str(i): 'B' + str(i+2) for i in range(10)}


def home(request):
    results = reader()
    header = results.pop(0)

    if request.method == 'POST':
        form = TasaEditForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            tasa = form.cleaned_data['tasa']
            for i in range(len(results)):
                if results[i][0] == id:
                    cell = cells.get(str(i))
                    editor(cell, tasa)
            return redirect('/gsheeteditor')
        else:
            return
            #Que pasa si no es valid
    else:
        form = TasaEditForm

    context = {'header': header, 'results': results, 'form': form}
    return render(request, 'GSheetEditor/gsheet.html', context)

