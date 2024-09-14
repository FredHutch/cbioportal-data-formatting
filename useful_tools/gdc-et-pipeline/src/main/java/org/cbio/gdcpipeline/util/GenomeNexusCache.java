package org.cbio.gdcpipeline.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.genomenexus.GenomeNexusEnsemblResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

/**
 *
 * @author heinsz
 */
public class GenomeNexusCache {
    
    private Map<String, GenomeNexusEnsemblResponse> genes = new HashMap<>();
    private static Log LOG = LogFactory.getLog(GenomeNexusCache.class);
    
    @Value("${cna.geneId.field}")
    private String geneField;           
            
    @Value("${cna.genomenexus.endpoint}")
    private String url;
    
    private RestTemplate restTemplate = new RestTemplate();
    
    public GenomeNexusCache(){}    
    
    public String getHugoSymbolFromEnsembl(String geneId) {
        if(!genes.containsKey(geneId)) {
            genes.put(geneId, getDataFromGenomeNexus(geneId));
        }
        try {
            return genes.get(geneId).getHugoSymbols().get(0);
        }        
        catch (NullPointerException e) {
            LOG.error("No Hugo symbols for gene " + geneId);
            return geneId;
        }
    }
    
    private GenomeNexusEnsemblResponse getDataFromGenomeNexus(String geneId) {
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);        
        geneId = geneId.substring(0, geneId.indexOf("."));
        String payload = "?" + geneField + "=" + geneId;
        HttpEntity<String> entity = new HttpEntity<>(httpHeaders);
        try {
            LOG.info("Fetching gene data from GenomeNexus for " + geneId);
            ResponseEntity<GenomeNexusEnsemblResponse[]> response = restTemplate.exchange(url + payload, HttpMethod.GET, entity, GenomeNexusEnsemblResponse[].class);
            return response.getBody()[0];            
        }
        catch (Exception e){
            LOG.error("Failed to retreive gene annotation from genome nexus for gene " + geneId);
            GenomeNexusEnsemblResponse defaultGNResponse = new GenomeNexusEnsemblResponse();
            List<String> ids = new ArrayList<>();
            ids.add(geneId);
            defaultGNResponse.setHugoSymbols(ids);
            defaultGNResponse.setGeneId(geneId);
            return defaultGNResponse;
        }        
    }
}
