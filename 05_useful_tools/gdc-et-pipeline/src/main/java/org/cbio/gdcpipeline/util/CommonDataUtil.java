package org.cbio.gdcpipeline.util;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.rest.response.Hits;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;
import java.util.zip.GZIPInputStream;

/**
 * @author Dixit Patel
 */
public class CommonDataUtil {
    public static final String NORMAL_SAMPLE_SUFFIX = "10";
    private static Log LOG = LogFactory.getLog(CommonDataUtil.class);
    public enum CLINICAL_TYPE{PATIENT,SAMPLE}
    private static String SYSTEM_TMP_DIR_PROPERTY = "java.io.tmpdir";
    private static String TMP_DIR_NAME = "gdcpipeline";
    private static File temp_dir;
    private static List<String> missingValueList = initMissingValueList();

    private static List<String> initMissingValueList() {
        List<String> missingValueList = new ArrayList<>();
        missingValueList.add("NA");
        missingValueList.add("N/A");
        missingValueList.add("N/a");
        missingValueList.add("n/A");
        missingValueList.add("Unknown");
        missingValueList.add("not available");
        return missingValueList;
    }

    public static boolean hasMissingKeys(String check) {
        for (String ignore : missingValueList) {
            if (check.equalsIgnoreCase(ignore)) {
                return true;
            }
        }
        return false;
    }

    public enum CLINICAL_OS_STATUS {LIVING, DECEASED}

    public enum GDC_DATAFORMAT {
        BCR_XML("BCR XML"),
        MAF("MAF");

        private final String format;

        GDC_DATAFORMAT(String format) {
            this.format = format;
        }

        @Override
        public String toString() {
            return this.format;
        }
    }

    public enum GDC_TYPE {
        BIOSPECIMEN("biospecimen_supplement"),
        CLINICAL("clinical_supplement"),
        MUTATION("masked_somatic_mutation"),
        CNA("gene_level_copy_number_scores"),
        EXPRESSION("gene_expression_quantification");

        private final String type;  

        GDC_TYPE(String type){
            this.type=type;
        }

        @Override
        public String toString() {
            return this.type;
        }
    }

    public enum REFERENCE_GENOME {
        GRCh37("GRCh37"),
        HG19("hg19");

        public  static Set<String> build37 = new HashSet<>(Arrays.asList(GRCh37.toString(),HG19.toString()));
        private final String ref;

        REFERENCE_GENOME(String ref){
            this.ref=ref;
        }

        @Override
        public String toString(){
            return this.ref;
        }
    }


    public enum COMPRESSION_FORMAT {
        GZIP(".gz");
        private final String format;

        COMPRESSION_FORMAT(String format) {
            this.format = format;
        }

        @Override
        public String toString() {
            return this.format;
        }
    }

    public static List<File> extractCompressedFiles(List<File> fileList) throws Exception {
        temp_dir = createTempDirectory();
        List<File> extracted = new ArrayList<>();
        if (!fileList.isEmpty()) {
            for (File extractFile : fileList) {
                extracted.add(extractCompressedFile(extractFile));
            }
        }
        return extracted;
    }
    
    public static File extractCompressedFile(File extractFile) throws Exception {
        temp_dir = createTempDirectory();
        if (isCompressedFile(extractFile)) {
            File tmp_file;
            try {
                tmp_file = File.createTempFile(extractFile.getName(), "", temp_dir);
            } catch (IOException e) {
                e.printStackTrace();
                if (LOG.isErrorEnabled()) {
                    LOG.error("Error creating temp file in : " + temp_dir.getAbsolutePath() + "\nSkipping File");
                }
                return extractFile;
            }
            try {
                FileOutputStream fos = new FileOutputStream(tmp_file);
                FileInputStream fis = new FileInputStream(extractFile);
                if (extractFile.getName().endsWith(COMPRESSION_FORMAT.GZIP.toString())) {
                    GZIPInputStream gzip = new GZIPInputStream(fis);
                    byte[] buffer = new byte[1024];
                    int readByte;
                    while ((readByte = gzip.read(buffer)) > 0) {
                        fos.write(buffer, 0, readByte);
                    }   
                    gzip.close();
                    Path path = Files.move(Paths.get(tmp_file.getAbsolutePath()), Paths.get(temp_dir.getAbsolutePath(), extractFile.getName().replace(COMPRESSION_FORMAT.GZIP.toString(), "")));
                    return new File(path.toUri());
                }
                fos.close();
            } catch (Exception e) {
                e.printStackTrace();
                deleteTempDir();
                throw new Exception("Error while decompressing files");                
            }
        }
        return extractFile;   
    }

    private static boolean isCompressedFile(File extractFile) {
        return extractFile.getName().endsWith(COMPRESSION_FORMAT.GZIP.toString());
    }

    public static void deleteTempDir() {
        if (temp_dir != null && temp_dir.exists()) {
            try {
                deleteDir(temp_dir);
            } catch (Exception e) {
                if (LOG.isWarnEnabled()) {
                    LOG.warn(" Temp directory could not be deleted : " + temp_dir.getAbsolutePath());
                }
                e.printStackTrace();
            }
        }
    }

    private static File createTempDirectory() throws Exception {
        File tmp_dir = new File(System.getProperty(SYSTEM_TMP_DIR_PROPERTY), TMP_DIR_NAME);
        if (tmp_dir.exists()) {
            if (LOG.isErrorEnabled()) {
                LOG.error("Temp directory already exists. Deleting directory and its contents :" + tmp_dir.getAbsolutePath());
            }
            deleteDir(tmp_dir);
        }
            tmp_dir.mkdir();
        return tmp_dir;
    }

    private static void deleteDir(File dir) throws Exception {
        File[] entries = dir.listFiles();
        if (entries != null) {
            for (File entry : entries) {
                deleteDir(entry);
            }
        }
        dir.delete();
    }
}
