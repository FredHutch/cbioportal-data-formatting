package org.cbio.gdcpipeline.model;

import java.util.List;
import java.util.ArrayList;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.cbio.gdcpipeline.util.CommonDataUtil;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

/**
 *
 * @author heinsz
 */
public class GDCCase {
    private String cancerType;
    private String primarySite;
    private String gender;
    private String race;
    private String ethnicity;
    private String osStatus;
    private String tumorGrade;
    private String tumorStage;
    private String sampleId;
    private String patientId;
    private String sampleType;
    private String sampleUUID;
    private String caseId;
    private String sampleTypeId;
    private List<String> aliquotIds = new ArrayList<>();
    private double yearOfBirth;
    private double daysToDeath;
    private double yearOfDiagnosis;
    private double daysToLastFollowUp;
    
    private static final Pattern TCGA_SAMPLE_BARCODE_REGEX =
        Pattern.compile("^(TCGA-\\w\\w-\\w\\w\\w\\w-\\d\\d).*$");   
    
    public GDCCase() {}
    
    public GDCCase(JSONObject jsonCase, String filterNormalSampleFlag) {
        JSONObject node = (JSONObject) jsonCase.get("node");
        JSONObject demographic = (JSONObject) node.get("demographic");
        JSONObject diagnoses = (JSONObject) node.get("diagnoses");
        JSONObject diagnosesHits = (JSONObject) diagnoses.get("hits");
        JSONArray diagnosesEdges = (JSONArray) diagnosesHits.get("edges");
        caseId = (String) node.get("case_id");
        // Patient data
        if (node.get("disease_type") != null) {
            cancerType = (String) node.get("disease_type");
        }
        if (node.get("primary_site") != null) {
            cancerType = (String) node.get("primary_site");
        }
        if (demographic.get("race") != null) {
            race = (String) demographic.get("race");
        }
        if (demographic.get("ethnicity") != null) {
            ethnicity = (String) demographic.get("ethnicity");
        }
        if (demographic.get("gender") != null) {
            gender = (String) demographic.get("gender");
        }
        if (demographic.get("vital_status") != null) {
            osStatus = (String) demographic.get("vital_status");
        }
        if (demographic.get("year_of_birth") != null) {
            yearOfBirth = (double) demographic.get("year_of_birth");
        }
        if (demographic.get("days_to_death") != null) {
            daysToDeath = (double) demographic.get("days_to_death");
        }
        for (Object diagnosesObject : diagnosesEdges) {
            JSONObject diagnosesJson = (JSONObject) diagnosesObject;
            JSONObject diagnosesNode = (JSONObject) diagnosesJson.get("node");
            if (diagnosesNode.get("year_of_diagnosis") != null) {
                yearOfDiagnosis = (double) diagnosesNode.get("year_of_diagnosis");
            }
            if (diagnosesNode.get("days_to_last_follow_up") != null) {
                daysToLastFollowUp = (double) diagnosesNode.get("days_to_last_follow_up");
            }
            if (diagnosesNode.get("tumor_grade") != null) {
                tumorGrade = (String) diagnosesNode.get("tumor_grade");
            }
            if (diagnosesNode.get("tumor_stage") != null) {
                tumorStage = (String) diagnosesNode.get("tumor_stage");
            }
        }
        
        JSONObject samples = (JSONObject) node.get("samples");
        JSONObject sampleHits = (JSONObject) samples.get("hits");
        JSONArray edges = (JSONArray) sampleHits.get("edges");
        for (Object sampleObject : edges) {
            JSONObject sample = (JSONObject) sampleObject;
            JSONObject sampleNode = (JSONObject) sample.get("node");
            String submitterId = (String) sampleNode.get("submitter_id");
            sampleUUID = (String) sampleNode.get("sample_id");
            sampleTypeId = (String) sampleNode.get("sample_type_id");
            if (sampleNode.get("sample_type") != null) {
                sampleType = (String) sampleNode.get("sample_type");
            }
            if ((filterNormalSampleFlag.equals("true") && !sampleTypeId.equals(CommonDataUtil.NORMAL_SAMPLE_SUFFIX))) {
                Matcher tcgaSampleBarcodeMatcher = TCGA_SAMPLE_BARCODE_REGEX.matcher(submitterId);
                sampleId = (tcgaSampleBarcodeMatcher.find()) ? tcgaSampleBarcodeMatcher.group(1) : submitterId;
                String barcodeParts[] = submitterId.split("-");
                patientId = barcodeParts[0] + "-" + barcodeParts[1] + "-" + barcodeParts[2];
                // Drill down to get the aliquot id mapping
                JSONObject portions = (JSONObject) sampleNode.get("portions");
                JSONObject portionHits = (JSONObject) portions.get("hits");
                JSONArray portionEdges = (JSONArray) portionHits.get("edges");
                for (Object portionObject : portionEdges) {
                    JSONObject portion = (JSONObject) portionObject;
                    JSONObject portionNode = (JSONObject) portion.get("node");
                    JSONObject analytes = (JSONObject) portionNode.get("analytes");
                    JSONObject analyteHits = (JSONObject) analytes.get("hits");
                    JSONArray analytesEdges = (JSONArray) analyteHits.get("edges");
                    for (Object analyteObject : analytesEdges) {
                        JSONObject analyte = (JSONObject) analyteObject;
                        JSONObject analyteNode = (JSONObject) analyte.get("node");
                        JSONObject aliquots = (JSONObject) analyteNode.get("aliquots");
                        JSONObject aliquotsHits = (JSONObject) aliquots.get("hits");
                        JSONArray aliquotsEdges = (JSONArray) aliquotsHits.get("edges");
                        for (Object aliquotObject : aliquotsEdges) {
                            JSONObject aliquot = (JSONObject) aliquotObject;
                            JSONObject aliquotHit = (JSONObject) aliquot.get("node");
                            aliquotIds.add((String) aliquotHit.get("aliquot_id")); 
                        }
                    }
                }
            }
        }        
    }
    
