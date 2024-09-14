package org.cbio.gdcpipeline.tasklet;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.lang.StringUtils;
import org.cbio.gdcpipeline.util.MetaFileWriter;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.beans.factory.annotation.Value;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 *@author Dixit Patel
 */
public class MutationMetadataTasklet implements Tasklet {
    @Value("#{jobExecutionContext[mutation_data_filenames]}")
    private List<String> MUTATION_DATA_FILES;

    @Value("${mutation.metadata.file}")
    private String MUTATION_METADATA_FILE;

    @Value("#{jobParameters[cancer_study_id]}")
    private String cancer_study_id;

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    private static Log LOG = LogFactory.getLog(MutationMetadataTasklet.class);

    @Override
    public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) throws Exception {
        String metafile = outputDir + File.separator + MUTATION_METADATA_FILE;
        Map<String, String> mutationMetadata = new LinkedHashMap<>();

        mutationMetadata.put("cancer_study_identifier",cancer_study_id);
        mutationMetadata.put("genetic_alteration_type","MUTATION_EXTENDED");
        mutationMetadata.put("datatype","MAF");
        mutationMetadata.put("stable_id","mutations");
        mutationMetadata.put("show_profile_in_analysis_tab","true");
        mutationMetadata.put("profile_description","Mutation data from whole exome sequencing");
        mutationMetadata.put("profile_name","Mutations");
        mutationMetadata.put("data_filename", StringUtils.join(MUTATION_DATA_FILES,','));

        MetaFileWriter.writeMetadata(mutationMetadata, metafile);
        return RepeatStatus.FINISHED;
    }
}
