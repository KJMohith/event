from django.contrib import admin
from .models import Event, Participant


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('event_date', 'title')


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'email', 'transaction_id', 'attendance', 'feedback_given', 'marks')
    list_filter = ('attendance', 'feedback_given', 'event')
    search_fields = ('name', 'email', 'transaction_id')
