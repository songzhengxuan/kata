package com.example.rotateeclipse;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;

public class MainActivity extends Activity {
    Runnable moveRunnable = null;
    Handler handler;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        final Draw2d view = new Draw2d(this);
        setContentView(view);

        handler = new Handler();
        moveRunnable = new Runnable() {

            @Override
            public void run() {
                view.increaseTick(1);
                handler.postDelayed(moveRunnable, 20);
            }
        };
        handler.post(moveRunnable);
    }

}
