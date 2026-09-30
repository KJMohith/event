import uuid
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import events.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('event_date', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['event_date', 'title']},
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('transaction_id', models.CharField(max_length=100, unique=True)),
                ('receipt', models.FileField(upload_to='receipts/', validators=[events.validators.validate_receipt])),
                ('photo', models.ImageField(upload_to='photos/', validators=[events.validators.validate_photo])),
                ('attendance', models.BooleanField(default=False)),
                ('feedback_given', models.BooleanField(default=False)),
                ('feedback_text', models.TextField(blank=True)),
                ('rating', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('marks', models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('certificate_hash', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='events.event')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='participant',
            index=models.Index(fields=['event', '-created_at'], name='events_part_event_i_9c7c4e_idx'),
        ),
        migrations.AddIndex(
            model_name='participant',
            index=models.Index(fields=['attendance'], name='events_part_attend_7ddf1a_idx'),
        ),
    ]
