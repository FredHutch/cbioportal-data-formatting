package org.cbio.gdcpipeline.step;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.cbio.ClinicalDataModel;
import org.cbio.gdcpipeline.reader.ClinicalReader;
import org.cbio.gdcpipeline.tasklet.ClinicalMetaDataTasklet;
import org.cbio.gdcpipeline.util.CommonDataUtil;
import org.cbio.gdcpipeline.writer.ClinicalWriter;
import org.springframework.batch.core.Step;
import org.springframework.batch.core.configuration.annotation.EnableBatchProcessing;
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepScope;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.item.ItemWriter;
import org.springframework.batch.item.support.CompositeItemWriter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.ArrayList;
import java.util.List;
import org.springframework.batch.core.listener.ExecutionContextPromotionListener;

/**
 * @author Dixit Patel
 */
@EnableBatchProcessing
@Configuration
public class ClinicalStep {
    @Autowired
    StepBuilderFactory stepBuilderFactory;

    @Autowired
    JobBuilderFactory jobBuilderFactory;

    private static Log LOG = LogFactory.getLog(ClinicalStep.class);

    @Value("${chunk.interval}")
    private int chunkInterval;

    @Bean
    @StepScope
    public ClinicalReader clinicalReader() {
        return new ClinicalReader();
    }

    @Bean
    public ExecutionContextPromotionListener clinicalDataListener() {
        String[] keys = new String[]{"sampleIds", "gdcIdToSampleId", "gdcAliquotIdToSampleId", "gdcUUIDToSampleId"};
        ExecutionContextPromotionListener executionContextPromotionListener = new ExecutionContextPromotionListener();
        executionContextPromotionListener.setKeys(keys);
        return executionContextPromotionListener;
    }

    public CompositeItemWriter<ClinicalDataModel> compositeItemWriter() {
        List<ItemWriter<? super ClinicalDataModel>> delegates = new ArrayList<>(2);
        delegates.add(clinicalPatientDataWriter());
        delegates.add(clinicalSampleDataWriter());
        CompositeItemWriter<ClinicalDataModel> compositeItemWriter = new CompositeItemWriter<>();
        compositeItemWriter.setDelegates(delegates);
        try {
            compositeItemWriter.afterPropertiesSet();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return compositeItemWriter;
    }

    @Bean
    @StepScope
    public ClinicalWriter clinicalPatientDataWriter() {
        return new ClinicalWriter(CommonDataUtil.CLINICAL_TYPE.PATIENT);
    }

    @Bean
    @StepScope
    public ClinicalWriter clinicalSampleDataWriter() {
        return new ClinicalWriter(CommonDataUtil.CLINICAL_TYPE.SAMPLE);
    }

    @Bean
    public Step clinicalDataStep() {
        return stepBuilderFactory.get("clinicalDataStep")
                .listener(clinicalDataListener())
                .<ClinicalDataModel, ClinicalDataModel>chunk(chunkInterval)
                .reader(clinicalReader())
                .writer(compositeItemWriter())
                .build();
    }

    @Bean
    @StepScope
    public Tasklet clinicalMetaDataTasklet() {
        return new ClinicalMetaDataTasklet();
    }

    @Bean
    public Step clinicalMetaDataStep() {
        return stepBuilderFactory.get("clinicalMetaDataStep")
                .tasklet(clinicalMetaDataTasklet())
                .build();
    }
}
