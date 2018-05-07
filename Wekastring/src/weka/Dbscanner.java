package weka;

import weka.clusterers.DBSCAN;
import weka.core.Instances;

public class Dbscanner {


	
	public void doDBSCAN(Instances data)
	{
		DBSCAN dbscan = new DBSCAN();
		dbscan.setEpsilon(0.12);
		dbscan.setMinPoints(5);
		try {
			dbscan.buildClusterer(data);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
