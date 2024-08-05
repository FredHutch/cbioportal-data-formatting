package org.cbio.gdcpipeline.model.genomenexus;

import java.util.HashMap;
import java.util.Map;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "exonId",
    "exonStart",
    "exonEnd",
    "rank",
    "strand",
    "version"
})
public class Exon {

    @JsonProperty("exonId")
    private String exonId;
    @JsonProperty("exonStart")
    private Integer exonStart;
    @JsonProperty("exonEnd")
    private Integer exonEnd;
    @JsonProperty("rank")
    private Integer rank;
    @JsonProperty("strand")
    private Integer strand;
    @JsonProperty("version")
    private Integer version;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public Exon() {
    }

    /**
    *
    * @param exonStart
    * @param rank
    * @param exonEnd
    * @param strand
    * @param exonId
    * @param version
    */
    public Exon(String exonId, Integer exonStart, Integer exonEnd, Integer rank, Integer strand, Integer version) {
        super();
        this.exonId = exonId;
        this.exonStart = exonStart;
        this.exonEnd = exonEnd;
        this.rank = rank;
        this.strand = strand;
        this.version = version;
    }

    @JsonProperty("exonId")
    public String getExonId() {
        return exonId;
    }

    @JsonProperty("exonId")
    public void setExonId(String exonId) {
        this.exonId = exonId;
    }

    public Exon withExonId(String exonId) {
        this.exonId = exonId;
        return this;
    }

    @JsonProperty("exonStart")
    public Integer getExonStart() {
        return exonStart;
    }

    @JsonProperty("exonStart")
    public void setExonStart(Integer exonStart) {
        this.exonStart = exonStart;
    }

    public Exon withExonStart(Integer exonStart) {
        this.exonStart = exonStart;
        return this;
    }

    @JsonProperty("exonEnd")
    public Integer getExonEnd() {
        return exonEnd;
    }

    @JsonProperty("exonEnd")
    public void setExonEnd(Integer exonEnd) {
        this.exonEnd = exonEnd;
    }

    public Exon withExonEnd(Integer exonEnd) {
        this.exonEnd = exonEnd;
        return this;
    }

    @JsonProperty("rank")
    public Integer getRank() {
        return rank;
    }

    @JsonProperty("rank")
    public void setRank(Integer rank) {
        this.rank = rank;
    }

    public Exon withRank(Integer rank) {
        this.rank = rank;
        return this;
    }

    @JsonProperty("strand")
    public Integer getStrand() {
        return strand;
    }

    @JsonProperty("strand")
    public void setStrand(Integer strand) {
        this.strand = strand;
    }

    public Exon withStrand(Integer strand) {
        this.strand = strand;
        return this;
    }

    @JsonProperty("version")
    public Integer getVersion() {
        return version;
    }

    @JsonProperty("version")
    public void setVersion(Integer version) {
        this.version = version;
    }

    public Exon withVersion(Integer version) {
        this.version = version;
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

    public Exon withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}