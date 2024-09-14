package org.cbio.gdcpipeline.reader;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.cbio.ClinicalDataModel;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.ItemStreamReader;
import org.springframework.beans.factory.annotation.Value;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.HashMap;
import org.cbio.gdcpipeline.util.GraphQLQueryUtil;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.util.regex.*;
import org.cbio.gdcpipeline.model.GDCCase;
import org.cbio.gdcpipeline.model.cbio.Patient;
import org.cbio.gdcpipeline.model.cbio.Sample;

/**
 * @author Dixit Patel
 */
public class ClinicalReader implements ItemStreamReader<ClinicalDataModel> {
    private static Log LOG = LogFactory.getLog(ClinicalReader.class);

    @Value("${gdc.graphql.endpoint}")
    private String graphqlEndpoint;

    @Value("#{jobExecutionContext[caseIds]}")
    private List<String> caseIds;

    @Value("#{jobParameters[filter_normal_sample]}")
    private String filterNormalSampleFlag;

    private List<ClinicalDataModel> clinicalDataModelList = new ArrayList<>();
    private JSONObject gdcResponse = new JSONObject();
    private String GDC_FILTER_DATATYPE = "cases";
    private String GDC_FILTER_FIELD = "case_id";
    Map<String, String> gdcIdToSampleId = new HashMap<>();
    Map<String, String> gdcAliquotIdToSampleId = new HashMap<>();
    Map<String, String> gdcUUIDToSampleId = new HashMap<>();


    public static final Pattern TCGA_SAMPLE_BARCODE_REGEX =
        Pattern.compile("^(TCGA-\\w\\w-\\w\\w\\w\\w-\\d\\d).*$");

    @Override
    public ClinicalDataModel read() throws Exception {
        if (!this.clinicalDataModelList.isEmpty()) {
            return clinicalDataModelList.remove(0);
        }
        return null;
    }

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        String query = "query CASES($filters: FiltersArgument) { viewer {repository " +
                "{cases {hits(filters: $filters, first: " + Integer.toString(caseIds.size()) +
                ") {edges {node {sample_ids,submitter_id,submitter_analyte_ids," +
                "case_id,disease_type,primary_site,demographic {gender,year_of_birth," +
                "demographic_id,race,ethnicity,year_of_death,days_to_birth," +
                "days_to_death,vital_status,id},diagnoses {hits {edges {node " +
                "{tumor_grade,tumor_stage,days_to_last_follow_up,year_of_diagnosis}}}}," +
                "samples {hits {edges {node {sample_id,sample_type_id,sample_type," +
                "submitter_id, portions {hits {edges {node {analytes {hits {edges {node " +
                "{aliquots {hits {edges {node {aliquot_id}}}}}}}}}}}}}}}}}}}}}}}";
        try {
            gdcResponse = GraphQLQueryUtil.query(graphqlEndpoint, query, GDC_FILTER_DATATYPE, GDC_FILTER_FIELD, caseIds);
        }
        catch (IOException e) {
            LOG.error("Failed to query graphql for cases!");
        }
        LOG.info("Finished graphql for cases.");

        processCasesResponse();
        executionContext.put("gdcIdToSampleId", gdcIdToSampleId);
        executionContext.put("gdcAliquotIdToSampleId", gdcAliquotIdToSampleId);
        executionContext.put("gdcUUIDToSampleId", gdcUUIDToSampleId);
    }

    @Override
    public void update(ExecutionContext executionContext) throws ItemStreamException {
    }

    @Override
    public void close() throws ItemStreamException {
    }

    private void processCasesResponse() {
        JSONArray cases = GraphQLQueryUtil.getQueryList(gdcResponse, "cases");
        for (Object caseObject : cases) {
            GDCCase gdcCase = new GDCCase((JSONObject) caseObject, filterNormalSampleFlag);
            clinicalDataModelList.add(new Sample(gdcCase));
            clinicalDataModelList.add(new Patient(gdcCase));
            for (String aliquotId : gdcCase.getAliquotIds()) {
                gdcAliquotIdToSampleId.put(aliquotId.toUpperCase(), gdcCase.getSampleId().toUpperCase());
            }
            gdcIdToSampleId.put(gdcCase.getCaseId().toUpperCase(), gdcCase.getSampleId().toUpperCase());
            gdcUUIDToSampleId.put(gdcCase.getSampleUUID().toUpperCase(), gdcCase.getSampleId().toUpperCase());
        }
    }
}
