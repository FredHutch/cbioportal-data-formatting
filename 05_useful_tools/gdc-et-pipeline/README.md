
GDC ET Pipeline is a spring-batch based tool that transforms cancer genomic data, available from NCI's GDC repository, into appropriate file formats that can be loaded into cBioPortal tool. 

Slides discussing this pipline can be found [here (2017)](https://drive.google.com/open?id=0BxMXiAE6vrzjQ0tzQk93Nk5MSDA) and [here (2019)](https://drive.google.com/open?id=1x99OQp9IIniSfEB5qC9lVWWtfw7ZHheW).

The pipeline currently requires that the data being transformed is available on the filesystem. To download data, use the GDC Portal to generate a manifest file containing all of the files desired, then use the GDC Data Transfer Tool to download the files.

GDC Portal: https://portal.gdc.cancer.gov/

GDC Data Transfer Tool: https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Getting_Started/

Downloading data with the data transfer tool can be done on the command line as follows:

`gdc-client download -m <MANIFEST_FILE.txt>`

<h3>GDC ET Pipeline</h3>
The pipeline expects a manifest file in order to know the data files it must process. More details on manifest file can be found on [GDC Data portal](https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Preparing_for_Data_Download_and_Upload/). The batch expects the actual data files to be downloaded by the user from the GDC repository. 

There are several datatypes that are hosted at GDC. The pipeline currently supports processing of **Clinical**, **Mutation**, **CNA**, and **Expression** data files for conversion into cBioPortal ready to import files. More details about these types of files can be found in the [cBioPortal documentation](https://github.com/cBioPortal/cbioportal/blob/master/docs/File-Formats.md).

<h4>Brief overview of Steps : </h4>
The batch runs in several steps each accomplishing a different task. Current implementation stage of each step is mentioned which can be further extended upon.

<h4>Running the pipeline</h4>
The batch has some required options as well as optional parameters that user can provide. 

    $JAVA_HOME org.cbio.gdcpipeline.GDCPipelineApplication -<option>
    List of options : 
    -c,--cancer_study_id <arg>             [REQUIRED]  Cancer Study Id 
    -o,--output <arg>                      [REQUIRED]  output directory for files
    -s,--source <arg>                      [REQUIRED]  source directory for files
    -d,--datatypes <arg>                   [OPTIONAL]  Datatypes to run. Default is All
    -f,--filter_normal_sample <arg>        [OPTIONAL]  True or False. Flag to filter
                                                       normal samples. Default is True

    -i,--isoformOverrideSource <arg>       [OPTIONAL]  Isoform Override Source. Default
                                                       is 'uniprot'
    -m,--manifest_file <arg>               [OPTIONAL]  Manifest file path

    -separate_mafs,--separate_mafs <arg>   [OPTIONAL]  True or False. Process MAF files
                                                       individually or merge together.
                                                       Default is False
    -h,--help                                          shows this help document and
                                                       quits.                                          

After the data has been downloaded using the GDC Data Download tool described above, you can call the pipeline like so:

`$JAVA_HOME/bin/java -jar target/gdcpipeline-0.0.1-SNAPSHOT.jar -c <CANCER_STUDY_NAME> -m <MANIFEST_FILE> -o <OUTPUT_DESTINATION> -s <DOWNLOADED_RAW_FILES_LOCATION>`

