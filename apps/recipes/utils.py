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

    def print_head():
        pdf_canvas.setFont('Arial', 40)
        pdf_canvas.drawString(150, 800, 'Список покупок')
        pdf_canvas.setFont('Arial', 20)

    buffer = io.BytesIO()
    pdf_canvas = canvas.Canvas(buffer)
    font = ttfonts.TTFont('Arial', os.path.join(settings.BASE_DIR,
                                                'static', 'fonts',
                                                'arial.ttf'))
    pdfmetrics.registerFont(font)
    print_head()
    line_y = -1
    for pos, val in enumerate(ingredients):
        line_y += 1
        string = (f'{pos + 1}. {val["recipe__ingredients__name"]} '
                  f'({val["recipe__ingredients__unit"]}): '
                  f'{val["quantity"] or ""}')
        pdf_canvas.drawString(50, 750 - 50 * line_y, string)
        if (pos + 1) % 15 == 0:
            pdf_canvas.showPage()
            line_y = -1
            print_head()

    pdf_canvas.showPage()
    pdf_canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=filename)
