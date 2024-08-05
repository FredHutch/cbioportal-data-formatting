package org.cbio.gdcpipeline.tasklet;

import java.io.File;
import java.util.LinkedHashMap;
import java.util.Map;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
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
public class CnaMetaDataTasklet implements Tasklet {
    @Value("${cna.data.file}")
    private String CNA_DATA_FILE;

    @Value("${cna.metadata.file}")
    private String CNA_METADATA_FILE;

    @Value("#{jobParameters[cancer_study_id]}")
    private String cancer_study_id;

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;
    
    private static Log LOG = LogFactory.getLog(CnaMetaDataTasklet.class);
    
    @Override
    public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) throws Exception {
        String metafile = outputDir + File.separator + CNA_METADATA_FILE;
        Map<String, String> cnaMetaData = new LinkedHashMap<>();
        
        cnaMetaData.put("cancer_study_identifier", cancer_study_id);
        cnaMetaData.put("genetic_alteration_type", "COPY_NUMBER_ALTERATION");
        cnaMetaData.put("datatype", "DISCRETE");
        cnaMetaData.put("stable_id", "cna");
        cnaMetaData.put("show_profile_in_analysis_tab", "true");
        cnaMetaData.put("profile_name", "Putative copy-number alterations");
        cnaMetaData.put("profile_description", "Putative copy-number. -2 = " + 
                "homozygous deletion; -1 = hemizygous deletion; 0 = neutral" + 
                " / no change; 1 = gain; 2 = high level amplification.");
        cnaMetaData.put("data_filename" , CNA_DATA_FILE);        
        
        MetaFileWriter.writeMetadata(cnaMetaData, metafile);
        
        return RepeatStatus.FINISHED;
    }
    
}
