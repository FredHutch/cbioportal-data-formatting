package org.cbio.gdcpipeline.reader;

import org.apache.commons.collections.map.MultiKeyMap;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.util.MutationDataFileUtils;
import org.cbioportal.annotator.Annotator;
import org.cbioportal.models.MutationRecord;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.ItemStreamReader;
import org.springframework.batch.item.file.FlatFileItemReader;
import org.springframework.batch.item.file.mapping.DefaultLineMapper;
import org.springframework.batch.item.file.mapping.FieldSetMapper;
import org.springframework.batch.item.file.transform.DelimitedLineTokenizer;
import org.springframework.batch.item.file.transform.FieldSet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;

import java.io.File;
import java.io.IOException;
import java.util.*;
import java.util.stream.Collectors;
import org.apache.commons.lang.StringUtils;

/**
 * @author Dixit Patel
 */
public class MutationReader implements ItemStreamReader<MutationRecord> {
    @Value("#{jobParameters[sourceDirectory]}")
    private String sourceDir;

    @Value("${mutation.data.file.prefix}")
    private String MUTATION_DATA_FILE_PREFIX;

    @Value("${mutation.default.merged.maf.file}")
    private String DEFAULT_MERGED_MAF_FILENAME;

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    @Value("#{jobParameters[separate_mafs]}")
    private String separate_mafs;

    @Autowired
    private Annotator annotator;

    private List<MutationRecord> mafRecords = new ArrayList<>();
    private static Log LOG = LogFactory.getLog(MutationReader.class);
    private Map<MutationRecord, Set<String>> seenMafRecord = new HashMap<>();
    private static String ADD_MAF_COLUMN_NAME = "Caller";

    @Override
    public MutationRecord read() throws Exception {
        if (!mafRecords.isEmpty()) {
            return mafRecords.remove(0);
        }
        return null;
    }

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        List<File> maf_files = (List<File>) executionContext.get("mafToProcess");
        if (maf_files == null || maf_files.isEmpty()) {
            throw new ItemStreamException("No MAF files to process");
        } else {
            for (File file : maf_files) {
                if (LOG.isInfoEnabled()) {
                    LOG.info("Processing MAF File : " + file.getAbsolutePath());
                }
                readFile(file);
            }
        }
        if (separate_mafs.equalsIgnoreCase("true")) {
            File output_file = new File(outputDir, MUTATION_DATA_FILE_PREFIX + maf_files.get(0).getName());
            executionContext.put("maf_file_to_write", output_file);
        } else {
            File MERGED_MAF_FILE_NAME = new File(outputDir, DEFAULT_MERGED_MAF_FILENAME);
            executionContext.put("maf_file_to_write", MERGED_MAF_FILE_NAME);
        }
        for (Map.Entry<MutationRecord, Set<String>> entry : seenMafRecord.entrySet()) {
            MutationRecord record = entry.getKey();
            Set<String> caller = entry.getValue();
            List<String> list = caller.stream().collect(Collectors.toList());
            record.getAdditionalProperties().put("Caller", StringUtils.join(list, '|'));
            mafRecords.add(record);
        }
    }

    private void readFile(File maf_file) {
        FlatFileItemReader<MutationRecord> reader = new FlatFileItemReader<>();
        DelimitedLineTokenizer tokenizer = new DelimitedLineTokenizer(DelimitedLineTokenizer.DELIMITER_TAB);
        MultiKeyMap mafFileMetadata = new MultiKeyMap();
        try {
            mafFileMetadata = MutationDataFileUtils.loadDataFileMetadata(maf_file);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String[] mafHeader = (String[]) mafFileMetadata.get(maf_file.getName(), "header");
        tokenizer.setNames(mafHeader);
        DefaultLineMapper<MutationRecord> lineMapper = new DefaultLineMapper<>();
        lineMapper.setLineTokenizer(tokenizer);
        lineMapper.setFieldSetMapper(mutationFieldSetMapper());
        reader.setResource(new FileSystemResource(maf_file));
        reader.setLineMapper(lineMapper);
        int metadataCount = (int) mafFileMetadata.get(maf_file.getName(), "metadataCount");
        //include the header row
        reader.setLinesToSkip(metadataCount + 1);
        reader.open(new ExecutionContext());
        try {
            MutationRecord record;
            while ((record = reader.read()) != null) {
                addRecord(record, maf_file.getName());
            }
        } catch (Exception e) {
            e.printStackTrace();
            throw new ItemStreamException("Error reading record");
        }
        reader.close();
    }

    private void addRecord(MutationRecord newRecord, String maf_filename) {
        maf_filename = MutationDataFileUtils.getCallerName(maf_filename);
        if (seenMafRecord.isEmpty()) {
            Set<String> caller = new HashSet<>();
            caller.add(maf_filename);
            seenMafRecord.put(newRecord, caller);
        } else {
            Iterator<Map.Entry<MutationRecord, Set<String>>> iterator = seenMafRecord.entrySet().iterator();
            Map.Entry<MutationRecord, Set<String>> entry = iterator.next();
            while (iterator.hasNext() && !entry.getKey().equals(newRecord)) {
                entry = iterator.next();
            }
            if (!entry.getKey().equals(newRecord)) {
                Set<String> caller = new HashSet<>();
                caller.add(maf_filename);
                seenMafRecord.put(newRecord, caller);
            } else {
                entry.getValue().add(maf_filename);
            }
        }
    }

    private FieldSetMapper<MutationRecord> mutationFieldSetMapper() {
        return (FieldSetMapper<MutationRecord>) (FieldSet fs) -> {
            MutationRecord record = new MutationRecord();
            for (String header : record.getHeader()) {
                try {
                    record.getClass().getMethod("set" + header.toUpperCase(), String.class).invoke(record, fs.readString(header));
                } catch (Exception e) {
                    if (LOG.isDebugEnabled()) {
                        LOG.error(" Error in setting record for :" + header);
                    }
                    e.printStackTrace();
                }
            }
            return record;
        };
    }

    @Override
    public void update(ExecutionContext executionContext) throws ItemStreamException {
    }

    @Override
    public void close() throws ItemStreamException {
    }
}
