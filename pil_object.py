import pydicom as pyd
from PIL import Image
from PIL.ImageQt import ImageQt
import numpy as np


from pydicom.dataset import Dataset

from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove, VerificationSOPClass

def dicom_to_qt(dcm_file):
    image = np.array(pyd.dcmread(dcm_file).pixel_array)
    image = Image.fromarray(image)
    image.mode = 'I'
    image = image.point(lambda i:i*(1./256)).convert('L')
    qim = ImageQt(image)
    return (qim)






