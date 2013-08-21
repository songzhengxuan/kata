package com.example.memoryleak.handler;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;

public class LongRunThreadLeak extends Activity {

    private Handler mHandler;
    private static final int MSG_TYPE_A = 0;
    private static final int MSG_TYPE_B = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.long_run_handler);

        mHandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                switch (msg.what) {
                case MSG_TYPE_A:
                    handleMessageA();
                    break;
                case MSG_TYPE_B:
                    handleMessageB();
                    break;
                default:
                    break;
                }
            }
        };
        
        Message msg = mHandler.obtainMessage(MSG_TYPE_A);
        mHandler.sendMessageDelayed(msg, 1000 * 20);
    }

    protected void handleMessageA() {
    }

    private void handleMessageB() {
    }
}
