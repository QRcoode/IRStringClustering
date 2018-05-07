package weka;

import weka.core.*;
import weka.core.converters.*;
import weka.classifiers.trees.*;
import weka.filters.*;
import weka.filters.unsupervised.attribute.*;
import weka.core.converters.ConverterUtils.DataSource;

import java.io.*;

public class TextCategorizationTest {
	 /**
	   * Expects the first parameter to point to the directory with the text files.
	   * In that directory, each sub-directory represents a class and the text
	   * files in these sub-directories will be labeled as such.
	   *
	   * @param args        the commandline arguments
	   * @throws Exception  if something goes wrong
	   */
	  public static void main(String[] args) throws Exception {
	    // convert the directory into a dataset
//	    TextDirectoryLoader loader = new TextDirectoryLoader();
//	    loader.setDirectory(new File(args[0]));
//	    Instances dataRaw = loader.getDataSet();
	    //System.out.println("\n\nImported data:\n\n" + dataRaw);

	    // apply the StringToWordVector
	    // (see the source code of setOptions(String[]) method of the filter
	    // if you want to know which command-line option corresponds to which
	    // bean property)
	    String filename = "E:\\eclipse-workspace\\Wekastring\\file\\min.arff";
	    DataSource source = new DataSource(filename);
	    Instances instances = source.getDataSet();
	    
	    //System.out.println(instances);
	    

	    StringToWordVector filter = new StringToWordVector();
	    
	    filter.setInputFormat(instances);
	    
	    Instances dataFiltered = Filter.useFilter(instances, filter);
	    
	    
	    //System.out.println("\n\nFiltered data:\n\n" + dataFiltered.toString().split("@data")[1]);
	    
	    String data = dataFiltered.toString().split("@data")[1];
	    System.out.println(data);
//	    System.out.println("\n\nFiltered data num attr:\n\n" + dataFiltered.numAttributes());
//	    System.out.println("\n\nFiltered data num Instances:\n\n" + dataFiltered.numInstances());
//	    System.out.println("\n\nFiltered data numClasses:\n\n" + dataFiltered);

	    // train J48 and output model
//	    J48 classifier = new J48();
//	    classifier.buildClassifier(dataFiltered);
//	    System.out.println("\n\nClassifier model:\n\n" + classifier);
	  }
}
