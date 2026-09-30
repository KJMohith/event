from django.conf import settings
from django.core.mail import send_mail
from django.http import FileResponse, HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import EventForm, FeedbackForm, MarksForm, RegistrationForm
from .models import Event, Participant
from .utils import generate_certificate_pdf, generate_qr_data


def _send_registration_email(participant, request):
    certificate_url = request.build_absolute_uri(
        reverse('certificate', args=[participant.certificate_hash])
    )
    send_mail(
        'Event Registration Confirmation',
        f'Hi {participant.name},\n\nYou are registered successfully.\nCertificate: {certificate_url}',
        settings.DEFAULT_FROM_EMAIL,
        [participant.email],
        fail_silently=True,
    )


def _participant_rows(request):
    participants = Participant.objects.select_related('event').all()
    for participant in participants:
        participant.qr_data = generate_qr_data(
            request.build_absolute_uri(reverse('certificate', args=[participant.certificate_hash]))
        )
    return participants


def dashboard(request):
    return render(request, 'events/dashboard.html', {
        'participants': _participant_rows(request),
        'events': Event.objects.all(),
        'participant_form': RegistrationForm(),
        'event_form': EventForm(),
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            participant = form.save()
            _send_registration_email(participant, request)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'events/register.html', {'form': form})


@require_POST
def add_participant(request):
    form = RegistrationForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)
    participant = form.save()
    _send_registration_email(participant, request)
    return JsonResponse({'message': 'Participant added successfully.', 'id': participant.pk})


@require_POST
def add_event(request):
    form = EventForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)
    event = form.save()
    return JsonResponse({'message': 'Event added successfully.', 'event': {
        'id': event.id, 'title': event.title, 'event_date': str(event.event_date),
        'description': event.description,
    }})


@require_POST
def delete_participant(request, pk):
    get_object_or_404(Participant, pk=pk).delete()
    return JsonResponse({'message': 'Participant deleted.'})


@require_POST
def delete_event(request, pk):
    get_object_or_404(Event, pk=pk).delete()
    return JsonResponse({'message': 'Event deleted.'})


@require_POST
def toggle_attendance(request, pk):
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'error': 'AJAX request required.'}, status=400)
    participant = get_object_or_404(Participant, pk=pk)
    participant.attendance = not participant.attendance
    participant.save(update_fields=['attendance'])
    return JsonResponse({'attendance': participant.attendance, 'eligible': participant.is_eligible()})


@require_POST
def update_marks(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = MarksForm(request.POST, instance=participant)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors.get_json_data()}, status=400)
    participant = form.save()
    return JsonResponse({'marks': participant.marks, 'eligible': participant.is_eligible()})


def feedback(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=participant)
        if form.is_valid():
            participant.rating = form.cleaned_data['rating']
            participant.feedback_text = form.cleaned_data['comment']
            participant.feedback_given = True
            participant.save(update_fields=['rating', 'feedback_text', 'feedback_given'])
            return redirect('dashboard')
    else:
        form = FeedbackForm(initial={'rating': participant.rating, 'comment': participant.feedback_text})
    return render(request, 'events/feedback.html', {'form': form, 'participant': participant})


def dashboard_stats(request):
    return JsonResponse({
        'participants': Participant.objects.count(),
        'events': Event.objects.count(),
        'attended': Participant.objects.filter(attendance=True).count(),
        'feedback': Participant.objects.filter(feedback_given=True).count(),
    })


def participant_rows(request):
    html = render_to_string('events/participant_rows.html', {'participants': _participant_rows(request)}, request=request)
    return JsonResponse({'html': html})


def certificate(request, hash):
    participant = get_object_or_404(Participant.objects.select_related('event'), certificate_hash=hash)
    if not participant.is_eligible():
        return HttpResponseForbidden(
            'Certificate not available. Attendance, feedback, and marks are required.'
        )
    return FileResponse(
        generate_certificate_pdf(participant),
        as_attachment=True,
        filename=f'certificate_{participant.name.replace(" ", "_")}.pdf',
        content_type='application/pdf',
    )
