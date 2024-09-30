package org.cbio.gdcpipeline.tasklet;

import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.ManifestFileData;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.powermock.api.mockito.PowerMockito;
import org.powermock.core.classloader.annotations.PrepareForTest;
import org.powermock.modules.junit4.PowerMockRunner;
import org.springframework.batch.core.StepContribution;
import org.springframework.batch.core.scope.context.ChunkContext;
import org.springframework.http.*;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.powermock.api.mockito.PowerMockito.when;

/**
 * @author Dixit Patel
 */

@PrepareForTest({ProcessManifestFileTasklet.class, LogFactory.class})
@RunWith(PowerMockRunner.class)
public class ProcessManifestFileTaskletTest {
    File sourceDir;
    String cancerStudyId;
    String GDC_API_FILES_ENDPOINT;
    int MAX_RESPONSE_SIZE;
    @Mock
    StepContribution stepContext;
    @Mock
    ChunkContext chunkContext;
    @Mock
    RestTemplate restTemplate;

    private ProcessManifestFileTasklet tasklet;

    @Before
    public void setUp() throws Exception {
        MockitoAnnotations.initMocks(this);
        setProperties();
        tasklet = new ProcessManifestFileTasklet();
    }

    public void setProperties() throws Exception {
        ClassLoader classLoader = getClass().getClassLoader();
        Properties p = new Properties();
        File file = new File(classLoader.getResource("data").getFile());
        sourceDir = new File(file.getAbsolutePath() + File.separator + "GDC");
        p.load(new FileReader(new File(classLoader.getResource("application.properties").getFile())));
        cancerStudyId = p.getProperty("test.cancer.study.id");
        GDC_API_FILES_ENDPOINT = p.getProperty("gdc.api.files.endpoint");
        MAX_RESPONSE_SIZE = Integer.parseInt(p.getProperty("gdc.max.response.size"));
    }


    @Test(expected = java.lang.Exception.class)
    public void testExecuteEmptyBiospecimenFileList() throws Exception {
        ReflectionTestUtils.setField(tasklet, "sourceDir", sourceDir.getAbsolutePath());
        ReflectionTestUtils.setField(tasklet, "cancer_study_id", cancerStudyId);
        File empty = new File(sourceDir.getAbsolutePath());
        PowerMockito.whenNew(File.class).withAnyArguments().thenReturn(empty);
        tasklet.execute(stepContext, chunkContext);
    }

    // TODO: Make this call out to the graphql endpoint instead of the rest
//    @Test(expected = java.lang.Exception.class)
//    public void testCallGdcApiServiceUnavailable() throws Exception {
//        ReflectionTestUtils.setField(tasklet, "GDC_API_FILES_ENDPOINT", GDC_API_FILES_ENDPOINT);
//        ReflectionTestUtils.setField(tasklet, "MAX_RESPONSE_SIZE", MAX_RESPONSE_SIZE);
//        ManifestFileData temp = new ManifestFileData();
//        temp.setId("sample_file_id");
//        List<ManifestFileData> manifestFileList = new ArrayList<>();
//        manifestFileList.add(temp);
//        ReflectionTestUtils.setField(tasklet, "manifestFileList", manifestFileList);
//        ResponseEntity<String> response = new ResponseEntity<String>(HttpStatus.INTERNAL_SERVER_ERROR);
//        RestTemplate restTemplate = mock(RestTemplate.class);
//        ReflectionTestUtils.setField(tasklet, "restTemplate", restTemplate);
//        HttpHeaders httpHeaders = new HttpHeaders();
//        httpHeaders.setContentType(MediaType.APPLICATION_JSON);
//        HttpEntity<String> entity = new HttpEntity<String>("", httpHeaders);
//        when(restTemplate.exchange(GDC_API_FILES_ENDPOINT, HttpMethod.POST, entity, String.class)).thenReturn(response);
//        //tasklet.callGdcApi(GDC_API_FILES_ENDPOINT, "");
//    }

    @Test
    public void testBuildJsonRequestReturnsValidJson() {
        ManifestFileData temp = new ManifestFileData();
        temp.setId("sample_file_id");
        List<ManifestFileData> manifestFileList = new ArrayList<>();
        manifestFileList.add(temp);
        ReflectionTestUtils.setField(tasklet, "manifestFileList", manifestFileList);
        String expectedPayload = "{\"filters\":{\"op\":\"in\",\"content\":{\"field\":\"file_id\",\"value\":[\"sample_file_id\"]}}," +
                "\"format\":\"JSON\",\"fields\":\"file_id,file_name,cases.case_id,type,data_format\"}";
        //String actualPayload = tasklet.buildJsonRequest();
        //assertEquals(expectedPayload, actualPayload);
    }
}
