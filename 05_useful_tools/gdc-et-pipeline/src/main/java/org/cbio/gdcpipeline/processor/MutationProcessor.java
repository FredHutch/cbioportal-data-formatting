package org.cbio.gdcpipeline.processor;

import java.util.ArrayList;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbioportal.annotator.Annotator;
import org.cbioportal.models.AnnotatedRecord;
import org.cbioportal.models.MutationRecord;
import org.springframework.batch.item.ItemProcessor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.cbio.gdcpipeline.model.ensemblmap.EnsemblMap;
import org.cbio.gdcpipeline.model.genomenexus.GenomeNexusEnsemblResponse;
import org.cbioportal.annotator.GenomeNexusAnnotationFailureException;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

/**
 * @author Dixit Patel
 */
public class MutationProcessor implements ItemProcessor<MutationRecord,AnnotatedRecord> {
    private static Pattern pattern = Pattern.compile("^(TCGA-\\w\\w-\\w\\w\\w\\w-(\\d\\d|Tumor)).*$");
    private static Map<String,String> validChrValues = null;
    private static Log LOG = LogFactory.getLog(MutationProcessor.class);
    @Value("#{jobParameters[isoformOverrideSource]}")
    private String isoformOverrideSource;
    private RestTemplate restTemplate = new RestTemplate();

    @Autowired
    private Annotator annotator;

    @Override
    public AnnotatedRecord process(MutationRecord mutationRecord) throws Exception {
        mutationRecord.setTUMOR_SAMPLE_BARCODE(extractSampleId(mutationRecord.getTUMOR_SAMPLE_BARCODE()));
        mutationRecord.setMATCHED_NORM_SAMPLE_BARCODE(extractSampleId(mutationRecord.getMATCHED_NORM_SAMPLE_BARCODE()));
        mutationRecord.setCHROMOSOME(normalizeChromosome(mutationRecord.getCHROMOSOME()));
        if (mutationRecord.getNCBI_BUILD().equalsIgnoreCase("grch38")) {
            mapToGrch37(mutationRecord);
        }
        AnnotatedRecord annotatedRecord = annotateRecord(mutationRecord);
        return annotatedRecord;
    }

    private String extractSampleId(String record) {
        Matcher matcher = pattern.matcher(record);
        if(matcher.find()) {
            record = matcher.group();
        }
        return record;
    }

    private String normalizeChromosome(String chromosome){
        if (chromosome == null){
            return null;
        }
        if (validChrValues==null) {
            validChrValues = new HashMap<>();
            for (int lc = 1; lc<=24; lc++) {
                validChrValues.put(Integer.toString(lc),Integer.toString(lc));
                validChrValues.put("CHR" + Integer.toString(lc), Integer.toString(lc));
            }
            validChrValues.put("X","23");
            validChrValues.put("CHRX","23");
            validChrValues.put("Y","24");
            validChrValues.put("CHRY","24");
            validChrValues.put("NA","NA");
            validChrValues.put("MT","MT"); // mitochondria
        }
        return validChrValues.get(chromosome.toUpperCase());
    }

    private AnnotatedRecord annotateRecord(MutationRecord record) throws GenomeNexusAnnotationFailureException {
        AnnotatedRecord annotatedRecord = new AnnotatedRecord();
        try {
            annotatedRecord = annotator.annotateRecord(record, false, isoformOverrideSource, true);
        } catch (HttpServerErrorException e) {
            if (LOG.isWarnEnabled()) {
                LOG.warn("Server Exception. Failed to annotate a record from json! Sample: " + record.getTUMOR_SAMPLE_BARCODE() + " Variant: " + record.getCHROMOSOME() + ":" + record.getSTART_POSITION() + record.getREFERENCE_ALLELE() + ">" + record.getTUMOR_SEQ_ALLELE2());
            }
        } catch (HttpClientErrorException e) {
            if (LOG.isWarnEnabled()) {
                LOG.warn("Client Error Exception. Failed to annotate a record from json! Sample: " + record.getTUMOR_SAMPLE_BARCODE() + " Variant: " + record.getCHROMOSOME() + ":" + record.getSTART_POSITION() + record.getREFERENCE_ALLELE() + ">" + record.getTUMOR_SEQ_ALLELE2());
            }
        } catch (GenomeNexusAnnotationFailureException e) {
            if (LOG.isWarnEnabled()) {
                LOG.warn("Genome Nexus Annotation Failure. Failed to anotate a record from json! Sample: " + record.getTUMOR_SAMPLE_BARCODE() + " Variant: " + record.getCHROMOSOME() + ":" + record.getSTART_POSITION() + record.getREFERENCE_ALLELE() + ">" + record.getTUMOR_SEQ_ALLELE2());
                annotatedRecord = new AnnotatedRecord(record);
            }
        }
        return annotatedRecord;
    }

    private void mapToGrch37(MutationRecord mutationRecord) {
        HttpHeaders httpHeaders = new HttpHeaders();
        httpHeaders.setContentType(MediaType.APPLICATION_JSON);

        EnsemblMap mapping = new EnsemblMap();

        Map<String, String> strandMap = new HashMap<>();
        strandMap.put("+", "1");
        strandMap.put("-", "0");
        strandMap.put("1", "1");
        strandMap.put("0", "0");

        String payload = "/map/human/GRCh38/" + mutationRecord.getCHROMOSOME() + ":" + mutationRecord.getSTART_POSITION() + ".." + mutationRecord.getEND_POSITION() + ":" + strandMap.get(mutationRecord.getSTRAND()) + "/GRCh37?content-type=application-json";
        HttpEntity<String> entity = new HttpEntity<>(httpHeaders);
        try {
            ResponseEntity<EnsemblMap> response = restTemplate.exchange("https://rest.ensembl.org" + payload, HttpMethod.GET, entity, EnsemblMap.class);
            mapping = response.getBody();
            mutationRecord.setSTART_POSITION(Integer.toString(mapping.getMappings().get(0).getMapped().getStart()));
            mutationRecord.setEND_POSITION(Integer.toString(mapping.getMappings().get(0).getMapped().getEnd()));
        }
        catch (Exception e){
            LOG.error("Failed to retreive gene mapping");
            return;
        }
    }
}
