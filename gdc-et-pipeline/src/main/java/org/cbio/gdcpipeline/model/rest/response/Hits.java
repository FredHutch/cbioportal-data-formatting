package org.cbio.gdcpipeline.model.rest.response;

import java.util.List;

/**
 * @author Dixit Patel
 */
public class Hits{
    private String file_id;
    private String file_name;
    private List<Case> cases;
    private String type;
    private String data_format;

    public Hits(){}

    public String getFile_id() {
        return file_id;
    }

    public void setFile_id(String file_id) {
        this.file_id = file_id;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getData_format() {
        return data_format;
    }

    public void setData_format(String data_format) {
        this.data_format = data_format;
    }

    public String getFile_name() {
        return file_name;
    }

    public void setFile_name(String file_name) {
        this.file_name = file_name;
    }

    public List<Case> getCases() {
        return cases;
    }

    public void setCases(List<Case> cases) {
        this.cases = cases;
    }
}
