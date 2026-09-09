import slicer



def load_extensions(extensions):
    manager = slicer.app.extensionsManagerModel()
    for extension in extensions:
        manager.downloadAndInstallExtensionByName(extension)


if __name__ == "__main__":
    extensions = [
        "AnatomyCarve",
        "ClassAnnotation",
        #"Chest_Imaging_Platform",
        "DCMQI",
        "DICOMwebBrowser",
        "ImageAugmenter",
        "MONAIAuto3DSeg",
        "MONAILabel",
        "MONAIViz",
        "NNUNet",
        "NNInteractive",
        "NvidiaAIAssistedAnnotation"
        "PETDICOMExtension",
        "PETTumorSegmentation",
        #"PyTorch",
        "QuantitativeReporting",
        "SegmentEditorExtraEffects",
        "SlicerConda",
        "SegmentationVerification",
        #"SkullStripper",
        #"SlicerDevelopmentToolbox",
        #"DatabaseInteractor",
        #"DebuggingTools",
        #"MarkupsToModel",
        #"MatlabBridge",
        #"SlicerBatchAnonymize",
        #"SlicerRT",
        #"SlicerRadiomics",
        #"TorchIO",
        #"LungCTAnalyzer",
        "TotalSegmentator",
        "SegmentWithSAM",
        "SlicerDcm2nii",
        "TCIABrowser",
        "XNATSlicer",
        "SlicerFreeSurfer",
    ]

    load_extensions(extensions)