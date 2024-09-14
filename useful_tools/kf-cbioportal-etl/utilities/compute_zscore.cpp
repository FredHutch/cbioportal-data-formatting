//compute_zscore.cpp
#include <Rcpp.h>
#include <fstream>
#include <thread>
#include <unistd.h>

using namespace Rcpp;

//Just declaration of functions similar to header file
NumericMatrix compute_write_zscore(NumericMatrix num, int no_threads) ;
void write_file(NumericMatrix num,std::string output_file_name);
void compute_zscore_row(NumericMatrix::Row row);

/**
 * @brief this function will write files in tsv format with column and row header
 * @param num Matrix to write into a tsv file
 * @param output_file_name name of the output file as a string 
 * @return none but a tsv format file in the current folder
*/
// [[Rcpp::export]]
void write_file(NumericMatrix num,std::string output_file_name) 
{
    //Rcout<<"Writing z-scores using C++ Implementation"<<"\n";
    std::ofstream myfile;
    myfile.open(output_file_name);
    CharacterVector column_names = colnames(num);
    CharacterVector row_names = rownames(num);

    myfile <<"Hugo_Symbol"<<"\t";
    for(auto p = column_names.begin(); p != column_names.end()-1; ++p){
          myfile << *p<<"\t";
      }
      myfile << *(column_names.end()-1); //do not add tab at the end of row
    myfile <<"\n";
    
    for(size_t i = 0; i < num.nrow();++i){
        myfile << row_names(i)<<"\t";
        for(size_t j = 0; j < num.ncol()-1;++j ){
            myfile << num(i,j)<<"\t";
          }
          myfile << num(i,num.ncol()-1); //do not add tab at the end of row
        myfile <<"\n"; //change of line
      }
    myfile.close();  // close the file
}

/**
 * @brief This function computes zscore for a single row
 * @param row A reference to row elements to compute zscore on them
 * @return none replaces a row within the num matrix with z-score 
*/
void compute_zscore_row(NumericMatrix::Row row)
{
    float mean =0.0;
    float sd = 0.0;
    float var = 0.0;
    int row_size=row.size();
    for (auto i = row.begin(); i != row.end(); ++i) // compute mean
    { 
        if ( *i != 0)
              *i = std::log2(*i+1);
        mean=mean + *i ;      
    }
    mean=mean/row_size;
    for (auto i = row.begin(); i != row.end(); ++i) //compute SD
    { 
          var=var+ ((*i-mean) * (*i-mean));
    }
    sd=std::sqrt(var/(row_size-1));  
    int round_off = 10000;
    float a;
    for(auto i = row.begin(); i != row.end(); ++i) //compute zscore
    {
          a = std::ceil((*i - mean)*round_off/sd) ;
          *i=a/round_off;
    }  
}

/**
 * @brief function to compute zscore and replace num matrix with it's zscores
 * @param num matrix that requires 
 * @param no_threads Number of threads to use for computing z score. Default is 1
 * @return num matrix with zscores
*/
// [[Rcpp::export]]
NumericMatrix compute_write_zscore(NumericMatrix num, int no_threads =1) 
{
    std::vector<std::thread*> threads;
    Rcout<<"Utilizing "<<no_threads<<" threads to compute zscore"<<"\n";
    for(int i = 0; i < num.nrow();i+=no_threads)
      {
        if (i>num.nrow()-no_threads) //check for last rows i.e corner case
          {
            for (size_t j=i; j<num.nrow();j++)
              {
              compute_zscore_row(num( j , _ ));
              }
          break;
          }
        for(int jj = 0; jj < no_threads; ++jj) //fire threads
        {
          threads.push_back(new std::thread(compute_zscore_row,num(i+jj, _ )));
            //  Rcout <<i+jj<<"\n";
        }
        for(int jj = 0; jj < no_threads; ++jj) // join threads and clean heap
        {
          threads.at(jj) -> join();
          delete threads.at(jj);
        }     
        threads.clear(); //clear the vector
      }
    //NumericMatrix::Row  col = num( 0 , _ );
    //for (auto i = col.begin(); i != col.end(); ++i)
    //     Rcout << *i << "\n";

    //write_file(num,"written.tsv"); //write the num matrix to tsv format
    return num; //return matrix with zscores in it
}