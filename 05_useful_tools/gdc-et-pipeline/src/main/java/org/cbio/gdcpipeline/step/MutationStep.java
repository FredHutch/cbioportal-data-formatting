package org.cbio.gdcpipeline.step;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.listener.MutationStepListener;
import org.cbio.gdcpipeline.processor.MutationProcessor;
import org.cbio.gdcpipeline.reader.MutationReader;
import org.cbio.gdcpipeline.tasklet.MutationMetadataTasklet;
import org.cbio.gdcpipeline.writer.MutationWriter;
import org.cbioportal.models.AnnotatedRecord;
import org.cbioportal.models.MutationRecord;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * @author Dixit Patel
 */

@EnableBatchProcessing
@Configuration
public class MutationStep {
    @Autowired
    StepBuilderFactory stepBuilderFactory;

    @Autowired
    JobBuilderFactory jobBuilderFactory;

    @Value("${chunk.interval}")
    private int chunkInterval;

    private static Log LOG = LogFactory.getLog(ClinicalStep.class);

    @Bean
    @StepScope
    public MutationReader mutationDataReader() {
        return new MutationReader();
    }

    @Bean
    @StepScope
    public MutationProcessor mutationDataProcessor() {
        return new MutationProcessor();
    }

    @Bean
    @StepScope
    public MutationWriter mutationDataWriter() {
        return new MutationWriter();
    }

    @Bean
    @StepScope
    public MutationStepListener mutationStepListener() {
        return new MutationStepListener();
    }

    @Bean
    public Step mutationDataStep() {
        return stepBuilderFactory.get("mutationDataStep")
                .listener(mutationStepListener())
                .<MutationRecord, AnnotatedRecord>chunk(chunkInterval)
                .reader(mutationDataReader())
                .processor(mutationDataProcessor())
                .writer(mutationDataWriter())
                .build();
    }

    @Bean
    @StepScope
    public Tasklet mutationMetaDataTasklet() {
        return new MutationMetadataTasklet();
    }

    @Bean
    public Step mutationMetaDataStep() {
        return stepBuilderFactory.get("mutationMetaDataStep")
                .tasklet(mutationMetaDataTasklet())
                .build();
    }
}
