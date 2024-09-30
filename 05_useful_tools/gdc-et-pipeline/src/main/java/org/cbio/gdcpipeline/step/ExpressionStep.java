package org.cbio.gdcpipeline.step;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.cbio.gdcpipeline.reader.ExpressionReader;
import org.cbio.gdcpipeline.tasklet.ExpressionMetaDataTasklet;
import org.cbio.gdcpipeline.writer.ExpressionWriter;
import org.springframework.batch.core.step.tasklet.Tasklet;

/**
 * @author heinsz
 */
@EnableBatchProcessing
@Configuration
public class ExpressionStep {
    @Autowired
    StepBuilderFactory stepBuilderFactory;

    @Autowired
    JobBuilderFactory jobBuilderFactory;

    private static Log LOG = LogFactory.getLog(ClinicalStep.class);

    @Value("${chunk.interval}")
    private int chunkInterval;

    @Bean
    @StepScope
    public ExpressionReader expressionReader() {
        return new ExpressionReader();
    }

    @Bean
    @StepScope
    public ExpressionWriter expressionWriter() {
        return new ExpressionWriter();
    }

    @Bean
    public Step expressionDataStep() {
        return stepBuilderFactory.get("expressionDataStep")
                .<String, String>chunk(chunkInterval)
                .reader(expressionReader())
                .writer(expressionWriter())
                .build();
    }
    
    @Bean
    @StepScope
    public Tasklet expressionMetaDataTasklet() {
        return new ExpressionMetaDataTasklet();
    }
    
    @Bean
    public Step expressionMetaDataStep() {
        return stepBuilderFactory.get("expressionMetaDataStep")
                .tasklet(expressionMetaDataTasklet())
                .build();
    }
}
