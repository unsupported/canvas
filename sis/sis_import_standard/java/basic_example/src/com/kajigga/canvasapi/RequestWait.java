package com.kajigga.canvasapi;

public class RequestWait {
	
	public static void waitABit(int waitTime) {
		
		System.out.println("Waiting: " + waitTime);
		try {
			Thread.sleep(waitTime * 1000);
		} catch (InterruptedException e) {
		}
		System.out.println("Done waiting");
	}
}
