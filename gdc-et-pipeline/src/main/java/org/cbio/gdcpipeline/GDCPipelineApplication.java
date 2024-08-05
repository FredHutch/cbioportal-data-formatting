package org.cbio.gdcpipeline;

import org.apache.commons.cli.*;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.util.CommonDataUtil;

import org.springframework.batch.core.Job;
import org.springframework.batch.core.JobExecution;
import org.springframework.batch.core.JobParameters;
import org.springframework.batch.core.JobParametersBuilder;
import org.springframework.batch.core.launch.JobLauncher;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * @author Dixit Patel
 */
@SpringBootApplication
public class GDCPipelineApplication {
    private static Log LOG = LogFactory.getLog(GDCPipelineApplication.class);
    private final static String GDC_JOB = "gdcJob";
    private final static String DEFAULT_DATATYPES = "ALL";
    private final static String DEFAULT_FILTER_NORMAL_SAMPLE = "true";
    private final static String DEFAULT_SEPARATE_MAF_FILES = "false";
    private final static String DEFAULT_ISOFORM_OVERRIDE_SOURCE = "uniprot";
    private final static String DEFAULT_REFERENCE_GENOME_BUILD = CommonDataUtil.REFERENCE_GENOME.GRCh37.toString();

    private static Options getOptions(String[] input) {
        Options options = new Options();
        options.addOption("s", "source", true, "source directory for files");
        options.addOption("o", "output", true, "output directory for files");
        options.addOption("c", "cancer_study_id", true, "Cancer Study Id");
        options.addOption("m", "manifest_file", true, "Manifest file path");
        options.addOption("f", "filter_normal_sample", true, "True or False. Flag to filter normal samples. Default is True ");
        options.addOption("d", "datatypes", true, "Datatypes to run. Default is All");
        options.addOption("separate_mafs", "separate_mafs", true, "True or False. Process MAF files individually or merge together. Default is False");
        options.addOption("i", "isoformOverrideSource", true, "Isoform Override Source. Default is \'uniprot\'");
        options.addOption("r", "reference_genome_build", true, "Reference Genome to use for processing MAF. Default is GRCh37");
        options.addOption("h", "help", false, "shows this help document and quits.");
        return options;
    }

    private static void help(Options gnuOptions, int exitStatus, String opt) {
        HelpFormatter helpFormatter = new HelpFormatter();
        if (!opt.isEmpty()) {
            System.out.println(opt);
        }
        helpFormatter.printHelp(" Pipeline Options ", gnuOptions);
        System.exit(exitStatus);
    }

    private static void launchJob(String[] args, String sourceDirectory, String outputDirectory, String cancer_study_id, String manifest_file, String filter_normal_sample, String datatypes, String separate_mafs,String isoformOverrideSource,String reference_genome_build) throws Exception {
        SpringApplication app = new SpringApplication(GDCPipelineApplication.class);
        ConfigurableApplicationContext ctx = app.run(args);
        Job gdcJob = ctx.getBean(GDC_JOB, Job.class);
        JobLauncher jobLauncher = ctx.getBean(JobLauncher.class);
        JobParameters jobParameters = new JobParametersBuilder()
                .addString("sourceDirectory", sourceDirectory)
                .addString("outputDirectory", outputDirectory)
                .addString("cancer_study_id", cancer_study_id)
                .addString("manifest_file", manifest_file)
                .addString("filter_normal_sample", filter_normal_sample)
                .addString("datatypes", datatypes)
                .addString("separate_mafs", separate_mafs)
                .addString("isoformOverrideSource",isoformOverrideSource)
                .addString("reference_genome_build",reference_genome_build)
                .toJobParameters();
        JobExecution jobExecution = jobLauncher.run(gdcJob, jobParameters);
    }

    public static void main(String[] args) throws Exception {
        Options options = GDCPipelineApplication.getOptions(args);
        CommandLineParser parser = new DefaultParser();
        CommandLine cli = parser.parse(options, args);
        if (cli.hasOption("help")) {
            GDCPipelineApplication.help(options, 0, "");
        }
        if (!cli.hasOption("source")) {
            GDCPipelineApplication.help(options, 0, "Source directory of files must be specified");
        }
        if (!cli.hasOption("output")) {
            GDCPipelineApplication.help(options, 0, "Output directory for files must be specified");
        }
        if (!cli.hasOption("manifest_file")) {
            GDCPipelineApplication.help(options, 0, "Manifest file path must be specified");
        }
        String datatypes = DEFAULT_DATATYPES;
        if (cli.hasOption("datatypes")) {
            datatypes = cli.getOptionValue("datatypes");
        }

        String filter_normal_sample = DEFAULT_FILTER_NORMAL_SAMPLE;
        if (cli.hasOption("filter_normal_sample")) {
            if (cli.getOptionValue("filter_normal_sample").toLowerCase().equals("false")) {
                filter_normal_sample = "false";
            } else if (!cli.getOptionValue("filter_normal_sample").toLowerCase().equals("true")) {
                GDCPipelineApplication.help(options, 0, "Filter Option must either be True or False");
            }
        }

        String separate_mafs = DEFAULT_SEPARATE_MAF_FILES;
        if (cli.hasOption("separate_mafs")) {
            if (cli.getOptionValue("separate_mafs").toLowerCase().equals("true")) {
                separate_mafs = "true";
            } else if (!cli.getOptionValue("separate_mafs").toLowerCase().equals("false")) {
                GDCPipelineApplication.help(options, 0, "MAF File Option must either be True or False");
            }
        }

        String isoformOverrideSource = DEFAULT_ISOFORM_OVERRIDE_SOURCE;
        if (cli.hasOption("isoformOverrideSource")) {
            isoformOverrideSource = cli.getOptionValue("isoformOverrideSource");
        }

        String reference_genome_build = DEFAULT_REFERENCE_GENOME_BUILD;
        if(cli.hasOption("reference_genome_build")){
            reference_genome_build = cli.getOptionValue("reference_genome_build");
            if(!(CommonDataUtil.REFERENCE_GENOME.build37.contains(reference_genome_build))){
                GDCPipelineApplication.help(options, 0, reference_genome_build+" reference genome build is not currently supported.");
            }
        }

        launchJob(args, cli.getOptionValue("source"), cli.getOptionValue("output"), cli.getOptionValue("cancer_study_id"), cli.getOptionValue("manifest_file"), filter_normal_sample, datatypes, separate_mafs,isoformOverrideSource,reference_genome_build);
    }
}
