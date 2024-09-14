package org.cbio.gdcpipeline.writer;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.util.ArrayList;
import java.util.List;
import org.apache.commons.lang.StringUtils;
import org.cbio.gdcpipeline.model.cbio.CnaRecord;
import org.springframework.batch.item.ExecutionContext;
import org.springframework.batch.item.ItemStreamException;
import org.springframework.batch.item.ItemStreamWriter;
import org.springframework.batch.item.file.FlatFileHeaderCallback;
import org.springframework.batch.item.file.FlatFileItemWriter;
import org.springframework.batch.item.file.transform.PassThroughLineAggregator;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;

/**
 *
 * @author heinsz
 */
public class CnaWriter  implements ItemStreamWriter<CnaRecord> {

    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    @Value("${cna.data.file}")
    private String cnaFile;

    private ExecutionContext executionContext;

    private FlatFileItemWriter<String> flatFileItemWriter = new FlatFileItemWriter<>();

    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        this.executionContext = executionContext;
        File outputFile = new File(outputDir, cnaFile);
        List<String> header = (List<String>) executionContext.get("cnaHeader");
        PassThroughLineAggregator aggr = new PassThroughLineAggregator();
        flatFileItemWriter.setLineAggregator(aggr);
        flatFileItemWriter.setHeaderCallback(new FlatFileHeaderCallback() {
            @Override
            public void writeHeader(Writer writer) throws IOException {
                writer.write(StringUtils.join(header, "\t"));
            }
        });
        flatFileItemWriter.setResource(new FileSystemResource(outputFile));
        flatFileItemWriter.open(executionContext);
    }

    @Override
    public void update(ExecutionContext executionContext) throws ItemStreamException {}

    @Override
    public void close() throws ItemStreamException {}

    @Override
    public void write(List<? extends CnaRecord> cnaRecords) throws Exception {
        List<String> writeList = new ArrayList<>();
        for (CnaRecord record : cnaRecords) {
            String recordString = record.getHugoSymbol() + "\t" + record.getTabDelimData();
            writeList.add(recordString);
        }
        flatFileItemWriter.write(writeList);
    }

}
