ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'md', 'stl', 'dwg', 'dxf', 'svg'}

def valid_email(email):
    return True if email.endswith('@cooper.edu') else False

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS