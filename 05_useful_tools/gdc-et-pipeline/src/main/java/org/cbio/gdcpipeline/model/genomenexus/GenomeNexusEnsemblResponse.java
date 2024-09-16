package org.cbio.gdcpipeline.model.genomenexus;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "transcriptId",
    "geneId",
    "proteinId",
    "proteinLength",
    "pfamDomains",
    "hugoSymbols",
    "refseqMrnaId",
    "ccdsId",
    "exons",
    "utrs"
})
public class GenomeNexusEnsemblResponse {

    @JsonProperty("transcriptId")
    private String transcriptId;
    @JsonProperty("geneId")
    private String geneId;
    @JsonProperty("proteinId")
    private String proteinId;
    @JsonProperty("proteinLength")
    private Integer proteinLength;
    @JsonProperty("pfamDomains")
    private List<PfamDomain> pfamDomains = null;
    @JsonProperty("hugoSymbols")
    private List<String> hugoSymbols = null;
    @JsonProperty("refseqMrnaId")
    private String refseqMrnaId;
    @JsonProperty("ccdsId")
    private String ccdsId;
    @JsonProperty("exons")
    private List<Exon> exons = null;
    @JsonProperty("utrs")
    private List<Utr> utrs = null;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public GenomeNexusEnsemblResponse() {
    }

    /**
    *
    * @param exons
    * @param proteinLength
    * @param pfamDomains
    * @param geneId
    * @param proteinId
    * @param ccdsId
    * @param refseqMrnaId
    * @param hugoSymbols
    * @param utrs
    * @param transcriptId
    */
    public GenomeNexusEnsemblResponse(String transcriptId, String geneId, String proteinId, Integer proteinLength, List<PfamDomain> pfamDomains, List<String> hugoSymbols, String refseqMrnaId, String ccdsId, List<Exon> exons, List<Utr> utrs) {
        this.transcriptId = transcriptId;
        this.geneId = geneId;
        this.proteinId = proteinId;
        this.proteinLength = proteinLength;
        this.pfamDomains = pfamDomains;
        this.hugoSymbols = hugoSymbols;
        this.refseqMrnaId = refseqMrnaId;
        this.ccdsId = ccdsId;
        this.exons = exons;
        this.utrs = utrs;
    }

    @JsonProperty("transcriptId")
    public String getTranscriptId() {
        return transcriptId;
    }

    @JsonProperty("transcriptId")
    public void setTranscriptId(String transcriptId) {
        this.transcriptId = transcriptId;
    }

    public GenomeNexusEnsemblResponse withTranscriptId(String transcriptId) {
        this.transcriptId = transcriptId;
        return this;
    }

    @JsonProperty("geneId")
    public String getGeneId() {
        return geneId;
    }

    @JsonProperty("geneId")
    public void setGeneId(String geneId) {
        this.geneId = geneId;
    }

    public GenomeNexusEnsemblResponse withGeneId(String geneId) {
        this.geneId = geneId;
        return this;
    }

    @JsonProperty("proteinId")
    public String getProteinId() {
        return proteinId;
    }

    @JsonProperty("proteinId")
    public void setProteinId(String proteinId) {
        this.proteinId = proteinId;
    }

    public GenomeNexusEnsemblResponse withProteinId(String proteinId) {
        this.proteinId = proteinId;
        return this;
    }

    @JsonProperty("proteinLength")
    public Integer getProteinLength() {
        return proteinLength;
    }

    @JsonProperty("proteinLength")
    public void setProteinLength(Integer proteinLength) {
        this.proteinLength = proteinLength;
    }

    public GenomeNexusEnsemblResponse withProteinLength(Integer proteinLength) {
        this.proteinLength = proteinLength;
        return this;
    }

    @JsonProperty("pfamDomains")
    public List<PfamDomain> getPfamDomains() {
        return pfamDomains;
    }

    @JsonProperty("pfamDomains")
    public void setPfamDomains(List<PfamDomain> pfamDomains) {
        this.pfamDomains = pfamDomains;
    }

    public GenomeNexusEnsemblResponse withPfamDomains(List<PfamDomain> pfamDomains) {
        this.pfamDomains = pfamDomains;
        return this;
    }

    @JsonProperty("hugoSymbols")
    public List<String> getHugoSymbols() {
        return hugoSymbols;
    }

    @JsonProperty("hugoSymbols")
    public void setHugoSymbols(List<String> hugoSymbols) {
        this.hugoSymbols = hugoSymbols;
    }

    public GenomeNexusEnsemblResponse withHugoSymbols(List<String> hugoSymbols) {
        this.hugoSymbols = hugoSymbols;
        return this;
    }

    @JsonProperty("refseqMrnaId")
    public String getRefseqMrnaId() {
        return refseqMrnaId;
    }

    @JsonProperty("refseqMrnaId")
    public void setRefseqMrnaId(String refseqMrnaId) {
        this.refseqMrnaId = refseqMrnaId;
    }

    public GenomeNexusEnsemblResponse withRefseqMrnaId(String refseqMrnaId) {
        this.refseqMrnaId = refseqMrnaId;
        return this;
    }

    @JsonProperty("ccdsId")
    public String getCcdsId() {
        return ccdsId;
    }

    @JsonProperty("ccdsId")
    public void setCcdsId(String ccdsId) {
        this.ccdsId = ccdsId;
    }

    public GenomeNexusEnsemblResponse withCcdsId(String ccdsId) {
        this.ccdsId = ccdsId;
        return this;
    }

    @JsonProperty("exons")
    public List<Exon> getExons() {
        return exons;
    }

    @JsonProperty("exons")
    public void setExons(List<Exon> exons) {
        this.exons = exons;
    }

    public GenomeNexusEnsemblResponse withExons(List<Exon> exons) {
    this.exons = exons;
        return this;
    }

    @JsonProperty("utrs")
    public List<Utr> getUtrs() {
        return utrs;
    }

    @JsonProperty("utrs")
    public void setUtrs(List<Utr> utrs) {
        this.utrs = utrs;
    }

    public GenomeNexusEnsemblResponse withUtrs(List<Utr> utrs) {
        this.utrs = utrs;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    public GenomeNexusEnsemblResponse withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}