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
    "pfamDomainId",
    "pfamDomainStart",
    "pfamDomainEnd"
})
public class PfamDomain {

    @JsonProperty("pfamDomainId")
    private String pfamDomainId;
    @JsonProperty("pfamDomainStart")
    private Integer pfamDomainStart;
    @JsonProperty("pfamDomainEnd")
    private Integer pfamDomainEnd;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public PfamDomain() {
    }

    /**
    *
    * @param pfamDomainId
    * @param pfamDomainEnd
    * @param pfamDomainStart
    */
    public PfamDomain(String pfamDomainId, Integer pfamDomainStart, Integer pfamDomainEnd) {
        super();
        this.pfamDomainId = pfamDomainId;
        this.pfamDomainStart = pfamDomainStart;
        this.pfamDomainEnd = pfamDomainEnd;
    }

    @JsonProperty("pfamDomainId")
    public String getPfamDomainId() {
        return pfamDomainId;
    }

    @JsonProperty("pfamDomainId")
    public void setPfamDomainId(String pfamDomainId) {
        this.pfamDomainId = pfamDomainId;
    }

    public PfamDomain withPfamDomainId(String pfamDomainId) {
        this.pfamDomainId = pfamDomainId;
        return this;
    }

    @JsonProperty("pfamDomainStart")
    public Integer getPfamDomainStart() {
        return pfamDomainStart;
    }

    @JsonProperty("pfamDomainStart")
    public void setPfamDomainStart(Integer pfamDomainStart) {
        this.pfamDomainStart = pfamDomainStart;
    }

    public PfamDomain withPfamDomainStart(Integer pfamDomainStart) {
        this.pfamDomainStart = pfamDomainStart;
        return this;
    }

    @JsonProperty("pfamDomainEnd")
    public Integer getPfamDomainEnd() {
        return pfamDomainEnd;
    }

    @JsonProperty("pfamDomainEnd")
    public void setPfamDomainEnd(Integer pfamDomainEnd) {
        this.pfamDomainEnd = pfamDomainEnd;
    }

    public PfamDomain withPfamDomainEnd(Integer pfamDomainEnd) {
        this.pfamDomainEnd = pfamDomainEnd;
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

    public PfamDomain withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}