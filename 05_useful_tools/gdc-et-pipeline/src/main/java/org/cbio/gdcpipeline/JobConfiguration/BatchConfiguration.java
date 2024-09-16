package org.cbio.gdcpipeline.JobConfiguration;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.decider.StepDecider;
import org.cbio.gdcpipeline.tasklet.ProcessManifestFileTasklet;
import org.cbio.gdcpipeline.tasklet.SetUpPipelineTasklet;
import org.springframework.batch.core.Job;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.batch.core.job.builder.FlowBuilder;
import org.springframework.batch.core.job.flow.Flow;
import org.springframework.batch.core.job.flow.JobExecutionDecider;
import org.springframework.batch.core.listener.ExecutionContextPromotionListener;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;

import javax.annotation.Resource;
import org.cbio.gdcpipeline.util.GenomeNexusCache;

/**
 * @author Dixit Patel
 */
@EnableBatchProcessing
@Configuration
@ComponentScan(basePackages="org.cbioportal.annotator")
public class BatchConfiguration {
    private static Log LOG = LogFactory.getLog(BatchConfiguration.class);
    @Autowired
    JobBuilderFactory jobBuilderFactory;

    @Autowired
    StepBuilderFactory stepBuilderFactory;

    @Resource(name = "clinicalDataStep")
    Step clinicalDataStep;

    @Resource(name = "clinicalMetaDataStep")
    Step clinicalMetaDataStep;

    @Resource(name = "mutationDataStep")
    Step mutationDataStep;

    @Resource(name = "mutationMetaDataStep")
    Step mutationMetaDataStep;

    @Resource(name = "cnaDataStep")
    Step cnaDataStep;

    @Resource(name = "cnaMetaDataStep")
    Step cnaMetaDataStep;

    @Resource(name = "expressionDataStep")
    Step expressionDataStep;
    
    @Resource(name = "expressionMetaDataStep")
    Step expressionMetaDataStep;

    @Value("${chunk.interval}")
    private int chunkInterval;

    @Bean
    public Step setUpPipeline() {
        return stepBuilderFactory.get("setUpPipeline")
                .tasklet(setUpPipelineTasklet())
                .build();
    }

    @Bean
    public GenomeNexusCache genomeNexusCache() {
        return new GenomeNexusCache();
    }

    @Bean
    public ExecutionContextPromotionListener processManifestFileListener() {
        String[] keys = new String[]{"gdcManifestData", "caseIds"};
        ExecutionContextPromotionListener executionContextPromotionListener = new ExecutionContextPromotionListener();
        executionContextPromotionListener.setKeys(keys);
        return executionContextPromotionListener;

    }

    @Bean
    public Step processManifestFile() {
        return stepBuilderFactory.get("processManifestFile")
                .listener(processManifestFileListener())
                .tasklet(processManifestFileTasklet())
                .build();
    }

    @Bean
    @StepScope
    public Tasklet processManifestFileTasklet() {
        return new ProcessManifestFileTasklet();
    }

    @Bean
    @StepScope
    public Tasklet setUpPipelineTasklet() {
        return new SetUpPipelineTasklet();
    }

    @Bean
    public Flow clinicalDataFlow() {
        return new FlowBuilder<Flow>("clinicalDataFlow")
                .start(clinicalDataStep)
                .next(clinicalMetaDataStep)
                .build();
    }

    @Bean
    public Flow mutationDataFlow() {
        return new FlowBuilder<Flow>("mutationDataFlow")
                .start(mutationDataStep)
                .from(mutationDataStep).on("CONTINUE").to(mutationDataStep)
                .next(mutationMetaDataStep)
                .build();
    }

    @Bean
    public Flow cnaDataFlow() {
        return new FlowBuilder<Flow>("cnaDataFlow")
                .start(cnaDataStep)
                .next(cnaMetaDataStep)
                .build();
    }

    @Bean
    public Flow expressionDataFlow() {
        return new FlowBuilder<Flow>("expressionDataFlow")
                .start(expressionDataStep)
                .next(expressionMetaDataStep)
                .build();
    }

    @Bean
    public Flow gdcAllDatatypesFlow() {
        return new FlowBuilder<Flow>("gdcAllDatatypesFlow")
                .start(clinicalDataFlow())
                .next(mutationDataFlow())
                .next(cnaDataFlow())
                .next(expressionDataFlow())
                .build();
    }

    @Bean
    public Flow configurePipelineFlow() {
        return new FlowBuilder<Flow>("configurePipelineFlow")
                .start(setUpPipeline())
                .next(processManifestFile())
                .build();
    }

    public Flow stepDeciderFlow() {
        return new FlowBuilder<Flow>("stepDeciderFlow")
                .start(stepDecider())
                .on(StepDecider.STEP.ALL.toString()).to(gdcAllDatatypesFlow())
                .from(stepDecider()).on(StepDecider.STEP.CLINICAL.toString()).to(clinicalDataFlow())
                .from(stepDecider()).on(StepDecider.STEP.MUTATION.toString()).to(mutationDataFlow())
                .from(stepDecider()).on(StepDecider.STEP.CNA.toString()).to(cnaDataFlow())
                .from(stepDecider()).on(StepDecider.STEP.EXPRESSION.toString()).to(expressionDataFlow())
                .build();
    }

    @Bean
    public JobExecutionDecider stepDecider() {
        return new StepDecider();
    }

    // Flow of All Steps
    @Bean
    public Job gdcJob() {
        return jobBuilderFactory.get("gdcJob")
                .start(configurePipelineFlow())
                .next(stepDeciderFlow())
                .end()
                .build();
    }
}
