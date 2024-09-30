package org.cbio.gdcpipeline.model.cbio;

import java.util.List;
import java.util.Map;

/**
 * @author Dixit Patel
 */

public abstract class ClinicalDataModel {
    public abstract List<String> getFields();
    public abstract Map<String, List<String>> getHeaders();
}
