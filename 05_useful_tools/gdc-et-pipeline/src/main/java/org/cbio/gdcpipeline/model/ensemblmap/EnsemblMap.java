package org.cbio.gdcpipeline.model.ensemblmap;

import java.util.ArrayList;
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
    "mappings"
})
public class EnsemblMap {
    @JsonProperty("mappings")
    private List<Mapping> mappings = new ArrayList<Mapping>();
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public EnsemblMap() {}

    /**
    *
    * @param mappings
    */
    public EnsemblMap(List<Mapping> mappings) {
        super();
        this.mappings = mappings;
    }

    @JsonProperty("mappings")
    public List<Mapping> getMappings() {
        return mappings;
    }

    @JsonProperty("mappings")
    public void setMappings(List<Mapping> mappings) {
        this.mappings = mappings;
    }

    public EnsemblMap withMappings(List<Mapping> mappings) {
        this.mappings = mappings;
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

    public EnsemblMap withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}