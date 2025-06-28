import os
import pydicom
import numpy as np
from src.model.mri_scan import MRIScan
import logging

class MRILoader:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def load_data(self, folder_path: str) -> MRIScan:
        """
        Load MRI data from a folder containing DICOM files.
        
        Args:
            folder_path: Path to the folder containing DICOM files
            
        Returns:
            MRIScan: Object containing the MRI data and metadata
            
        Raises:
            ValueError: If no valid DICOM files are found or if the data is invalid
            FileNotFoundError: If the folder doesn't exist
        """
        self.logger.info(f"Loading MRI data from folder: {folder_path}")
        
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")
            
        if not os.path.isdir(folder_path):
            raise ValueError(f"Path is not a directory: {folder_path}")
        
        # Get all files in the folder
        dicom_files = []
        for root, _, files in os.walk(folder_path):
            for file in files:
                try:
                    file_path = os.path.join(root, file)
                    self.logger.debug(f"Attempting to read: {file_path}")
                    # Try to read as DICOM
                    dcm = pydicom.dcmread(file_path)
                    # Check required attributes
                    required_attrs = ['EchoTime', 'SliceLocation', 'Rows', 'Columns', 'PixelSpacing', 'SliceThickness']
                    missing_attrs = [attr for attr in required_attrs if not hasattr(dcm, attr)]
                    if missing_attrs:
                        self.logger.warning(f"File {file_path} missing required attributes: {missing_attrs}")
                        continue
                    # If successful, add to list
                    dicom_files.append((file_path, dcm))
                    self.logger.debug(f"Successfully read DICOM file: {file_path}")
                except Exception as e:
                    self.logger.warning(f"Failed to read {file_path}: {str(e)}")
                    continue
        
        if not dicom_files:
            raise ValueError("No valid DICOM files found in the specified folder")
            
        self.logger.info(f"Found {len(dicom_files)} valid DICOM files")
            
        # Get unique echo times and sort them
        echo_times = sorted(set(dcm.EchoTime for _, dcm in dicom_files))
        self.logger.debug(f"Found echo times: {echo_times}")
        
        # Filter out echo time 0
        echo_times = [t for t in echo_times if t != 0]
        num_echoes = len(echo_times)
        
        if num_echoes == 0:
            raise ValueError("No valid echo times found (all were 0)")
            
        self.logger.info(f"Using {num_echoes} echo times: {echo_times}")
            
        # Get unique slice locations and sort them
        slice_locations = sorted(set(dcm.SliceLocation for _, dcm in dicom_files))
        num_slices = len(slice_locations)
        self.logger.info(f"Found {num_slices} slices")
        
        # Create mapping from echo time to index
        echo_to_index = {echo: idx for idx, echo in enumerate(echo_times)}
        
        # Create mapping from slice location to index
        slice_to_index = {loc: idx for idx, loc in enumerate(slice_locations)}
        
        # Get dimensions and metadata from first file
        first_dcm = dicom_files[0][1]
        num_rows = first_dcm.Rows
        num_columns = first_dcm.Columns
        pixel_spacing = tuple(float(x) for x in first_dcm.PixelSpacing)
        slice_thickness = float(first_dcm.SliceThickness)
        
        self.logger.info(f"Image dimensions: {num_rows}x{num_columns}")
        self.logger.info(f"Pixel spacing: {pixel_spacing} mm")
        self.logger.info(f"Slice thickness: {slice_thickness} mm")
        
        # Create 4D array (X, Y, Z, T)
        data = np.zeros((num_rows, num_columns, num_slices, num_echoes), dtype=np.float32)
        
        # Load all slices
        for file_path, dcm in dicom_files:
            try:
                echo_idx = echo_to_index[dcm.EchoTime]
                slice_idx = slice_to_index[dcm.SliceLocation]
                data[:, :, slice_idx, echo_idx] = dcm.pixel_array
                self.logger.debug(f"Loaded slice {slice_idx} echo {echo_idx} from {file_path}")
            except Exception as e:
                self.logger.error(f"Failed to load data from {file_path}: {str(e)}")
                continue
            
        # Verify data is complete
        if np.any(data == 0):
            self.logger.warning("Data contains zero values, some slices might be missing")
            
        return MRIScan(
            data=data,
            echo_times=np.array(echo_times),
            slice_locations=np.array(slice_locations),
            num_rows=num_rows,
            num_columns=num_columns,
            pixel_spacing=pixel_spacing,
            slice_thickness=slice_thickness
        ) 