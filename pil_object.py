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




class GetPatient:
    def __init__(self,
                 patient_name=None,
                 patient_DOB=None,
                 study_date='20180802',
                 destination_folder='images/',

                 scp_port=11113):

        self.study_date = study_date
        self.patient_name = patient_name
        self.scp_port = scp_port
        self.destination_folder = destination_folder

    def check_SCP(self):
        ae = AE()

        # Add a requested presentation context
        ae.add_requested_context(VerificationSOPClass)

        # Associate with peer AE at IP 127.0.0.1 and port 11112
        assoc = ae.associate('127.0.0.1', self.scp_port)

        if assoc.is_established:
            # Use the C-ECHO service to send the request
            # returns the response status a pydicom Dataset
            status = assoc.send_c_echo()

            # Check the status of the verification request
            if status:
                # If the verification request succeeded this will be 0x0000
                # print('C-ECHO request status: 0x{0:04x}'.format(status.Status))

                return status.Status == 0

            assoc.release()
        else:
            print('Association rejected, aborted or never connected')
            return False

    '''    
    def run_SCP(self):
        print('starting STORESCP!')
        comand_string = 'python -m pynetdicom storescp ' + str(self.scp_port) + '-d -od ' + self.destination_folder

        os.system(comand_string)

    '''

    def c_move_params(self):
        ae = AE()

        # Add a requested presentation context
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

        # Create out identifier (query) dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = 'PATIENT'
        # Unique key for PATIENT level
        ds.PatientID = '4508'
        # ds.StudyDate = self.study_date
        # Unique key for STUDY level
        # Unique key for SERIES level
        # ds.SeriesInstanceUID = '1.2.3.4'

        # Associate with peer AE at IP 127.0.0.1 and port 11112
        assoc = ae.associate('127.0.0.1', 4242, ae_title=b'ORTHANC')

        if assoc.is_established:
            # Use the C-MOVE service to send the identifier
            responses = assoc.send_c_move(ds, 'STORESCP', PatientRootQueryRetrieveInformationModelMove)
            for (status, identifier) in responses:
                if status:
                    print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                else:
                    print('Connection timed out, was aborted or received invalid response')

            # Release the association
            assoc.release()
        else:
            print('Association rejected, aborted or never connected')

    def get_patient(self):

        if self.check_SCP():
            self.c_move_params()

        else:

            print("RUN STORESCP!")
            #### python -m pynetdicom storescp 11113 -d -od storescp