    public String getCancerType() {
        return cancerType;
    }
    
    public void setCancerType(String cancerType) {
        this.cancerType = cancerType;
    }

    public String getPrimarySite() {
        return primarySite;
    }
    
    public void setPrimarySite(String primarySite) {
        this.primarySite = primarySite;
    }
    
    public String getGender() {
        return gender;
    }
    
    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getRace() {
        return race;
    }
    
    public void setRace(String race) {
        this.race = race;
    }  

    public String getEthnicity() {
        return ethnicity;
    }
    
    public void setEthnicity(String ethnicity) {
        this.ethnicity = ethnicity;
    }  

    public String getOsStatus() {
        return osStatus;
    }
    
    public void setOsStatus(String osStatus) {
        this.osStatus = osStatus;
    }   

    public String getTumorGrade() {
        return tumorGrade;
    }
    
    public void setTumorGrade(String tumorGrade) {
        this.tumorGrade = tumorGrade;
    }  

    public String getTumorStage() {
        return tumorStage;
    }
    
    public void setTumorStage(String tumorStage) {
        this.tumorStage = tumorStage;
    } 
    
    public String getSampleId() {
        return sampleId;
    }
    
    public void setSampleId(String sampleId) {
        this.sampleId = sampleId;
    }
    
    public String getPatientId() {
        return patientId;
    }
    
    public void setPatientId(String patientId) {
        this.patientId = patientId;
    }    

    public String getSampleType() {
        return sampleType;
    }
    
    public void setSampleType(String sampleType) {
        this.sampleType = sampleType;
    }
    
    public double getYearOfBirth() {
        return yearOfBirth;
    }
    
    public void setYearOfBirth(double yearOfBirth) {
        this.yearOfBirth = yearOfBirth;
    }
    
    public double getDaysToDeath() {
        return daysToDeath;
    }
    
    public void setDaysToDeath(double daysToDeath) {
        this.daysToDeath = daysToDeath;
    }

    public double getYearOfDiagnosis() {
        return yearOfDiagnosis;
    }
    
    public void setYearOfDiagnosis(double yearOfDiagnosis) {
        this.yearOfDiagnosis = yearOfDiagnosis;
    }

    public double getDaysToLastFollowUp() {
        return daysToLastFollowUp;
    }
    
    public void setDaysToLastFollowUp(double daysToLastFollowUp) {
        this.daysToLastFollowUp = daysToLastFollowUp;
    }
    
    public List<String> getAliquotIds() {
        return aliquotIds;
    }
    
    public void setAliquoteIds(List<String> aliquotIds) {
        this.aliquotIds = aliquotIds;
    }
    
    public void setCaseId(String caseId) {
        this.caseId = caseId;
    }    

    public String getCaseId() {
        return caseId;
    }

    public void setSampleUUID(String sampleUUID) {
        this.sampleUUID = sampleUUID;
    }    

    public String getSampleUUID() {
        return sampleUUID;
    }    
}
