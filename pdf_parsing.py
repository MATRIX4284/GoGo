import pymupdf # imports the pymupdf library
import pandas as pd 
import fitz  # import PyMuPDF

import numpy as np


import numpy as np
import matplotlib.pyplot as plt
import os
import json


def download_images_per_page(doc,doc_name,page,page_index,DPI):
    image_list = page.get_images()
    # print the number of images found on the page
    if image_list:
        print(f"Found {len(image_list)} images on page {page_index}")
    else:
        print("No images found on page", page_index)

    for image_index, img in enumerate(image_list, start=1): # enumerate the image list
        xref = img[0] # get the XREF of the image
        pix = pymupdf.Pixmap(doc, xref) # create a Pixmap
        #pix = pymupdf.Pixmap(doc.extract_image(xref)["image"])
        #mask = pymupdf.Pixmap(doc.extract_image(smask)["image"])
        #pix = pymupdf.Pixmap(pix1, mask)

        ### Commented Out Section for showing images################################
        #if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
        #    pix = pymupdf.Pixmap(pymupdf.csRGB, pix)            
        # %matplotlib inline
        #pix = item.get_pixmap(dpi=DPI)
        #img = np.ndarray([pix.h, pix.w, 3], dtype=np.uint8, buffer=pix.samples_mv)
        #plt.figure(dpi=DPI)  # set the figure's DPI
        #plt.title(title)  # set title of image
        #_ = plt.imshow(img, extent=(0, pix.w * 72 / DPI, pix.h * 72 / DPI, 0))
        
        #############################################################################
            
        print('Image:')
        print(type(img))
            
        pix.save("./Parsed_PDF_Output/"+doc_name+"/"+"page_"+str(page_index+1)+"/image_%s.jpg" % (image_index)) # save the image as png
        pix = None
        
    return True



def extract_images_per_page(doc,doc_name,page_index):
    print("IN extract_images_per_page")
    page_image_dict={}
    page_number=page_index+1
    page = doc[page_index] # get the page by index
    
    ####Get Images along with the metadata of it in the following order:
    #(xref, smask, width, height, bpc, colorspace, alt. colorspace, name, filter, referencer)
    #xref (int) is the image object number
    #smask (int) is the object number of its soft-mask image
    #width and height (ints) are the image dimensions
    #bpc (int) denotes the number of bits per component (normally 8)
    #colorspace (str) a string naming the colorspace (like DeviceRGB)
    #alt. colorspace (str) is any alternate colorspace depending on the value of colorspace
    #name (str) is the symbolic name by which the image is referenced
    #filter (str) is the decode filter of the image (Adobe PDF References, pp. 22).
    #referencer (int) the xref of the referencer. Zero if directly referenced by the page. Only present if full=True.
    
    image_list = page.get_images(full=True) #full=True as it will give the if any other pages are referencing
                                            #the image.
    
    #for image in image_list:
    #    xref, smask, width, height, bpc, colorspace, alt_colorspace, name, filter, referencer=image
    #    print("width")
    #    print(width)
    ###########################################################################################################
    
    img_cnt=len(image_list)
    npy_img_lst=[]
    DPI=150
    title=""
    ###########Extraction Of Images in Numpy Format############
    
    for image_index, img in enumerate(image_list, start=1): # enumerate the image list
        
            img_meta_dict={}
            
            xref = img[0] # get the XREF of the image
            
            smask= img[1] # Get Object number of the Soft Mask of the Image
            
            width = img[2]
            print("width")
            print(width)
            
            height = img[3]
            print("height")
            print(height)
            
            num_bits = img[4] # Nuber of bits that is being used to represent the smallest component of the image
            colorspace = img[5] #colorspace of the image
            alt_colorspace = img[6] #colorspace of the image
            sym_name = img[7] #Symbolic name of the image
            img_filter = img[8] #decode filter of the image (Adobe PDF References, pp. 22)
            img_ref = img[9] #xref of the referencer. Zero if directly referenced by the page. 
                             #Only present if full=True.
                
            
            
            
            
            img_meta_dict["img_obj_num"]=xref
            img_meta_dict["smask_obj_num"]=smask
            img_meta_dict["width"]=width
            img_meta_dict["height"]=height
            img_meta_dict["num_bits"]=num_bits
            img_meta_dict["colorspace"]=colorspace
            img_meta_dict["alt_colorspace"]=alt_colorspace
            img_meta_dict["sym_name"]=sym_name
            img_meta_dict["filter"]=img_filter
            img_meta_dict["referencer"]=img_ref
            
            
            
            
            
            pix = pymupdf.Pixmap(doc, xref) # create a Pixmap
            
            #pix = pymupdf.Pixmap(doc.extract_image(xref)["image"])
            #mask = pymupdf.Pixmap(doc.extract_image(smask)["image"])
            #pix = pymupdf.Pixmap(pix1, mask)
            
            #pix.set_alpha(premultiply=False)
            
            ### Commented Out Section for showing images#############################

            if pix.n - pix.alpha > 3: # CMYK: convert to RGB first
                pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
            # %matplotlib inline
            #pix = item.get_pixmap(dpi=DPI)
            
            print("PIX BUFFER SIZE")
            print(len(pix.samples_mv))
            
            
            image_size=(pix.h*pix.w*3)
            print('Original IMG_BUFFER_SIZE')
            print(image_size)
            
            print('Page Image Buffer Size')
            print(pix.samples_mv)
            
            #pix.size()=image_size
            
            try:
                img = np.ndarray([pix.h, pix.w, 3], dtype=np.uint8, buffer=pix.samples_mv)
            except:
                print('Image too large for Picture')
            finally:
                #img = np.ndarray([pix.h, pix.w, 3], dtype=np.uint8, buffer=pix.samples_mv)
                continue
            
            #plt.figure(dpi=DPI)  # set the figure's DPI
            #plt.title(title)  # set title of image
            #_ = plt.imshow(img, extent=(0, pix.w * 18 / DPI, pix.h * 18 / DPI, 0))
            
            #############################################################################
            
            #print('Image:')
            #print(type(img))
            
            #Encode the Image into Base64

            #img_enc = base64.b64encode(img)
            
            #For Decoding use the following statement 
            
            #decoded_image = base64.decodestring(img_enc)
            
            img_meta_dict["img_matrix"]=img
            
            npy_img_lst.append(img_meta_dict)
            
            #pix.save("page_%s-image_%s.png" % (page_index, image_index)) # save the image as png
            #pix = None
            
    
    ###########################################################
    
    page_image_dict['page']=page_number
    #page_image_dict['img_lst']=image_list
    page_image_dict['img_cnt']=len(image_list)
    page_image_dict['img_npy_lst']=npy_img_lst
    
    
    #download_images_per_page(doc,doc_name,page,page_index,DPI)
    
    return page_image_dict


