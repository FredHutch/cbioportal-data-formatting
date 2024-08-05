package org.cbio.gdcpipeline.tasklet;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.ManifestFileData;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.batch.core.step.tasklet.Tasklet;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.file.FlatFileItemReader;
import org.springframework.batch.item.file.mapping.DefaultLineMapper;
import org.springframework.batch.item.file.mapping.FieldSetMapper;
import org.springframework.batch.item.file.transform.DelimitedLineTokenizer;
import org.springframework.batch.item.file.transform.FieldSet;
import org.springframework.batch.repeat.RepeatStatus;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import java.io.BufferedReader;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.cbio.gdcpipeline.util.GraphQLQueryUtil;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 * @author Dixit Patel
 */
public class ProcessManifestFileTasklet implements Tasklet {
    @Value("${gdc.graphql.endpoint}")
    private String graphqlEndpoint;

    @Value("#{jobParameters[manifest_file]}")
    private String manifestFile;

    private static Log LOG = LogFactory.getLog(ProcessManifestFileTasklet.class);
    private List<ManifestFileData> manifestFileList = new ArrayList<>();
    private List<String> filenames = new ArrayList<>();
    private Set<String> caseIds = new HashSet<>();
    private JSONObject gdcResponse = new JSONObject();
    private String GDC_FILTER_DATATYPE = "files";
    private String GDC_FILTER_FIELD = "file_name";

    @Override
    public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) throws Exception {
        FlatFileItemReader<ManifestFileData> reader = new FlatFileItemReader<>();
        DelimitedLineTokenizer tokenizer = new DelimitedLineTokenizer(DelimitedLineTokenizer.DELIMITER_TAB);
        try (BufferedReader buff = new BufferedReader(new FileReader(manifestFile))) {
            // header line
            String header = buff.readLine();
            tokenizer.setNames(header.split(DelimitedLineTokenizer.DELIMITER_TAB));
        }
        DefaultLineMapper<ManifestFileData> lineMapper = new DefaultLineMapper<>();
        lineMapper.setLineTokenizer(tokenizer);
        lineMapper.setFieldSetMapper(manifestFieldSetMapper());
        reader.setResource(new FileSystemResource(manifestFile));
        reader.setLineMapper(lineMapper);
        reader.setLinesToSkip(1);
        reader.open(new ExecutionContext());
        ManifestFileData record = null;
        try {
            while ((record = reader.read()) != null) {
                manifestFileList.add(record);
                filenames.add(record.getFilename());
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new ItemStreamException("Error reading manifest record : "+record.toString());
        }
        reader.close();

        String query = "query FILES_EDGES($filters: FiltersArgument) {viewer" + 
                "{repository {files {hits(filters: $filters, first:" + 
                Integer.toString(filenames.size()) +") {total, edges {node {id," + 
                " data_type, data_format, file_name, experimental_strategy, data_category, analysis {workflow_type}," + 
                " submitter_id, cases {hits {edges {node {submitter_id," + 
                " submitter_sample_ids, case_id}}}}}}}}}}}";
        gdcResponse = GraphQLQueryUtil.query(graphqlEndpoint, query, GDC_FILTER_DATATYPE, GDC_FILTER_FIELD, filenames);
        processFilesResponse();

        ExecutionContext ec = chunkContext.getStepContext().getStepExecution().getExecutionContext();
        ec.put("caseIds", caseIds);
        ec.put("gdcManifestData", manifestFileList);

        return RepeatStatus.FINISHED;
    }

    private FieldSetMapper<ManifestFileData> manifestFieldSetMapper() {
        return (FieldSetMapper<ManifestFileData>) (FieldSet fs) -> {
            ManifestFileData record = new ManifestFileData();
            for (String header : record.getHeader()) {
                try {
                    record.getClass().getMethod("set" + header, String.class).invoke(record, fs.readString(header.toLowerCase()));
                } catch (Exception e) {
                    if (LOG.isDebugEnabled()) {
                        LOG.error(" Error in setting record for :" + header);
                    }
                    e.printStackTrace();
                }
            }
            return record;
        };
    }
    
    /**
     * Parses the json response from GDC graphql endpoint.
     * Traverses the json to get the case_ids associated with all of the files
     * in the manifest.
     */
    private void processFilesResponse() {
        JSONArray files = GraphQLQueryUtil.getQueryList(gdcResponse, "files");

        // TODO: Move this json traversing to a util class
        for (Object edgeObject : files) {
             JSONObject edge = (JSONObject) edgeObject;
            // Get a list of all case ids from the manifest files
            JSONObject node = (JSONObject) edge.get("node");
            for (ManifestFileData manifestFileData : manifestFileList) {
                String filename = (String) node.get("file_name");
                if (manifestFileData.getFilename().equals(filename)) {
                    manifestFileData.setSubmitterId((String)node.get("submitter_id"));
                    manifestFileData.setSubmitterSampleIds((String)node.get("submitter_sample_ids"));
                    manifestFileData.setDatatype((String) node.get("data_type"));
                    manifestFileData.setDataCategory((String) node.get("data_category"));
                    JSONObject analysis = (JSONObject) node.get("analysis");
                    manifestFileData.setWorkflowType((String) analysis.get("workflow_type"));
                    JSONObject cases = (JSONObject) node.get("cases");
                    JSONObject caseHits = (JSONObject) cases.get("hits");
                    JSONArray caseEdges = (JSONArray) caseHits.get("edges");
                    for (Object caseEdgeObject : caseEdges) {
                        JSONObject caseEdge = (JSONObject) caseEdgeObject;
                        JSONObject caseNode = (JSONObject) caseEdge.get("node");
                        String caseId = (String) caseNode.get("case_id");
                        caseIds.add(caseId);
                        manifestFileData.addSampleId(caseId);
                    }                    
                }
            }
        }
    }


}
