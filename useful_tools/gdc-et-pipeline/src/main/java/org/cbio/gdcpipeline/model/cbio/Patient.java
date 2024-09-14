package org.cbio.gdcpipeline.model.cbio;

import org.cbio.gdcpipeline.model.ClinicalDataSourceImpl;
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
public class Patient extends ClinicalDataModel {
    private String patient_id;
    private String gender;
    private double age;
    private String os_status;
    private String os_months;
    private String race;
    private String ethnicity;
    private String tumor_grade;
    private ClinicalDataSourceImpl clinicalDataSource = new ClinicalDataSourceImpl();
    private static final float AVG_NUM_DAYS_MONTH = 30.44f;

    public Patient() {
    }

    private static enum VitalStatusAlive {
        ALIVE("Alive"),
        LIVING("LIVING");

        private String propertyName;

        VitalStatusAlive(String propertyName) {
            this.propertyName = propertyName;
        }

        public String toString() { return propertyName; }

        static public boolean has(String value) {
            if (value == null) return false;
            try {
                return valueOf(value.toUpperCase()) != null;
            }
            catch (IllegalArgumentException x) {
                return false;
            }
        }
    }

    private static enum VitalStatusDead {
        DEAD("Dead"),
        DECEASED("DECEASED");

        private String propertyName;

        VitalStatusDead(String propertyName) {
            this.propertyName = propertyName;
        }

        public String toString() { return propertyName; }

        static public boolean has(String value) {
            if (value == null) return false;
            try {
                return valueOf(value.toUpperCase()) != null;
            }
            catch (IllegalArgumentException x) {
                return false;
            }
        }
    }

    public Patient(String patient_id, String os_status, String os_months, String gender, double age, String race, String ethnicity, String tumor_grade) {
        this.patient_id = patient_id;
        this.gender = gender;
        this.age = age;
        this.os_status = os_status;
        this.os_months = os_months;
        this.race = race;
        this.ethnicity = ethnicity;
        this.tumor_grade = tumor_grade;
    }

    public Patient(GDCCase gdcCase) {
        patient_id = gdcCase.getPatientId();
        gender = gdcCase.getGender();
        age = gdcCase.getYearOfBirth() - gdcCase.getYearOfDiagnosis();
        os_status = gdcCase.getOsStatus();
        os_months = calcOverallSurvivalMonths(gdcCase.getDaysToDeath(), gdcCase.getDaysToLastFollowUp(), os_status);
        race = gdcCase.getRace();
        ethnicity = gdcCase.getEthnicity();
        tumor_grade = gdcCase.getTumorGrade();
    }

    @Override
    public List<String> getFields() {
        List<String> fields = new ArrayList<>();
        fields.add("Patient_id");
        fields.add("Os_status");
        fields.add("Os_months");
        fields.add("Age");
        fields.add("Gender");
        fields.add("Race");
        fields.add("Ethnicity");
        fields.add("Tumor_grade");
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

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public double getAge() {
        return age;
    }

    public void setAge(double age) {
        this.age = age;
    }

    public String getOs_status() {
        return os_status;
    }

    public void setOs_status(String os_status) {
        this.os_status = this.clinicalDataSource.getNormalizedClinicalFieldValue(os_status);
    }

    public String getOs_months() {
        return os_months;
    }

    public void set_Os_months(String os_months) {
        this.os_months = os_months;
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

    public String getTumor_grade() {
        return tumor_grade;
    }

    public void setTumor_grade(String tumorGrade) {
        this.tumor_grade = tumor_grade;
    }

    /**
     * Calculates Overall Survival Months.
     * If the patient is alive, use the number of days since to the last follow up
     * If the patient is deceased, use the number of days to death. Both values
     * are divided by the average number of days in a month.
     *
     * @param daysToDeath
     * @param daysToLastFollowup
     * @param vitalStatus
     * @return
     */
    public static String calcOverallSurvivalMonths(double daysToDeath, double daysToLastFollowup, String vitalStatus) {
        String osSurvivalMonths = "NA";
        if (VitalStatusAlive.has(vitalStatus)) {
            osSurvivalMonths =  String.format("%.3f", daysToLastFollowup / AVG_NUM_DAYS_MONTH);
        }
        else if (VitalStatusDead.has(vitalStatus)) {
            osSurvivalMonths = String.format("%.3f", daysToDeath / AVG_NUM_DAYS_MONTH);
        }
        return osSurvivalMonths;
    }
}
