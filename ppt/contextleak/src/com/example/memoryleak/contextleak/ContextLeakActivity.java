package com.example.memoryleak.contextleak;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class ContextLeakActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView thisView = new TextView(this);
        thisView.setText("ContextLeak example");
        setContentView(thisView);
        
        ContextLeakHolder.setContext(this);
    }
}
