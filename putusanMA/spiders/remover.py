import sys
#import slate3k as slate 
from io import StringIO
from pdfminer.high_level import extract_text
from pdfminer.high_level import extract_text_to_fp
from PyPDF4 import PdfFileReader, PdfFileWriter
from PyPDF4.pdf import ContentStream
from PyPDF4.generic import TextStringObject, NameObject
from PyPDF4.utils import b_

def remove_watermark(wm_text, inputFile, outputFile):
    
    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)

            for operands, operator in content.operations:
                if operator == b_("Tj"):
                    text = operands[0]

                    if isinstance(text, str) and text.startswith(wm_text):
                        operands[0] = TextStringObject('')

            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)

#def read_pdf(file):
#    with open(file, 'rb') as f:
#        extracted_text = slate.PDF(f)
#        print(extracted_text)
def read_pdf(file):
    output_string = StringIO()
    with open(file, 'rb') as f:
        extract_text_to_fp(f, output_string)
        text = output_string.getvalue().strip().replace('DisclaimerKepaniteraan Mahkamah Agung Republik Indonesia berusaha untuk selalu mencantumkan informasi paling kini dan akurat sebagai bentuk komitmen Mahkamah Agung untuk pelayanan publik, transparansi dan akuntabilitaspelaksanaan fungsi peradilan. Namun dalam hal-hal tertentu masih dimungkinkan terjadi permasalahan teknis terkait dengan akurasi dan keterkinian informasi yang kami sajikan, hal mana akan terus kami perbaiki dari waktu kewaktu.Dalam hal Anda menemukan inakurasi informasi yang termuat pada situs ini atau informasi yang seharusnya ada, namun belum tersedia, maka harap segera hubungi Kepaniteraan Mahkamah Agung RI melalui :Email : kepaniteraan@mahkamahagung.go.id    Telp : 021-384 3348 (ext.318)','')
        print(text)

wm_text = 'Mahkamah Agung'
inputFile = sys.argv[1]
outputFile = f'{inputFile.replace(".pdf","")}_output.pdf'  
remove_watermark(wm_text, inputFile, outputFile)
read_pdf(outputFile)

