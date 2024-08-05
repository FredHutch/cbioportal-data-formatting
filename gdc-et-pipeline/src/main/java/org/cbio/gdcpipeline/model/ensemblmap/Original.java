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
    "strand",
    "seq_region_name",
    "start",
    "end",
    "assembly",
    "coord_system"
})
public class Original {

    @JsonProperty("strand")
    private Integer strand;
    @JsonProperty("seq_region_name")
    private String seqRegionName;
    @JsonProperty("start")
    private Integer start;
    @JsonProperty("end")
    private Integer end;
    @JsonProperty("assembly")
    private String assembly;
    @JsonProperty("coord_system")
    private String coordSystem;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public Original() {}

    /**
    *
    * @param start
    * @param assembly
    * @param strand
    * @param seqRegionName
    * @param coordSystem
    * @param end
    */
    public Original(Integer strand, String seqRegionName, Integer start, Integer end, String assembly, String coordSystem) {
        super();
        this.strand = strand;
        this.seqRegionName = seqRegionName;
        this.start = start;
        this.end = end;
        this.assembly = assembly;
        this.coordSystem = coordSystem;
    }

    @JsonProperty("strand")
    public Integer getStrand() {
        return strand;
    }

    @JsonProperty("strand")
    public void setStrand(Integer strand) {
        this.strand = strand;
    }

    public Original withStrand(Integer strand) {
    this.strand = strand;
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

    public Original withSeqRegionName(String seqRegionName) {
    this.seqRegionName = seqRegionName;
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

    public Original withStart(Integer start) {
        this.start = start;
        return this;
    }

    @JsonProperty("end")
    public Integer getEnd() {
        return end;
    }

    @JsonProperty("end")
    public void setEnd(Integer end) {
        this.end = end;
    }

    public Original withEnd(Integer end) {
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

    public Original withAssembly(String assembly) {
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

    public Original withCoordSystem(String coordSystem) {
    this.coordSystem = coordSystem;
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

    public Original withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}