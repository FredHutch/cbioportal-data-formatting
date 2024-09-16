package org.cbio.gdcpipeline.reader;

import java.io.BufferedReader;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.cbio.CnaRecord;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.ItemStreamReader;
import java.util.*;
import org.cbio.gdcpipeline.model.ManifestFileData;
import org.cbio.gdcpipeline.util.CommonDataUtil;
import org.springframework.beans.factory.annotation.Value;
import java.io.File;
import java.io.FileReader;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 *
 * @author heinsz
 */
public class CnaReader implements ItemStreamReader<CnaRecord> {
    @Value("#{jobParameters[sourceDirectory]}")
    private String sourceDir;

    @Value("#{jobExecutionContext[gdcManifestData]}")
    private List<ManifestFileData> gdcManifestData;

    @Value("#{jobExecutionContext[gdcAliquotIdToSampleId]}")
    private Map<String, String> gdcAliquotIdToSampleId;

    private List<CnaRecord> cnaRecords = new ArrayList<>();
    private Set<String> samplesSeen = new HashSet<>();

    private static Log LOG = LogFactory.getLog(CnaReader.class);

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        for (ManifestFileData fileData : gdcManifestData) {
            if (CommonDataUtil.GDC_TYPE.CNA.toString().equalsIgnoreCase(fileData.getDatatype().replace(" ", "_"))) {
                File cnaFile;
                LOG.info("Processing CNA file: " + fileData.getFilename());
                try {
                    Path path = Paths.get(sourceDir, fileData.getId(), fileData.getFilename());
                    cnaFile = CommonDataUtil.extractCompressedFile(path.toFile());
                }
                catch (Exception e) {
                    LOG.error("failed to extract file");
                    throw new ItemStreamException("Failed to process file");
                }

                try {
                    readFile(cnaFile, executionContext);
                }
                catch (Exception e){
                    LOG.error("Failed to read file");
                }

            };
        }
    }

    @Override
    public CnaRecord read() throws Exception {
        if (!cnaRecords.isEmpty()) {
            return cnaRecords.remove(0);
        }
        return null;
    }

    @Override
    public void update(ExecutionContext executionContext) throws ItemStreamException {}

    @Override
    public void close() throws ItemStreamException {}

    private void readFile(File cnaFile, ExecutionContext executionContext) throws Exception {
        BufferedReader br = new BufferedReader(new FileReader(cnaFile));
        String line;
        String header = br.readLine();
        List<String> headerList = new ArrayList<>(Arrays.asList(header.split("\t")));
        headerList.replaceAll(String::toUpperCase);

        // Keep these in order
        int geneIdIndex = headerList.indexOf("GENE ID");
        if (geneIdIndex != -1) {
            headerList.remove(geneIdIndex);
        }
        int geneSymbolIndex = headerList.indexOf("GENE SYMBOL");
        if (geneSymbolIndex != -1) {
            headerList.remove(geneSymbolIndex);
        }
        headerList.add(geneSymbolIndex, "Hugo_Symbol");
        int cytobandIndex = headerList.indexOf("CYTOBAND");
        if (cytobandIndex != -1) {
            headerList.remove(cytobandIndex);
        }

        List<Integer> indicesToSkip = new ArrayList<>();

        // Replace case ids with sample ids
        for (int i = 0; i < headerList.size(); i++) {
            if (gdcAliquotIdToSampleId.containsKey(headerList.get(i))) {
                String sid = gdcAliquotIdToSampleId.get(headerList.get(i));
                if (samplesSeen.contains(sid)) {
                    indicesToSkip.add(0,i);
                }
                headerList.set(i, sid);
                samplesSeen.add(sid);
            }
        }

        for (Integer indexToSkip : indicesToSkip) {
            headerList.remove(indexToSkip);
        }

        executionContext.put("cnaHeader", headerList);
        while ((line = br.readLine()) != null) {
            List<String> fields = new ArrayList<>(Arrays.asList(line.split("\t")));
            if (geneIdIndex != -1) {
                fields.remove(geneIdIndex);
            }
            if (cytobandIndex != -1) {
                fields.remove(cytobandIndex);
            }
            for (Integer indexToSkip : indicesToSkip) {
                fields.remove(indexToSkip);
            }
            // Assuming that only ensembl id is present for the gene symbol
            cnaRecords.add(new CnaRecord(fields.get(0), fields.subList(1, fields.size())));
        }
    }
}
