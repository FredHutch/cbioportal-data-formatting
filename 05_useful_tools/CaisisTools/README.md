# CaisisTools
Tools to transform Caisis data into cBioPortal format, including extensions specific to Oncoscape V3.

[Caisis](http://www.caisis.org/) is a clinical database system. [Oncoscape](https://github.com/FredHutch/OncoscapeV3#readme) is a visualization and hypothesis generation tool developed at Fred Hutchinson Cancer Research Center. The [cBioPortal](http://www.cbioportal.org/) project has produced a set of file formats for transporting molecular data (primarily) and clinical data (secondarily), and Oncoscape uses that format for importing data. This project takes an export from Caisis, in the form of an Excel workbook, and transform it into cBioPortal-compatible tab-separated (TSV) files that Oncoscape can then readily import. In addition, it adds some decoration with Oncoscape extensions to the cBioPortal format.


