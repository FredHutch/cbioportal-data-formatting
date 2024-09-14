package org.cbio.gdcpipeline.util;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.commons.lang.StringUtils;

import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * @author Dixit Patel
 */
public class MetaFileWriter {
    private static String metadata;
    private static Log LOG = LogFactory.getLog(MetaFileWriter.class);

    public static void makeMetadata(Map<String, String> fields) {
        if (!fields.isEmpty()) {
            List<String> data = new ArrayList<>();
            for (Map.Entry<String, String> entry : fields.entrySet()) {
                data.add(entry.getKey() + ": " + entry.getValue());
            }
            metadata = StringUtils.join(data, '\n');
        }
    }

    public static void writeMetadata(Map<String, String> fields, String file_path) throws Exception {
        makeMetadata(fields);
        File filename = new File(file_path);
        if (metadata.isEmpty()) {
            if (LOG.isErrorEnabled()) {
                LOG.error("Metadata is empty. Nothing to write");
            }
            throw new Exception();
        }
        try (Writer writer = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(filename), "utf-8"))) {
            writer.write(metadata);
        }
    }
}
