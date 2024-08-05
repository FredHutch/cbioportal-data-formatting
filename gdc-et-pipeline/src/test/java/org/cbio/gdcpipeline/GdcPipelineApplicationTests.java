package org.cbio.gdcpipeline;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.IntegrationTest;
import org.springframework.boot.test.SpringApplicationConfiguration;
import org.springframework.test.context.TestPropertySource;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@IntegrationTest
//@SpringApplicationConfiguration(classes={BatchConfiguration.class, TestConfiguration.class})
@TestPropertySource("classpath:application.properties")
public class GdcPipelineApplicationTests {

	@Test
	public void contextLoads() {
	}

}
