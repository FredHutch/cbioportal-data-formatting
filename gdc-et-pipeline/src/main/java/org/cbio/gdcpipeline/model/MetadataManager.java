package org.cbio.gdcpipeline.model;

import java.util.List;
import java.util.Map;

/**
 * @author Dixit Patel
 */
public interface MetadataManager {
    Map<String, List<String>> getFullHeader(List<String> header);
}
