package com.example.zigbeetesttwo;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;

import com.pjl.tools.SeriaportTool;

import android.app.Activity;
import android.os.Bundle;
import android.serialport.SerialPort;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity{
	TextView tv;
	EditText ed;
	SerialPort sp;
	FileOutputStream fos;
	FileOutputStream fis;
	byte[] buffer;
//	ZigbeeAPI zapi=new ZigbeeAPI();
	SeriaportTool zapi=new SeriaportTool();
	@Override
	protected void onCreate(Bundle savedInstanceState)  {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		ed=(EditText) findViewById(R.id.ed);
		tv=(TextView) findViewById(R.id.textView1);

	}
	
	public void accept(View view)throws Exception{
		ArrayList<byte[]> list;
		byte[] butt=null;
//		butt=Arrays.copyOf(SeriaportTool.getBuffer(), SeriaportTool.getBuffer().length);
//		butt=SeriaportTool.getBuffer();
		list=SeriaportTool.getBuffer();
		for(int i=0;i<SeriaportTool.getBuffer().size();i++){
			butt=list.get(i);
		//System.out.println("收到："+butt[i]);
			System.out.println(""+SeriaportTool.bytesToHexString(butt));
		}
//		System.out.println(""+SeriaportTool.bytesToHexString(butt));
		tv.setText(""+SeriaportTool.bytesToHexString(butt));
	}
	
	
	public void send(View view) throws Exception{
		String src=ed.getText().toString().trim();
		System.out.println("src为："+src);
//		byte[] jg={(byte) 0xfa,(byte) 0x7c,(byte) 0x0f,(byte)0x03,(byte) 0xea,(byte) 0x01,(byte) 0xae,(byte) 0xf5};
//		String src="fc1000f5";
		if(src!=null||src!=""){
		zapi.PTsend(SeriaportTool.hexStringToBytes(src));
		System.out.println("已发送");
		}else{
			System.out.println("发送内容为空");
		}
	}
		
}
