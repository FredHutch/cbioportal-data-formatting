package org.cbio.gdcpipeline.model;

import org.cbio.gdcpipeline.util.CommonDataUtil;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author Dixit Patel
 */
public class ClinicalDataSourceImpl implements ClinicalDataSource {
    private Map<String, String> clinicalFieldMap = initClinicalFieldValues();

    public ClinicalDataSourceImpl() {
    }

    private Map<String,String> initClinicalFieldValues() {
        Map<String, String> map = new HashMap<>();
        map.put("alive", CommonDataUtil.CLINICAL_OS_STATUS.LIVING.toString());
        map.put("dead", CommonDataUtil.CLINICAL_OS_STATUS.DECEASED.toString());
        return map;
    }

    @Override
    public String getNormalizedClinicalFieldValue(String key) {
        if (!key.isEmpty()) {
            return this.clinicalFieldMap.get(key.toLowerCase());
        }
        return null;
    }

    @Override
    public List<Map<String, String>> getClinicalData() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public List<String> getSampleHeader() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public List<String> getPatientHeader() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public List<String> getTimelineHeader() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public List<Map<String, String>> getTimelineData() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public String getNextClinicalStudyId() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public String getNextTimelineStudyId() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public boolean hasMoreTimelineData() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public boolean hasMoreClinicalData() {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public Map<String, List<String>> getFullPatientHeader(Map<String, List<String>> fullHeader) {
        throw new UnsupportedOperationException("Not Supported Yet");
    }

    @Override
    public Map<String, List<String>> getFullSampleHeader(Map<String, List<String>> fullHeader) {
        throw new UnsupportedOperationException("Not Supported Yet");
    }


}
