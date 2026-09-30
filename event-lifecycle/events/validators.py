from pathlib import Path

from django.core.exceptions import ValidationError

MAX_FILE_SIZE = 2 * 1024 * 1024
RECEIPT_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.pdf'}
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png'}


def _validate_file(file_obj, extensions, label):
    if file_obj.size > MAX_FILE_SIZE:
        raise ValidationError(f'{label} must be 2MB or smaller.')
    extension = Path(file_obj.name).suffix.lower()
    if extension not in extensions:
        allowed = ', '.join(sorted(extensions))
        raise ValidationError(f'{label} must use one of: {allowed}.')


def validate_receipt(file_obj):
    _validate_file(file_obj, RECEIPT_EXTENSIONS, 'Receipt')


def validate_photo(file_obj):
    _validate_file(file_obj, PHOTO_EXTENSIONS, 'Photo')
