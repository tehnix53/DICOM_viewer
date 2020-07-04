from pydicom.dataset import Dataset

from pynetdicom import AE
from pynetdicom.sop_class import (PatientRootQueryRetrieveInformationModelMove,
                                  VerificationSOPClass,
                                  PatientRootQueryRetrieveInformationModelFind)



class GetPatient:
    def __init__(self,
                 patient_name='^',
                 patient_DOB=None,
                 study_date='20180802',
                 pacs_ip='127.0.0.1',
                 pacs_aet=b'ORTHANC',
                 pacs_port=4242,
                 scp_port=11113,
                 ):
        if patient_DOB:
            self.patient_DOB = patient_DOB
        else:
            self.patient_DOB = None

        if study_date:
            self.study_date = study_date
        else:
            self.study_date = None
        self.patient_name = patient_name
        self.scp_port = scp_port
        self.finded_patients = []
        self.pacs_ip = pacs_ip
        self.pacs_aet = pacs_aet
        self.pacs_port = pacs_port

    def find_patient_by_name(self):

        ae = AE()

        # Add a requested presentation context
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

        # Create our Identifier (query) dataset
        ds = Dataset()
        ds.PatientID = '*'
        ds.Modality = '*'
        ds.PatientName = '*' + self.patient_name + '*'
        if self.patient_DOB:
            ds.PatientBirthDate = self.patient_DOB

        if self.study_date:
            ds.StudyDate = self.study_date

        ds.QueryRetrieveLevel = 'PATIENT'

        assoc = ae.associate(self.pacs_ip, self.pacs_port, ae_title=self.pacs_aet)

        if assoc.is_established:
            for cx in assoc.accepted_contexts:
                print('Context: {}, SCP role: {}, SCU role: {}'.format(cx.abstract_syntax, cx.as_scp, cx.as_scu))
            print('Association Established')
            # Use the C-FIND service to send the identifier
            # A query_model value of 'P' means use the 'Patient Root Query Retrieve
            #     Information Model - Find' presentation context
            responses = assoc.send_c_find(ds, query_model='1.2.840.10008.5.1.4.1.2.1.1')

            for (status, identifier) in responses:
                print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
                self.finded_patients.append((status, identifier))
            # Release the association
            assoc.release()
            print('Association Released')
        else:
            print('Association rejected or aborted')

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

    def c_move_params(self, ds_from_c_find):
        ae = AE()

        # Add a requested presentation context
        ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

        # Create out identifier (query) dataset
        ds = Dataset()
        ds.QueryRetrieveLevel = 'PATIENT'
        # Unique key for PATIENT level
        ds.PatientID = ds_from_c_find.PatientID
        # ds.PatientName = 'TIMONOVA^LARISA^ALEKSANDROVNA' #ds_from_c_find.PatientName
        # ds.StudyDate = self.study_date
        # Unique key for STUDY level
        # Unique key for SERIES level
        # ds.SeriesInstanceUID = '1.2.3.4'

        # Associate with peer AE at IP 127.0.0.1 and port 11112
        assoc = ae.associate(self.pacs_ip, self.pacs_port, ae_title=self.pacs_aet)

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

    def get_patient(self, finded_patient):

        if self.check_SCP():
            self.c_move_params(finded_patient)

        else:

            print("RUN STORESCP!")
            #### python -m pynetdicom storescp 11113 -d -od storescp


if __name__ == '__main__':
    gp = GetPatient()
    gp.find_patient_by_name()
    gp.get_patient(gp.finded_patients[1][1])