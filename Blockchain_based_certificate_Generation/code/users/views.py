# views.py
from django.shortcuts import render, redirect
from .models import Certificate
from .forms import CertificateForm
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage
import hashlib
from .utils import generate_certificate_pdf

# User submits request
from django.contrib import messages

def issue_certificate(request):
    
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.status = "Pending"
            instance.save()

            messages.success(request, 'Your request has been submitted and is waiting for admin approval.')
            return redirect('issue')  # or render success.html
    else:
        form = CertificateForm()
    return render(request, 'issue_certificate.html', {'form': form})


# Admin login view
def admin_login(request):
    if request.method == 'POST':
        if request.POST['username'] == 'authority' and request.POST['password'] == 'authority':
            request.session['admin'] = True
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'admin_login.html')

# Admin dashboard
def admin_dashboard(request):
    if not request.session.get('admin'):
        return redirect('admin_login')
    
    certs = Certificate.objects.all().order_by('-id')  # Show all certs, latest first
    return render(request, 'admin_dashboard.html', {'certs': certs})

# Admin approves certificate
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def approve_certificate(request, cert_id):
    if not request.session.get('admin'):
        return redirect('admin_login')

    cert = Certificate.objects.get(id=cert_id)

    # Generate hash
    input_str = f"{cert.name}{cert.issued_to}{cert.description}"
    cert.cert_hash = hashlib.sha256(input_str.encode()).hexdigest()

    # Generate QR code (link or hash)
    qr_data = f"http://yourdomain.com/verify?cert_hash={cert.cert_hash}"
    qr_img = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer)
    qr_bytes = qr_buffer.getvalue()

    # Generate PDF with QR code
    cert_pdf = generate_certificate_pdf(cert.name, cert.issued_to, cert.description, qr_bytes)

    # Send email
    email = EmailMessage(
        subject='Your Approved Digital Certificate',
        body=f'Hello {cert.issued_to},\n\nYour certificate is approved.\n\nHash: {cert.cert_hash}\nYou can also scan the QR code embedded in the certificate.',
        from_email='saikumardatapoint1@gmail.com',
        to=[cert.email],
    )
    email.attach(f"{cert.issued_to}_certificate.pdf", cert_pdf, 'application/pdf')
    email.send()

    cert.status = 'Approved'
    cert.email_sent = True
    cert.issued_at = timezone.now()
    cert.save()

    messages.success(request, f"Certificate for {cert.issued_to} sent successfully.")
    return redirect('admin_dashboard')

# Home
def home(request):
    return render(request, 'home.html')

def verify_certificate(request):
    result = None
    cert_hash = request.GET.get('cert_hash') or request.POST.get('cert_hash')

    if cert_hash:
        try:
            result = Certificate.objects.get(cert_hash=cert_hash)
        except Certificate.DoesNotExist:
            result = False

    return render(request, 'verify_certificate.html', {'result': result})

# views.py
def reject_certificate(request, cert_id):
    if not request.session.get('admin'):
        return redirect('admin_login')

    cert = Certificate.objects.get(id=cert_id)
    cert.status = 'Rejected'
    cert.save()

    messages.warning(request, f"Certificate request from {cert.issued_to} was rejected.")
    return redirect('admin_dashboard')


def index(request):
    return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.contrib import messages

def validator_login(request):
    if request.method == 'POST':
        validator_id = request.POST.get('validator_id')
        validator_name = request.POST.get('validator_name')

        # For now, we use a fixed validator; you can extend with models later
        if validator_id == 'validator' and validator_name.lower() == 'validator':
            request.session['validator'] = True
            return redirect('verify')
        else:
            messages.error(request, 'Invalid Validator Credentials')

    return render(request, 'validator_login.html')