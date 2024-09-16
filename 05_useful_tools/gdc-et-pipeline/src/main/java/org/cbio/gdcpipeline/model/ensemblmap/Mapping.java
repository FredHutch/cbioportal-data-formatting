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
    "original",
    "mapped"
})
public class Mapping {

    @JsonProperty("original")
    private Original original;
    @JsonProperty("mapped")
    private Mapped mapped;
    @JsonIgnore
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
    * No args constructor for use in serialization
    *
    */
    public Mapping() {}

    /**
    *
    * @param original
    * @param mapped
    */
    public Mapping(Original original, Mapped mapped) {
        super();
        this.original = original;
        this.mapped = mapped;
    }

    @JsonProperty("original")
    public Original getOriginal() {
        return original;
    }

    @JsonProperty("original")
    public void setOriginal(Original original) {
        this.original = original;
    }

    public Mapping withOriginal(Original original) {
    this.original = original;
        return this;
    }

    @JsonProperty("mapped")
    public Mapped getMapped() {
        return mapped;
    }

    @JsonProperty("mapped")
    public void setMapped(Mapped mapped) {
        this.mapped = mapped;
    }

    public Mapping withMapped(Mapped mapped) {
        this.mapped = mapped;
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

    public Mapping withAdditionalProperty(String name, Object value) {
        this.additionalProperties.put(name, value);
        return this;
    }
}
