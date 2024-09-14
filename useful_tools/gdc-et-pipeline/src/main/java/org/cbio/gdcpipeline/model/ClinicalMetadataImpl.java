package org.cbio.gdcpipeline.model;

import java.util.*;

/**
 * @author Dixit Patel
 */

// TODO: This class should be replaced with dynamic calls to the data dictionary api
// oncotree.mskcc.org/cdd/swagger-ui.html
public class ClinicalMetadataImpl implements MetadataManager {
    private Map<String, String> displayNames = new HashMap<>();
    private Map<String, String> description = new HashMap<>();
    private Map<String, String> datatype = new HashMap<>();
    private Map<String, String> priority = new HashMap<>();

    public ClinicalMetadataImpl() {
        setDisplayNames();
        setDescription();
        setDatatype();
        setPriority();
    }

    @Override
    public Map<String, List<String>> getFullHeader(List<String> header) {
        Map<String, List<String>> headers = new LinkedHashMap<>();
        List<String> displayNames = new ArrayList<>();
        List<String> description = new ArrayList<>();
        List<String> datatype = new ArrayList<>();
        List<String> priority = new ArrayList<>();

        for (String key : header) {
            key = key.toUpperCase();
            displayNames.add(this.displayNames.get(key));
            description.add(this.description.get(key));
            datatype.add(this.datatype.get(key));
            priority.add(this.priority.get(key));
        }
        headers.put("displayNames", displayNames);
        headers.put("description", description);
        headers.put("datatype", datatype);
        headers.put("priority", priority);
        headers.put("headers", header);
        return headers;
    }

    private void setDisplayNames() {
        this.displayNames.put("PATIENT_ID", "Patient Identifier");
        this.displayNames.put("SAMPLE_ID", "Sample Identifier");
        this.displayNames.put("ONCOTREE_CODE", "Onco Tree Code");
        this.displayNames.put("OS_STATUS", "Overall Survival Status");
        this.displayNames.put("OS_MONTHS", "Overall Survival (Months)");       
        this.displayNames.put("SEX", "Sex");
        this.displayNames.put("AGE", "Age");
        this.displayNames.put("GENDER", "Gender");
        this.displayNames.put("RACE", "Race");
        this.displayNames.put("ETHNICITY", "Ethnicity");
        this.displayNames.put("TUMOR_GRADE", "Tumor Grade");
        this.displayNames.put("SAMPLE_TYPE", "Sample Type");
        this.displayNames.put("PRIMARY_SITE", "Primary Tumor Site");
        this.displayNames.put("CANCER_TYPE", "Cancer Type");
        this.displayNames.put("TUMOR_STAGE", "Tumor Stage");
    }

    private void setDescription() {
        this.description.put("PATIENT_ID", "Patient_Identifier");
        this.description.put("SAMPLE_ID", "Sample Identifier");
        this.description.put("ONCOTREE_CODE", "Onco Tree Code");
        this.description.put("OS_STATUS", "Overall Survival Status");
        this.description.put("OS_MONTHS", "Overall Survival (Months)");
        this.description.put("SEX", "Sex");
        this.description.put("AGE", "Age");
        this.description.put("GENDER", "Gender");
        this.description.put("RACE", "Race");
        this.description.put("ETHNICITY", "Ethnicity");
        this.description.put("TUMOR_GRADE", "Tumor Grade");
        this.description.put("SAMPLE_TYPE", "The type of sample (i.e., normal, primary, met, recurrence).");
        this.description.put("PRIMARY_SITE", "Text term to describe the organ sub-division in an individual with cancer.");
        this.description.put("CANCER_TYPE", "Cancer Type");
        this.description.put("TUMOR_STAGE", "Tumor Stage");
    }

    private void setDatatype() {
        this.datatype.put("PATIENT_ID", "STRING");
        this.datatype.put("SAMPLE_ID", "STRING");
        this.datatype.put("ONCOTREE_CODE", "STRING");
        this.datatype.put("OS_STATUS", "STRING");
        this.datatype.put("OS_MONTHS", "NUMBER");
        this.datatype.put("SEX", "STRING");
        this.datatype.put("AGE", "NUMBER");
        this.datatype.put("GENDER", "STRING");
        this.datatype.put("RACE", "STRING");
        this.datatype.put("ETHNICITY", "STRING");
        this.datatype.put("TUMOR_GRADE", "STRING");
        this.datatype.put("SAMPLE_TYPE", "STRING");
        this.datatype.put("PRIMARY_SITE", "STRING");
        this.datatype.put("CANCER_TYPE", "STRING");
        this.datatype.put("TUMOR_STAGE", "STRING");
    }

    private void setPriority() {
        this.priority.put("PATIENT_ID", "1");
        this.priority.put("SAMPLE_ID", "1");
        this.priority.put("ONCOTREE_CODE", "1");
        this.priority.put("OS_STATUS", "1");
        this.priority.put("OS_MONTHS", "1");
        this.priority.put("SEX", "1");
        this.priority.put("AGE", "1");
        this.priority.put("GENDER", "1");
        this.priority.put("RACE", "1");
        this.priority.put("ETHNICITY", "1");
        this.priority.put("TUMOR_GRADE", "1");
        this.priority.put("SAMPLE_TYPE", "9");
        this.priority.put("PRIMARY_SITE", "1");
        this.priority.put("CANCER_TYPE", "1");
        this.priority.put("TUMOR_STAGE", "1");
    }
}
