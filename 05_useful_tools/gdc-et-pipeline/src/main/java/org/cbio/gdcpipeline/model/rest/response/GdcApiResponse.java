package org.cbio.gdcpipeline.model.rest.response;

/**
 * @author Dixit Patel
 */

public class GdcApiResponse {
    private Data data;
    private Warning warnings;

    public Data getData() {
        return data;
    }

    public void setData(Data data) {
        this.data = data;
    }

    public Warning getWarnings() {
        return warnings;
    }

    public void setWarnings(Warning warnings) {
        this.warnings = warnings;
    }
}
