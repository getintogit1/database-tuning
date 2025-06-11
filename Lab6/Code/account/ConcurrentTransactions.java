/*
 * Example code for Assignment 6 (concurrency tuning) of the course:
 * 
 * Database Tuning
 * Department of Computer Science
 * University of Salzburg, Austria
 * 
 * Lecturer: Nikolaus Augsten
 */
package account;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** 
 * Dummy transaction that prints a start message, waits for a random time 
 * (up to 100ms) and finally prints a status message at termination.
 */
class Transaction extends Thread {

	// identifier of the transaction
	int id;
	
	Transaction(int id) {
		this.id = id;
	}
	
	@Override
	public void run() {
		System.out.println("transaction " + id + " started");
		
		// replace this with a transaction
		int ms = (int)(Math.random()*100);
		try {
			sleep(ms);
		} catch (Exception e) {};
		
		System.out.println("transaction " + id + " terminated");
	}	
	
}

/**
 * <p>
 * Run numThreads transactions, where at most maxConcurrent transactions 
 * can run in parallel.
 * 
 * <p>params: numThreads maxConcurrent
 *
 */
public class ConcurrentTransactions {

	public static void main(String[] args) {

		// read command line parameters
		if (args.length != 2) {
			System.err.println("params: numThreads maxConcurrent");
			System.exit(-1);
		}	
		int numThreads = Integer.parseInt(args[0]);
		int maxConcurrent = Integer.parseInt(args[1]);

		// create numThreads transactions
		Transaction[] trans = new Transaction[numThreads];
		for (int i = 0; i < trans.length; i++) {
			trans[i] = new Transaction(i + 1);
		}

		// start all transactions using a thread pool 
		ExecutorService pool = Executors.newFixedThreadPool(maxConcurrent);				
		for (int i = 0; i < trans.length; i++) {
			pool.execute(trans[i]);
		}		
		pool.shutdown(); // end program after all transactions are done	
		while (!pool.isTerminated());
	}
}
 
