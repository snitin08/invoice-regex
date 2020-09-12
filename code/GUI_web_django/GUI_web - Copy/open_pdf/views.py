from django.shortcuts import render,redirect,reverse
from django.core.files.uploadhandler import TemporaryFileUploadHandler
import PyPDF2 
import os
from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    return render(request,'open_pdf/index.html',{})

def view_pdf(request):
    print(request.POST)
    print('FILES',request.FILES)
    filename = request.FILES.get('filename')
    
    if request.method == 'POST' and request.FILES['filename']:
        print(filename.file)
        fs = FileSystemStorage()
        myfile = request.FILES.get('filename')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        print("upload url",uploaded_file_url)
        print("media URL",settings.MEDIA_ROOT)
        file_url = os.path.join(settings.BASE_DIR,uploaded_file_url[1:].replace('/','\\'))
        #file_url = settings.BASE_DIR.replace('\\','/')
        print(file_url)
        

        #Convert to list of images
        pdfFileObj = open(file_url.replace("%20"," "), 'rb') 
        from pdf2image import convert_from_path
        dpi = 500 # dots per inch
        
        pages = convert_from_path(file_url.replace("%20"," ") ,dpi )
        image_paths = []
        for i in range(len(pages)):
            page = pages[i]
            image_path = 'media/output_'+str(i)+'.jpg'
            image_paths.append(
                os.path.join('/media/','output_'+str(i)+'.jpg')
            )
            page.save(image_path, 'JPEG')
        print(image_paths)
        request.session['image_paths'] = image_paths
        #redirect(reverse('open_pdf:annotate_pdf', kwargs={ "images":image_paths }))
        #return render(request,'open_pdf/annotate.html',{"images":image_paths})
        return redirect('open_pdf:annotate_pdf')
    return render(request,'open_pdf/index.html',{})

def annotate_pdf(request):
    image_paths = request.session.get('image_paths')
    return render(request,'open_pdf/annotate.html',{"images":image_paths})