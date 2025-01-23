from django.shortcuts import render


def show_phones(request):
	return render(request, 'index.html')
