import pydicom as pyd
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np

def dicom_to_qt(dcm_file):
    image = np.array(pyd.dcmread(dcm_file).pixel_array)
    image = Image.fromarray(image)
    image.mode = 'I'
    image = image.point(lambda i:i*(1./256)).convert('L')
    qim = ImageQt(image)
    return (qim)

