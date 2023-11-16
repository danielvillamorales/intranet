from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from pdf2docx import Converter
import PyPDF2
import PIL.Image as Image

def convertpdftoword(request):
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']

        # Guardar el archivo PDF en el sistema de archivos temporal de Django
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        pdf_path = fs.path(filename)

        # Convertir el PDF a Word
        docx_file_path = convert_pdf_to_docx(pdf_path)
        nombre = pdf_file.name.replace('.pdf','')
        # Descargar el archivo Word resultante
        with open(docx_file_path, 'rb') as docx_file:
            response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={nombre}.docx'

        # Eliminar los archivos temporales
        fs.delete(filename)
        fs.delete(docx_file_path)

        return response

    return render(request, 'convertpdftoword.html')

def convert_pdf_to_docx(pdf_path):
    # Nombre de archivo docx resultante
    docx_filename = pdf_path.replace('.pdf', '.docx')

    # Convertir PDF a Word
    cv = Converter(pdf_path)
    cv.convert(docx_filename, start=0, end=None )
    cv.close()

    return docx_filename


def unir_pdfs(request):
    if request.method == 'POST' and request.FILES.getlist('pdf_files'):
        pdf_files = request.FILES.getlist('pdf_files')

        # Verifica que todos los archivos sean archivos PDF
        for pdf_file in pdf_files:
            if not pdf_file.name.endswith('.pdf'):
                return HttpResponse("Error: Todos los archivos deben ser archivos PDF.")

        # Crea un objeto PdfMerger de PyPDF2
        pdf_merger = PyPDF2.PdfMerger()

        # Agrega cada archivo PDF al objeto PdfMerger
        for pdf_file in pdf_files:
            pdf_merger.append(pdf_file)

        # Crea un HttpResponse con el contenido del archivo combinado
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=pdfs_unidos.pdf'

        # Escribe el contenido del archivo combinado en la respuesta
        pdf_merger.write(response)

        return response

    return render(request, 'unir_pdfs.html')



def menu_utiles(request):
    return render(request, 'menu_utiles.html')