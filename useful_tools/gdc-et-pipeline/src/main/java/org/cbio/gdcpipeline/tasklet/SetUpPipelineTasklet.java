package org.cbio.gdcpipeline.tasklet;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.beans.factory.annotation.Value;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.HashSet;

/**
 * @author Dixit Patel
 */
public class SetUpPipelineTasklet implements Tasklet {
    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    @Value("#{jobParameters[sourceDirectory]}")
    private String sourceDir;

    @Value("#{jobParameters[cancer_study_id]}")
    private String cancer_study_id; 
    
    private static Log LOG = LogFactory.getLog(SetUpPipelineTasklet.class);

    @Override
    public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) throws Exception {
        createOutputDirectory();
        validateSourceDirectory();
        if (LOG.isInfoEnabled()) {
            LOG.info(" ######### Pipeline Setup Completed #########");
        }
        return RepeatStatus.FINISHED;
    }

    private void validateSourceDirectory() throws FileNotFoundException {
        File source = new File(sourceDir);
        if (!source.exists()) {
            if (LOG.isErrorEnabled()) {
                LOG.error(" Invalid Source directory ");
            }
            throw new FileNotFoundException();
        }
    }

    private void createOutputDirectory() throws FileNotFoundException {
        File outputDirectory = new File(outputDir);
        if (outputDirectory.mkdir()) {
            if (LOG.isInfoEnabled()) {
                LOG.info(" Output will be at " + outputDir);
            }
        } else if (!outputDirectory.exists()) {
            if (LOG.isErrorEnabled()) {
                LOG.error(" Invalid output directory ");
            }
            throw new FileNotFoundException();
        } else {
            if (LOG.isInfoEnabled()) {
                LOG.info(" Output directory is valid ");
            }
        }
    }
}
