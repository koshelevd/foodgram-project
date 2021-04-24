"""Util functions for 'recipes' app."""
import io
import os

from django.conf import settings
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics, ttfonts


def create_pdf(ingredients, filename):
    """
    Create pdf-document with filename specified.
    """
    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer)

    font = ttfonts.TTFont('Arial', os.path.join(settings.BASE_DIR,
                                                'static', 'fonts',
                                                'arial.ttf'))
    pdfmetrics.registerFont(font)

    pdf_canvas.setFont('Arial', 40)
    pdf_canvas.drawString(150, 800, 'Список покупок')
    pdf_canvas.setFont('Arial', 20)

    for pos, val in enumerate(ingredients):
        string = (f'{pos + 1}. {val["recipe__ingredients__name"]} '
                  f'({val["recipe__ingredients__unit"]}): '
                  f'{val["quantity"]}')
        pdf_canvas.drawString(50, 750 - 50 * pos, string)

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)