def extract_text_tables_images_per_page(doc,doc_name,doc_img,index):
    print("IN extract_text_tables_images_per_page")
    page_dict={}
    page_image_dict={}
    tab_df_lst=[]
    page = doc[index]
    tabs = page.find_tables()  # detect the tables
    
    ##Extract Images From Pages############
    
    page_image_dict=extract_images_per_page(doc_img,doc_name,index)
    
    print("page_image_dict")
    print(page_image_dict)
    
    
    page_dict['page']=page_image_dict['page']
    #page_dict['img_lst']=page_image_dict['img_lst']

    page_dict['img_cnt']=page_image_dict['img_cnt']
    page_dict['img_npy_lst']=page_image_dict['img_npy_lst']
    
    #######################################
    
    ############################Extract Text#######################################################
    #Extract Text From each page.
    #Commented out for experiment
    #text = page.get_text()
    
    #Trying to get the page structure along with text from each page.############
    #So that we can get more page metadata to add more context to the page############
    text = page.get_text("html")
    
    page_dict['text']=text
    
    print(text)
    ###############################################################################################
    
    #for i,tab in enumerate(tabs):  # iterate over all tables
    #    for cell in tab.header.cells:
    #       page.draw_rect(cell,color=fitz.pdfcolor["red"],width=0.3)
    #    page.draw_rect(tab.bbox,color=fitz.pdfcolor["green"])
    #    print(f"Table {i} column names: {tab.header.names}, external: {tab.header.external}")
    
    #show_image(page, f"Table & Header BBoxes")
   
    # choose the second table for conversion to a DataFrame
    #tab = tabs[0]
    #print(tabs)
    
    if tabs.tables == []:
        print('Do Nothing')
    else:
        for tab in tabs:
            df=pd.DataFrame()
            df = tab.to_pandas()
            tab_df_lst.append(df)
    
    page_dict['tables']=tab_df_lst
    
    
    
    
    #print(tab_df_lst)
    #df = tab.to_pandas()
    # show the DataFrame
    return page_dict

#from numpyencoder import NumpyEncoder
import pickle
import shutil

def extract_text_images_tables(doc_path):
    
    doc_per_page_tabs_lst=[]
    doc = fitz.open(doc_path)
    
    num_pages=len(doc)
    
    doc_img = pymupdf.open(doc_path)
    
    doc_name=doc_path.split('/')[-1]
    
    doc_type=doc_path.split('.')[-1]
    
    doc_name_wo_type=doc_path.split('/')[-1].split('.')[0]
    
    print(doc_name_wo_type)
    
    isExist = os.path.exists('./Parsed_PDF_Output/'+doc_name_wo_type)
    
    if isExist:
        shutil.rmtree('./Parsed_PDF_Output/'+doc_name_wo_type)
        
    os.mkdir('./Parsed_PDF_Output/'+doc_name_wo_type)
    
    for i in range(1,num_pages):
        #page_image_dict={}
        
        os.mkdir('./Parsed_PDF_Output/'+doc_name_wo_type+'/page_'+str(i+1))
        
        tab_df_lst=extract_text_tables_images_per_page(doc,doc_name_wo_type,doc_img,i)
        
        
        
        if len(tab_df_lst) == 0:
            print("Do Nothing Here")
        else: 
            doc_per_page_tabs_lst.append(tab_df_lst)
        
    
    
    document_dictionary={"name":doc_name,"type":doc_type, "data": doc_per_page_tabs_lst}

    
        #Save the List of MetaData to pickle in disk.
    with open("./parsed_pdf_output_pickle/"+doc_name+'.pickle', 'wb') as f:
        pickle.dump(document_dictionary, f)
    
    return document_dictionary