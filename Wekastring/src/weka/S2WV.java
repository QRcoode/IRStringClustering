package weka;

import weka.core.*;
import weka.core.converters.*;
import weka.classifiers.trees.*;
import weka.clusterers.DBSCAN;
import weka.filters.*;
import weka.filters.unsupervised.attribute.*;
import weka.core.converters.ConverterUtils.DataSource;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

import java.io.*;

public class S2WV {
	 /**
	   * Expects the first parameter to point to the directory with the text files.
	   * In that directory, each sub-directory represents a class and the text
	   * files in these sub-directories will be labeled as such.
	   *
	   * @param args        the commandline arguments
	   * @throws Exception  if something goes wrong
	   */
	  public static void main(String[] args) throws Exception {
	    String filename = "E:\\Uni\\787\\IRStringClustering\\Wekastring\\files\\merged_issues_reviews.arff";
	    DataSource source = new DataSource(filename);
	    Instances instances = source.getDataSet();

	    StringToWordVector filter = new StringToWordVector();
	    
	    
	    
	    filter.setInputFormat(instances);
	    
	    Instances dataFiltered = Filter.useFilter(instances, filter);
	    
	    
		System.out.println("\n\nFiltered data numClasses:\n\n" + dataFiltered);
		
		//
		System.out.println("numInstances: " + dataFiltered.numInstances());
		
		//========== create CSV =========
		PrintWriter pw = new PrintWriter(new File("E:\\Uni\\787\\IRStringClustering\\files\\vectors.csv"));
		StringBuilder sb = new StringBuilder();
		

		

		
		
	    int numOfAttribute = dataFiltered.numAttributes();
	    
	    System.out.println("numOfAttribute: " + numOfAttribute);
	    
	    System.out.println();
	    
	    for(int i = 0; i < dataFiltered.numInstances(); i++)
	    {
	    	Instance singleData = dataFiltered.instance(i);
	    	
	    	//System.out.println("singleData: " + singleData);
	    	
	    	for(int k = 0 ; k < numOfAttribute; k++)
	    	{
	    		sb.append(singleData.value(k));
	    		sb.append(',');
	    	}
	    	sb.append('\n');
	    	
	    }
		pw.write(sb.toString());
		pw.close();
		System.out.println("done!");
	    
	  }
}
