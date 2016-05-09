package android.test;

public class Test {

	public static void main(String[] args) {
		
		long start = System.currentTimeMillis();
		System.out.println(start);
		for (int i = 0; i < 100; i++) {
		System.out.println(i);
		}
		long end = System.currentTimeMillis();
		System.out.println(end);
		long time=end-start;
		System.out.println(time);
	}

}
