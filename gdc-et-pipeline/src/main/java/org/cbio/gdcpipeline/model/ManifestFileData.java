package org.cbio.gdcpipeline.model;

import java.util.ArrayList;
import java.util.List;

/**
 * @author Dixit Patel
 */
public class ManifestFileData {
    private String id;
    private String filename;
    private String md5;
    private String size;
    private String state;
    private String submitterId;
    private String submitterSampleIds;
    private String datatype;
    private String dataCategory;
    private String workflowType;
    private List<String> sampleIds = new ArrayList<>();

    public List<String> getHeader(){
        List<String> header = new ArrayList<>();
        header.add("Id");
        header.add("Filename");
        header.add("Md5");
        header.add("Size");
        header.add("State");
        return header;
    }
    public String getMd5() {
        return md5;
    }

    public void setMd5(String md5) {
        this.md5 = md5;
    }

    public String getSize() {
        return size;
    }

    public void setSize(String size) {
        this.size = size;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getFilename() {
        return filename;
    }

    public void setFilename(String filename) {
        this.filename = filename;
    }

    public String getSubmitterId() {
        return this.submitterId;
    }

    public void setSubmitterId(String submitterId) {
        this.submitterId = submitterId;
    }

    public String getSubmitterSampleIds() {
        return this.submitterSampleIds;
    }

    public void setSubmitterSampleIds(String submitterSampleIds) {
        this.submitterSampleIds = submitterSampleIds;
    }

    public String getDatatype() {
        return datatype;
    }

    public void setDatatype(String datatype) {
        this.datatype = datatype;
    }
    
    public String getNormalizedDatatype() {
        return this.getDatatype().toLowerCase().replace(" ", "_");
    }
    
    public String getDataCategory() {
        return dataCategory;
    }
    
    public void setDataCategory(String dataCategory) {
        this.dataCategory = dataCategory;
    }
    
    public String getWorkflowType() {
        return workflowType;
    }
    
    public void setWorkflowType(String workflowType) {
        this.workflowType = workflowType;
    }
    
    public List<String> getSampleIds() {
        return sampleIds;
    }
    
    public void setSampleIds(List<String> sampleIds) {
        this.sampleIds.clear();
        this.sampleIds.addAll(sampleIds);    
    }
    
    public void addSampleId(String sampleId) {
        sampleIds.add(sampleId);
    }
}
