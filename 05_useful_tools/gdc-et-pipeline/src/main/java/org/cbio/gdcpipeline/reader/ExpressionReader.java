/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.cbio.gdcpipeline.reader;

import java.io.BufferedReader;
import java.util.List;
import java.util.Map;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.ManifestFileData;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.ItemStreamReader;
import org.springframework.batch.item.NonTransientResourceException;
import org.springframework.batch.item.ParseException;
import org.springframework.batch.item.UnexpectedInputException;
import org.springframework.beans.factory.annotation.Value;
import org.cbio.gdcpipeline.util.CommonDataUtil;
import java.io.File;
import java.io.FileReader;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;
import org.apache.commons.collections.map.MultiKeyMap;
import org.cbio.gdcpipeline.util.GenomeNexusCache;
import org.springframework.beans.factory.annotation.Autowired;

/**
 *
 * @author heinsz
 */
public class ExpressionReader implements ItemStreamReader<String> {

    @Value("#{jobParameters[sourceDirectory]}")
    private String sourceDir;

    @Value("#{jobExecutionContext[gdcManifestData]}")
    private List<ManifestFileData> gdcManifestData;

    @Value("#{jobExecutionContext[gdcAliquotIdToSampleId]}")
    private Map<String, String> gdcAliquotIdToSampleId;

    @Value("#{jobExecutionContext[gdcIdToSampleId]}")
    private Map<String, String> gdcIdToSampleId;

    @Value("#{jobExecutionContext[gdcUUIDToSampleId]}")
    private Map<String, String> gdcUUIDToSampleId;

    @Autowired
    GenomeNexusCache genomeNexusCache;

    private List<String> expressionRecords = new ArrayList<>();
    private MultiKeyMap expressionMap = new MultiKeyMap();
    private Set<String> genes = new HashSet<>();
    private Set<String> samplesSeen = new HashSet();
    private List<String> sampleIds = new ArrayList<>();
    private static Log LOG = LogFactory.getLog(ExpressionReader.class);

    private static final Pattern FILENAME_PATTERN = Pattern.compile("(\\S+)\\.htseq\\.counts.*");

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        for (ManifestFileData fileData : gdcManifestData) {
            if (CommonDataUtil.GDC_TYPE.EXPRESSION.toString().equalsIgnoreCase(fileData.getDatatype().replace(" ", "_"))) {
                File expressionFile;
                LOG.info("Processing Expression file: " + fileData.getFilename());
                try {
                    Path path = Paths.get(sourceDir, fileData.getId(), fileData.getFilename());
                        expressionFile = CommonDataUtil.extractCompressedFile(path.toFile());
                }
                catch (Exception e) {
                    LOG.error("Failed to extract file");
                    throw new ItemStreamException("Failed to process file");
                }

                try {
                    String sampleId = fileData.getSampleIds().get(0);
                    if (gdcAliquotIdToSampleId.containsKey(sampleId.toUpperCase()) && !samplesSeen.contains(sampleId)) {
                        readFile(expressionFile, executionContext, gdcAliquotIdToSampleId.get(sampleId));
                    }
                    else if (gdcIdToSampleId.containsKey(sampleId.toUpperCase()) && !samplesSeen.contains(sampleId)) {
                        readFile(expressionFile, executionContext, gdcIdToSampleId.get(sampleId.toUpperCase()));
                    }
                    else if (gdcUUIDToSampleId.containsKey(sampleId.toUpperCase()) && !samplesSeen.contains(sampleId)) {
                        readFile(expressionFile, executionContext, gdcUUIDToSampleId.get(sampleId.toUpperCase()));
                    }
                    else {
                        LOG.error("Could not find id from filename " + fileData.getFilename());
                    }
                    samplesSeen.add(sampleId);
                }
                catch (Exception e) {
                    LOG.error("Failed to read file " + fileData.getFilename());
                }
            }
        }
        generateExpressionRecords();
        List<String> headerList = new ArrayList<>();
        headerList.add("Hugo_Symbol");
        for (String sampleId : sampleIds) {
            headerList.add(sampleId);
        }
        executionContext.put("expressionHeader", headerList);
    }

    @Override
    public void update(ExecutionContext arg0) throws ItemStreamException {}

    @Override
    public void close() throws ItemStreamException {}

    @Override
    public String read() throws Exception, UnexpectedInputException, ParseException, NonTransientResourceException {
        if (!expressionRecords.isEmpty()) {
            return expressionRecords.remove(0);
        }
        return null;
    }

    private void readFile(File expressionFile, ExecutionContext e, String sampleId) throws Exception {
        //TODO: There should be a cache for gene id mappings
        BufferedReader br = new BufferedReader(new FileReader(expressionFile));
        String line;
        while ((line = br.readLine()) != null) {
            if (line.startsWith("_")) {
                continue;
            }
            String lineData[] = line.split("\t");
            String geneId = lineData[0];
            String value = lineData[1];
            genes.add(genomeNexusCache.getHugoSymbolFromEnsembl(geneId));
            //genes.add(geneId);
            if (!sampleIds.contains(sampleId)) {
                sampleIds.add(sampleId);
            }
            expressionMap.put(geneId, sampleId, value);
        }
    }

    private void generateExpressionRecords() {
        for (String gene : genes) {
            String expressionRecord = gene;
            for (String sampleId : sampleIds) {
                expressionRecord = expressionRecord + "\t" + expressionMap.get(gene, sampleId);
            }
            expressionRecords.add(expressionRecord);
        }
    }
}
