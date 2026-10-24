
from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('issued_to', 'name', 'status', 'email')
    list_filter = ('status',)
    actions = ['approve_certificates']

    def approve_certificates(self, request, queryset):
        for cert in queryset:
            if cert.status == 'Pending':
                cert.status = 'Approved'

                # Generate certificate hash
                input_str = f"{cert.name}{cert.issued_to}{cert.description}"
                cert_hash = hashlib.sha256(input_str.encode()).hexdigest()
                cert.cert_hash = cert_hash

                # Send certificate
                from .utils import generate_certificate_pdf
                cert_pdf = generate_certificate_pdf(cert.name, cert.issued_to, cert.description)

                email = EmailMessage(
                    subject='Your Digital Certificate',
                    body=f'Hello {cert.issued_to},\n\nAttached is your certificate.\nCertificate Hash: {cert.cert_hash}',
                    from_email='saikumardatapoint1@gmail.com',
                    to=[cert.email],
                )
                email.attach(f"{cert.issued_to}_certificate.pdf", cert_pdf, 'application/pdf')
                email.send()

                cert.save()
        self.message_user(request, "Selected certificates approved and emailed.")

    approve_certificates.short_description = "Approve selected certificates"
