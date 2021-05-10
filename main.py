import requests
import wget
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM
import os
from PyPDF2 import PdfFileMerger, PdfFileReader

is_teacher = ''
selected = True
while selected:
    teacher = input('P para professor, A para aluno. ')
    if teacher.capitalize() == 'P':
        is_teacher = 'TE'
        selected = False
    elif teacher.capitalize() == 'A':
        is_teacher = 'SE'
        selected = False
    else:
        print('Erro, tenta outra-vez.')

checking = True
while checking:
    name_book = input('Nome do Livro ')
    manual_id = input('Qual o ISBN? ')
    part = input('Qual a parte? Se nao souberes usa "1" ')
    part = '0' + part
    first_page = f'https://www.escolavirtual.pt/emanuais-cs/{manual_id}-{is_teacher}-{part}/html5/{manual_id}-{is_teacher}-{part}-lite//OPS/images/page0001.svgz'
    exists = requests.post(first_page)
    if exists.status_code == 405:
        checking = False
        print('Comecando Download.')
    else:
        print('O manual n existe. Tenta outra-vez.')

# List of pages to merge in PDF
pages_downloaded = []
page_num = 1

run = True
# Download SVG page, convert it in PDF and remove SVG page.
while run:
    for i in range(1, 9999):

        page = '%0.4d' % i
        file_svg = 'page' + page + '.svg'
        file_pdf = 'page' + page + '.pdf'
        manual = f'https://www.escolavirtual.pt/emanuais-cs/{manual_id}-{is_teacher}-{part}/html5/{manual_id}-{is_teacher}-{part}-lite//OPS/images/page{page}.svgz'
        response = requests.post(manual)
        # Check if Page exists
        if response.status_code == 405:
            run = True
        else:
            run = False
            break
        print(f'Descarregando pagina {page_num}')
        page_num += 1
        pages_downloaded.append(file_pdf)
        wget.download(manual, file_svg)
        convert = svg2rlg(file_svg)
        renderPDF.drawToFile(convert, file_pdf)
        os.remove(file_svg)
        print('Removendo ficheiros temporarios.')

    run = False

print('Criando PDF.')
mergedObject = PdfFileMerger()
for i in range(len(pages_downloaded)):
    page = pages_downloaded[i]
    mergedObject.append(PdfFileReader(str(page), 'rb'))

mergedObject.write(f"{name_book}.pdf")

print('Apagando ficheiro temporarios.')

for i in range(len(pages_downloaded)):
    page = pages_downloaded[i]
    os.remove(page)
    print('Ficheiro removido.')


print(f'Concluido. O livro {name_book} foi descarregado.')