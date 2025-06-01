import os
import magic

def validate_is_image(file):
    check = True
    valid_mime_types = ['image/jpeg', 'image/gif','image/png']
    valid_file_extensions = ['.jpeg', '.jpg', '.gif', '.png']
    file_mime_type = magic.from_buffer(file.read(2048), mime=True)
    if file_mime_type not in valid_mime_types:
        check = False
    ext = os.path.splitext(file.name)[1]
    if ext.lower() not in valid_file_extensions:
        check = False
    return check