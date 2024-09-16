package org.cbio.gdcpipeline.processor;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.cbio.gdcpipeline.model.cbio.CnaRecord;
import org.cbio.gdcpipeline.util.GenomeNexusCache;
import org.springframework.batch.item.ItemProcessor;
import org.springframework.beans.factory.annotation.Autowired;

/**
 *
 * @author heinsz
 */
public class CnaProcessor implements ItemProcessor<CnaRecord,CnaRecord>{
    
    @Autowired
    private GenomeNexusCache genomeNexusCache;

    private static Log LOG = LogFactory.getLog(CnaProcessor.class);

    @Override
    public CnaRecord process(CnaRecord record) throws Exception {
        record.setHugoSymbol(genomeNexusCache.getHugoSymbolFromEnsembl(record.getEnsemblGeneId()));
        return record;
    }

}
