package org.cbio.gdcpipeline.tasklet;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.Map;
import org.cbio.gdcpipeline.util.MetaFileWriter;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.beans.factory.annotation.Value;

/**
 *
 * @author heinsz
 */
public class ExpressionMetaDataTasklet implements Tasklet {
    @Value("${expression.data.file}")
    private String EXPRESSION_DATA_FILE;

    @Value("${expression.metadata.file}")
    private String EXPRESSION_METADATA_FILE;

    @Value("#{jobParameters[cancer_study_id]}")
    private String cancer_study_id;

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;
    
    @Override
    public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) throws Exception {
        String metafile = outputDir + File.separator + EXPRESSION_METADATA_FILE;
        Map<String, String> expressionMetadata = new LinkedHashMap<>();
        
        expressionMetadata.put("cancer_study_identifier", cancer_study_id);
        expressionMetadata.put("genetic_alteration_type", "MRNA_EXPRESSION");
        expressionMetadata.put("datatype", "CONTINUOUS");
        expressionMetadata.put("stable_id", "rna_seq_mrna");
        expressionMetadata.put("show_profile_in_analysis_tab", "false");
        expressionMetadata.put("profile_name", "mRNA Expression (microarray)");
        expressionMetadata.put("profile_description", "Expression levels");
        expressionMetadata.put("data_filename", EXPRESSION_DATA_FILE);        
        
        MetaFileWriter.writeMetadata(expressionMetadata, metafile);
        
        return RepeatStatus.FINISHED;
    }
    
}
