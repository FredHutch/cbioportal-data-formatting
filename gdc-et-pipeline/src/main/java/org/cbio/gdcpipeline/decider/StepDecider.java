package org.cbio.gdcpipeline.decider;

import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.StepExecution;
import org.springframework.batch.core.job.flow.FlowExecutionStatus;
import org.springframework.batch.core.job.flow.JobExecutionDecider;

/**
 * @author Dixit Patel
 */
public class StepDecider implements JobExecutionDecider {
    public enum STEP {
        ALL, CLINICAL, MUTATION, CNA, EXPRESSION
    }

    @Override
    public FlowExecutionStatus decide(JobExecution jobExecution, StepExecution stepExecution) {
        String stepToRun = jobExecution.getJobParameters().getString("datatypes");
        if (stepToRun.contains(STEP.CLINICAL.toString())) {
            return new FlowExecutionStatus(STEP.CLINICAL.toString());
        }
        if (stepToRun.contains(STEP.MUTATION.toString())) {
            return new FlowExecutionStatus(STEP.MUTATION.toString());
        }
        if (stepToRun.contains(STEP.CNA.toString())) {
            return new FlowExecutionStatus(STEP.CNA.toString());
        }
        if (stepToRun.contains(STEP.EXPRESSION.toString())) {
            return new FlowExecutionStatus(STEP.EXPRESSION.toString());
        }
        return new FlowExecutionStatus(STEP.ALL.toString());
    }
}
