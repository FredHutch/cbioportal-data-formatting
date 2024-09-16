package org.cbio.gdcpipeline.listener;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.util.CommonDataUtil;
import org.springframework.batch.core.ExitStatus;
import org.springframework.batch.core.StepExecution;
import org.springframework.batch.core.StepExecutionListener;
import org.springframework.beans.factory.annotation.Value;

import java.io.File;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.List;
import org.cbio.gdcpipeline.model.ManifestFileData;

/**
 * @author Dixit Patel
 **/
public class MutationStepListener implements StepExecutionListener {
    private static Log LOG = LogFactory.getLog(MutationStepListener.class);

    @Value("${mutation.data.file.prefix}")
    private String MUTATION_DATA_FILE_PREFIX;

    @Value("${mutation.default.merged.maf.file}")
    private String MUTATION_DEFAULT_MERGED_MAF_FILE;

    @Value("#{jobParameters[sourceDirectory]}")
    private String sourceDir;

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    @Value("#{jobExecutionContext[gdcManifestData]}")
    private List<ManifestFileData> gdcManifestData;

    @Value("#{jobParameters[separate_mafs]}")
    private String separate_mafs;

    @Override
    public void beforeStep(StepExecution stepExecution) {
        List<File> maf_files ;
        if (stepExecution.getJobExecution().getExecutionContext().containsKey("maf_files")) {
            maf_files = (List<File>)stepExecution.getJobExecution().getExecutionContext().get("maf_files");
        }
        else {
            maf_files = getMutationFileList();
        }
        if (!maf_files.isEmpty()) {
            if (!separate_mafs.isEmpty()) {
                if (separate_mafs.equalsIgnoreCase("true")) {
                    //used by metadata step
                    List<String> maf_filenames = new ArrayList<>();
                    for(File file : maf_files){
                        maf_filenames.add(MUTATION_DATA_FILE_PREFIX+file.getName());
                    }
                    stepExecution.getJobExecution().getExecutionContext().put("mutation_data_filenames", maf_filenames);
                    //read individually
                    List<File> mafToProcess = new ArrayList<>();
                    mafToProcess.add(maf_files.remove(0));
                    stepExecution.getJobExecution().getExecutionContext().put("maf_files", maf_files);
                    stepExecution.getExecutionContext().put("mafToProcess", mafToProcess);
                } else {
                    //Read all MAF's together
                    List<String> mutation_data_filenames = new ArrayList<>();
                    mutation_data_filenames.add(MUTATION_DEFAULT_MERGED_MAF_FILE);
                    stepExecution.getJobExecution().getExecutionContext().put("mutation_data_filenames",mutation_data_filenames );
                    stepExecution.getExecutionContext().put("mafToProcess", maf_files);
                }
            }
        }
    }

    @Override
    public ExitStatus afterStep(StepExecution stepExecution) {
        if (!separate_mafs.isEmpty()) {
            if (separate_mafs.equalsIgnoreCase("true")) {
                List<String> mafList = (List<String>) stepExecution.getJobExecution().getExecutionContext().get("maf_files");
                if (!mafList.isEmpty()) {
                    return new ExitStatus("CONTINUE");
                }
            }
            //delete temp directory
            CommonDataUtil.deleteTempDir();
        }
        return ExitStatus.COMPLETED;
    }

    public List<File> getMutationFileList() {
        List<File> mutationFileList = new ArrayList<>();
        for (ManifestFileData dataFile : gdcManifestData) {
            if (CommonDataUtil.GDC_TYPE.MUTATION.toString().equals(dataFile.getNormalizedDatatype())) {
                Path path = Paths.get(sourceDir, dataFile.getId(), dataFile.getFilename());
                File file = path.toFile();
                mutationFileList.add(file);
            }
        }
        try {
            if (!mutationFileList.isEmpty()) {
                mutationFileList = CommonDataUtil.extractCompressedFiles(mutationFileList);
            }
            else {
                LOG.error("Mutation file list empty");
            }
        }
        catch (Exception e) {
            LOG.error("Could not extract maf files!");
        }
        return mutationFileList;
    }
}
