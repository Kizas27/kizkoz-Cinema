import cairosvg as cairosvg
from django.core.mail import EmailMessage
from fpdf import FPDF
from Cinema.models import Sessions, Seats, Tickets


class PDF(FPDF):
    pass


def create_tickets():
    sessions = Sessions.objects.all()
    seats = Seats.objects.all()
    ticket_session_list = list()

    for ticket in Tickets.objects.all():
        if not ticket.session_id in ticket_session_list:
            ticket_session_list.append(ticket.session_id)
    for session in sessions:
        if not session.id in ticket_session_list:
            for seat in seats:
                Tickets.objects.create(
                    session_id=session.id,
                    seat_id=seat.id,
                    price=5.99,
                    sold=False
                )


def qr_generator(data):
    import qrcode.image.svg
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.make(fit=True)

    factory = qrcode.image.svg.SvgPathImage
    tickets = Tickets.objects.get(id=data)
    print(tickets.seat)
    qr_data = f"Laikas: {tickets.session}\n" \
              f"Eile: {tickets.seat.row_id}\n" \
              f"Vieta: {tickets.seat.seat_id}"

    img = qrcode.make(data=qr_data, image_factory=factory)
    img.save(stream=f"{data}.svg")
    cairosvg.svg2png(url=f"{data}.svg", write_to=f"{data}.png")
    return img


def ticket_pdf_create(ticket):
    tickets = Tickets.objects.get(id=ticket)
    pdf = PDF(format='Letter')
    pdf.add_page()
    pdf.set_font('Times', 'B', 14)
    pdf.cell(w=210, h=60, txt=f"", border=0, ln=1, align='C')
    pdf.image(f"{ticket}.png", 92, 80, w=0, h=0, )
    pdf.cell(w=210, h=8, txt=f"Filmas: {tickets.session.movie}", border=0, ln=1, align='C')
    pdf.cell(w=210, h=60, txt=f"", border=0, ln=1, align='C')
    pdf.cell(w=210, h=8, txt=f"Laikas: {tickets.session}", border=0, ln=1, align='C')
    pdf.cell(w=210, h=8, txt=f"Eile: {tickets.seat.row_id}", border=0, ln=1, align='C')
    pdf.cell(w=210, h=8, txt=f"Vieta: {tickets.seat.seat_id}", border=0, ln=1, align='C')
    pdf.output(f"{ticket}.pdf", 'F')
    return pdf


def ticket_send(ticket_id, customers_email):
    for ticket in ticket_id:
        qr_generator(ticket)
        ticket_pdf_create(ticket)
    mail_subject = 'KizKoz Cinema - buying tickets'
    message = f"Ačiū,kad pirkote bilietus"
    email_s = EmailMessage(mail_subject, message, to=[customers_email])
    for ticket in ticket_id:
        email_s.attach_file(f"{ticket}.pdf")
    email_s.send()
    pass
