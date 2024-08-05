package org.cbio.gdcpipeline.model.cbio;

import java.util.List;
import org.apache.commons.lang.StringUtils;

/**
 *
 * @author heinsz
 */
public class CnaRecord {
    private String hugoSymbol;
    private String ensemblGeneId;
    private List<String> data;

    public CnaRecord() {}

    public CnaRecord(String hugoSymbol, String entrezGeneId, List<String> data) {
        this.hugoSymbol = hugoSymbol;
        this.ensemblGeneId = entrezGeneId;
        this.data = data;
    }

    // Constructor for when only ensemblGeneId is present
    public CnaRecord(String ensemblGeneId, List<String> data) {
        this.ensemblGeneId = ensemblGeneId;
        this.data = data;
    }

    public String getHugoSymbol() {
        return hugoSymbol;
    }

    public void setHugoSymbol(String hugoSymbol) {
        this.hugoSymbol = hugoSymbol;
    }

    public String getEnsemblGeneId() {
        return ensemblGeneId;
    }

    public void setEnsemblGeneId(String ensemblGeneId) {
        this.ensemblGeneId = ensemblGeneId;
    }

    public List<String> getData() {
        return data;
    }

    public void setData(List<String> data) {
        this.data = data;
    }

    public String getTabDelimData() {
        return StringUtils.join(data, "\t").trim();
    }
}
