package com.example.memoleak.nonstaticinnerclass;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.widget.TextView;

public class MainActivity extends Activity {
	class LeakyNonstaticInnerClass {
		void doSomething() {
			System.out.println("Oops");
		}
	}
	
	private static LeakyNonstaticInnerClass leak = null;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		if (leak == null) {
			leak = new LeakyNonstaticInnerClass();
		}
		TextView text = (TextView) findViewById(R.id.text);
		text.setBackgroundResource(R.drawable.image_large);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.activity_main, menu);
		return true;
	}

}
