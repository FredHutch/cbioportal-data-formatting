package org.cbio.gdcpipeline.writer;

import java.io.File;
import java.io.IOException;
import java.io.Writer;
import java.util.List;
import org.apache.commons.lang.StringUtils;
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
public class ExpressionWriter implements ItemStreamWriter<String>{
    @Value("#{jobParameters[outputDirectory]}")
    private String outputDir;

    @Value("${expression.data.file}")
    private String expressionFile;       
    
    private FlatFileItemWriter<String> flatFileItemWriter = new FlatFileItemWriter<>();
    
    @Override
    public void open(ExecutionContext executionContext) throws ItemStreamException {
        File outputFile = new File(outputDir, expressionFile);
        List<String> header = (List<String>) executionContext.get("expressionHeader");
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
    public void update(ExecutionContext arg0) throws ItemStreamException {}

    @Override
    public void close() throws ItemStreamException {}

    @Override
    public void write(List<? extends String> expressionRecords) throws Exception {
        flatFileItemWriter.write(expressionRecords);
    }
    
}
