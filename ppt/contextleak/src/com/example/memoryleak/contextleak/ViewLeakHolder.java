package com.example.memoryleak.contextleak;

import android.view.View;

public class ViewLeakHolder {
    private static View sViewInstance = null;
    public ViewLeakHolder() {
    }
    
    public static void setView(View view) {
        if (sViewInstance == null) {
            sViewInstance = view;
        }
    }
}
