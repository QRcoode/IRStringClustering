package weka;


import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import weka.classifiers.Classifier;
import weka.classifiers.bayes.NaiveBayes;
import weka.classifiers.trees.J48;
import weka.core.Attribute;
import weka.core.FastVector;
import weka.core.Instance;
import weka.core.Instances;
import weka.core.Utils;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.StringToWordVector;

public class MessageClassify implements Serializable 
{
	private Instances instances = null;	
	private StringToWordVector filter = new StringToWordVector();
	private Classifier classifier = new NaiveBayes();
	
	/**
	 * �������������Ҫ��ʱ�����ݸ�ʽ����꣬�����Ŀ�Ƚ���˵��
	 */
	public MessageClassify() throws Exception
	{
		String nameOfDataset = "MessageClassification";		
		FastVector attributes = new FastVector(2);
		attributes.addElement(new Attribute("Message", (FastVector) null));
		FastVector classValues = new FastVector(2);//�����������������
		classValues.addElement("alt.atheism");
		classValues.addElement("comp.graphics");
		attributes.addElement(new Attribute("Class", classValues));				
		instances = new Instances(nameOfDataset, attributes, 100);//���԰�instance��Ϊ���У�attribute��Ϊ����
		instances.setClassIndex(instances.numAttributes() - 1);//�����instance�е�����
	}

	/**
	 * ������ݵ�ѵ������
	 */
	public void updateData(String message, String classValue) throws Exception
	{
		Instance instance = makeInstance(message, instances);
		instance.setClassValue(classValue);
		instances.add(instance);	
	}
	
	/**
	 * �ı�����Ҫ�ر�һ�㣬��Ϊ��ʹ��StringToWordVector��������ı��д���(attribute)Ȩ�ص�ʱ����Ҫ�õ�ȫ�ֱ���������DF������������Ҫ��������
	 * ��weka��Ҫע����Щ����ѧϰ�㷨����������Щ����
	 */
	public void finishBatch() throws Exception
	{
		filter.setInputFormat(instances);
		Instances filteredData = Filter.useFilter(instances, filter);//���������������weka�㷨�����ʽ�����ݼ�
		classifier.buildClassifier(filteredData);//������ѵ��������
	}
	
	/**
	 * �������
	 */
	public void classifyMessage(String message) throws Exception
	{			
		filter.input(makeInstance(message, instances.stringFreeStructure()));
		Instance filteredInstance = filter.output();//����ʹ��ԭ����filter
		
		double predicted = classifier.classifyInstance(filteredInstance);//(int)predicted���������
		System.out.println("Message classified as : "
				+ instances.classAttribute().value((int) predicted));
	}

	
	private Instance makeInstance(String text, Instances data)
	{		
		Instance instance = new Instance(2);		
		Attribute messageAtt = data.attribute("Message");		
		instance.setValue(messageAtt, messageAtt.addStringValue(text));		
		instance.setDataset(data);
		return instance;
	}

	public static String getStringFromFile(File file)
	{
		StringBuilder sb=new StringBuilder();
		try
		{
			BufferedReader br=new BufferedReader(new FileReader(file));
			String line;
			while(true)
			{				
				if((line=br.readLine())==null) break;
				sb.append(line.trim());
			}		
			br.close();
		} catch (Exception e){}
		return sb.toString();
	}
	
	
	static String modelname="weka.message";	
	public static void main(String[] options)
	{
		try
		{
			MessageClassify messageCl=null;
			if(new File(modelname).exists())
				messageCl=loadModel(modelname);
			else
			{
				messageCl=trainModel();
				try
				{
					ObjectOutputStream modelOutObjectFile = new ObjectOutputStream(new FileOutputStream(modelname));
					modelOutObjectFile.writeObject(messageCl);
					modelOutObjectFile.close();
				} catch (Exception e){}
			}
			String testPath="E:/datasets/54262";
			messageCl.classifyMessage(getStringFromFile(new File(testPath)));		
		} 
		catch (Exception e){}
	}

	/**
	 * ѵ��������
	 */
	private static MessageClassify trainModel()
	{
		MessageClassify mc=null;
		try
		{
			mc = new MessageClassify();			
			String basePath="E:/datasets/20_newsgroups_two_class/train";
			File base=new File(basePath);
			for(File dir : base.listFiles())
			{
				for(File file : dir.listFiles())
				{
					String message=getStringFromFile(file);
					String classValue=dir.getName();
					mc.updateData(message, classValue);//���һ��ѵ��������classvalue�������
				}				
			}
			mc.finishBatch();//ѵ������
			
		} catch (Exception e){}
		return mc;
	}

	public static MessageClassify loadModel(String modelname)
	{
		MessageClassify mc=null;
		try
		{
			ObjectInputStream modelInObjectFile =new ObjectInputStream(new FileInputStream(modelname));
			mc = (MessageClassify) modelInObjectFile.readObject();
			modelInObjectFile.close();
		}
		catch (Exception e){}
		return mc;		
	}
}