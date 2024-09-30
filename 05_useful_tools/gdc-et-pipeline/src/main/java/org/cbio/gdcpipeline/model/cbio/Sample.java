package org.cbio.gdcpipeline.model.cbio;

import org.cbio.gdcpipeline.model.ClinicalMetadataImpl;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.cbio.gdcpipeline.model.GDCCase;

/**
 * @author Dixit Patel
 */


/** TODO: The field names and getters/setters should be changed to camel case
 * at some point. This will require changing how the fields extractor in
 * the writer functions
 */
public class Sample extends ClinicalDataModel {
    private String patient_id;
    private String sample_id;
    private String sample_type;
    private String cancer_type;
    private String primary_site;
    private String tumor_stage;

    public Sample() {
    }

    public Sample(String patient_id, String sample_id, String sample_type, String cancer_type, String primary_site, String tumor_stage) {
        this.patient_id = patient_id;
        this.sample_id = sample_id;
        this.sample_type = sample_type;
        this.cancer_type = cancer_type;
        this.primary_site = primary_site;
        this.tumor_stage = tumor_stage;
    }

    public Sample(GDCCase gdcCase) {
        patient_id = gdcCase.getPatientId();
        sample_id = gdcCase.getSampleId();
        sample_type = gdcCase.getSampleType();
        cancer_type = gdcCase.getCancerType();
        primary_site = gdcCase.getPrimarySite();
        tumor_stage = gdcCase.getTumorStage();
    }

    @Override
    public List<String> getFields() {
        List<String> fields = new ArrayList<>();
        fields.add("Patient_id");
        fields.add("Sample_id");
        fields.add("Sample_type");
        fields.add("Cancer_type");
        fields.add("Primary_site");
        fields.add("Tumor_stage");

        return fields;
    }

    @Override
    public Map<String, List<String>> getHeaders() {
        ClinicalMetadataImpl headers = new ClinicalMetadataImpl();
        return (headers.getFullHeader(getFields()));
    }

    public String getPatient_id() {
        return patient_id;
    }

    public void setPatient_id(String patient_id) {
        this.patient_id = patient_id;
    }

    public String getSample_id() {
        return sample_id;
    }

    public void setSample_id(String sample_id) {
        this.sample_id = sample_id;
    }

    public String getSample_type() {
        return sample_type;
    }

    public void setSample_type(String sample_type) {
        this.sample_type = sample_type;
    }

    public String getCancer_type() {
        return cancer_type;
    }

    public void setCancer_type(String cancer_type) {
        this.cancer_type = cancer_type;
    }

    public String getPrimary_site() {
        return primary_site;
    }

    public void setPrimary_site(String primary_site) {
        this.primary_site = primary_site;
    }

    public String getTumor_stage() {
        return tumor_stage;
    }

    public void setTumor_stage(String tumor_stage) {
        this.tumor_stage = tumor_stage;
    }
}
