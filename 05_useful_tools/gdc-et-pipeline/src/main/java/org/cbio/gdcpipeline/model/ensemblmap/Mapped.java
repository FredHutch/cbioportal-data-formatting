package org.cbio.gdcpipeline.model.ensemblmap;

import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;
import java.util.HashMap;
import java.util.Map;

@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonPropertyOrder({
    "end",
    "assembly",
    "coord_system",
    "strand",
    "start",
    "seq_region_name"
})
public class Mapped {
    @JsonProperty("end")
    private Integer end;
    @JsonProperty("assembly")
    private String assembly;
    @JsonProperty("coord_system")
    private String coordSystem;
    @JsonProperty("strand")
    private Integer strand;
    @JsonProperty("start")
    private Integer start;
    @JsonProperty("seq_region_name")
    private String seqRegionName;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public Mapped() {}

    /**
    *
    * @param start
    * @param assembly
    * @param strand
    * @param seqRegionName
    * @param coordSystem
    * @param end
    */
    public Mapped(Integer end, String assembly, String coordSystem, Integer strand, Integer start, String seqRegionName) {
        super();
        this.end = end;
        this.assembly = assembly;
        this.coordSystem = coordSystem;
        this.strand = strand;
        this.start = start;
        this.seqRegionName = seqRegionName;
    }

    @JsonProperty("end")
    public Integer getEnd() {
        return end;
    }

    @JsonProperty("end")
    public void setEnd(Integer end) {
        this.end = end;
    }

    public Mapped withEnd(Integer end) {
        this.end = end;
        return this;
    }

    @JsonProperty("assembly")
    public String getAssembly() {
        return assembly;
    }

    @JsonProperty("assembly")
    public void setAssembly(String assembly) {
        this.assembly = assembly;
    }

    public Mapped withAssembly(String assembly) {
        this.assembly = assembly;
        return this;
    }

    @JsonProperty("coord_system")
    public String getCoordSystem() {
        return coordSystem;
    }

    @JsonProperty("coord_system")
    public void setCoordSystem(String coordSystem) {
        this.coordSystem = coordSystem;
    }

    public Mapped withCoordSystem(String coordSystem) {
        this.coordSystem = coordSystem;
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

    public Mapped withStrand(Integer strand) {
        this.strand = strand;
        return this;
    }

    @JsonProperty("start")
    public Integer getStart() {
        return start;
    }

    @JsonProperty("start")
    public void setStart(Integer start) {
        this.start = start;
    }

    public Mapped withStart(Integer start) {
        this.start = start;
        return this;
    }

    @JsonProperty("seq_region_name")
    public String getSeqRegionName() {
        return seqRegionName;
    }

    @JsonProperty("seq_region_name")
    public void setSeqRegionName(String seqRegionName) {
        this.seqRegionName = seqRegionName;
    }

    public Mapped withSeqRegionName(String seqRegionName) {
        this.seqRegionName = seqRegionName;
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

    public Mapped withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}