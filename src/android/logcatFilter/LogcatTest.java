package android.logcatFilter;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
/**
 * 使用adb logcat | findstr Displayed命令获取页面跳转响应时间
 * 
 * Created on 2015/12/16
 * 
 * @author Reggie 
 *
 */

public class LogcatTest implements Runnable {
	static LogcatTest lt = new LogcatTest();

	public static void main(String[] args) {
		lt.run();
		// lt.test01();
	}

	@Override
	public void run() {
		String command = "adb logcat";
		StringBuffer sb = new StringBuffer();
		String line = null;
		try {
			Process proc = Runtime.getRuntime().exec(command);
//			StreamGobbler errorGobbler = new StreamGobbler(proc.getErrorStream(), "ERROR");
//			errorGobbler.start();
//			StreamGobbler outGobbler = new StreamGobbler(proc.getInputStream(), "STDOUT");
//			outGobbler.start();
//			proc.waitFor();
			BufferedReader br = new BufferedReader(new InputStreamReader(proc.getInputStream()));
			while ((line = br.readLine()) != null) {
				if (line.contains("Displayed")) {
					System.out.println(line);
//					String[] str0 = line.split(" ");
//					System.out.println(str0[str0.length - 1]);
//					sb.append(line + "\n");
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		} 

	}

	public void test01() {
		String str0 = "I/ActivityManager(  803): [AppLaunch] Displayed Displayed com.aurora.note/.NoteMainActivity: +411ms";
		String[] str1 = str0.split(" ");
		System.out.println(Arrays.toString(str1));
		String str2 = str1[str1.length - 1].trim();
		System.out.println(str2);
	}

}
