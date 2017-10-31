package com.pjl.tools;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import android.serialport.SerialPort;
import android.util.Log;

public class SeriaportTool {
	private static FileOutputStream fos;
	private static FileInputStream fis;
	public static  ArrayList<byte[]> list=new ArrayList<byte[]>();
	private static SerialPort sp;
	private static ReadThread mreadthread;
	private static boolean flag=false;//清空list开关

	/**
	 * 初始化，这里定义要打开哪个串口。这里打开的串口是"/dev/ttySAC0"，不同的设备打开的串口不同，需注意修改
	 */
	static {
		try {//注意try catch的嵌套。catch有相当于return的作用,它会直接返回
			sp = new SerialPort(new File("/dev/ttySAC3"), 38400);
		} catch (SecurityException | IOException e) {
			e.printStackTrace();
			if (sp != null) {
				System.out.println("SERIAL ttySAC3" + " Enable");
			} else {
				System.out.println("SERIAL ttySAC3" + " Disable");
				try {
					sp = new SerialPort(new File("/dev/ttyS0"), 38400);
				} catch (SecurityException | IOException e1) {
					e1.printStackTrace();
					if (sp != null) {
						System.out.println("SERIAL ttyS0" + " Enable");
					} else {
						System.out.println("SERIAL ttyS0" + " Disable");
						try {
							sp = new SerialPort(new File("/dev/ttyS1"), 38400);
						} catch (SecurityException | IOException e2) {
							e2.printStackTrace();
						}
					}
				}
			}
		} // 串口和波特率
		//开启接收线程
		mreadthread = new ReadThread();
		mreadthread.start();
	}

	/**
	 * 发送
	 * 
	 * @param cmd
	 *            要发送的数据
	 * @throws Exception
	 */
	public void PTsend(byte[] cmd) throws Exception {
		fos = (FileOutputStream) sp.getOutputStream();
		fos.write(cmd);
		fos.flush();
	}

	/**
	 * 接收，当收到“0xf5”时，就会结束。单开一个线程来进行接收才有效果。
	 */
	private static class ReadThread extends Thread {
		@Override
		public void run() {
			super.run();
			fis = (FileInputStream) sp.getInputStream();
			byte[] temp = null;
			while (!isInterrupted()) {
				temp = null;
				if (fis != null) {
					try {
						int i = 0;
						byte bb;
	// 为什么要把它分成"byte[] temp=null;"和"temp=new byte[80];"，因为这样才能使数组每次清空数据
						temp = new byte[80];
						do {// 一个字节一个字节的读
							bb = (byte) fis.read();
							temp[i] = bb;
	// 这样才能保证数据的有效性，无效数据会被过滤掉，起始符必须符合fc、fb、fa，不然不让temp数组的i增加
							if (temp[0] == (byte) 0xfc || temp[0] == (byte) 0xfb || temp[0] == (byte) 0xfa) {
								i++;
							}
						} while (bb != (byte) 0xf5); // 保证结束符为f5	
						if(flag==true){//清空ArrayList集合，释放资源
							list.clear();
						}//用ArrayList<byte[]>来存放byte数组，这样能缓存接收的数据
							list.add(Arrays.copyOf(temp, i));//用Arrays.copyOf()来传递，可以确定这个数组的具体长度
							flag=false;//把标志位改回不清空状态
					} catch (IOException e) {
						e.printStackTrace();
					}
				}
			}
		}
	}

	@Override
	protected void finalize() throws Throwable {
		if (mreadthread != null)
			mreadthread.interrupt();
		fos.flush();
		fos.close();
		fis.close();
		sp = null;
		super.finalize();

	}

	private void delay(int ms) {
		try {
			Thread.currentThread();
			Thread.sleep(ms);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
	}
	
	public static ArrayList<byte[]> getBuffer(){
		flag=true;
		return list;	
	}
	// 16进制字节（byte）转字符串
	public static String bytesToHexString(byte[] src) {
		StringBuilder stringBuilder = new StringBuilder("");
		if (src == null || src.length <= 0) {
			return null;
		}
		for (int i = 0; i < src.length; i++) {
			int v = src[i] & 0xFF;
			String hv = Integer.toHexString(v);
			if (hv.length() < 2) {
				stringBuilder.append(0);
			}
			stringBuilder.append(hv);
		}
		return stringBuilder.toString();
	}

	public static byte[] hexStringToBytes(String hexString) {
		if (hexString == null || hexString.equals("")) {
			return null;
		}
		hexString = hexString.toUpperCase();
		int length = hexString.length() / 2;
		char[] hexChars = hexString.toCharArray();
		byte[] d = new byte[length];
		for (int i = 0; i < length; i++) {
			int pos = i * 2;
			d[i] = (byte) (charToByte(hexChars[pos]) << 4 | charToByte(hexChars[pos + 1]));
		}
		return d;
	}

	private static byte charToByte(char c) {
		return (byte) "0123456789ABCDEF".indexOf(c);
	}
}
