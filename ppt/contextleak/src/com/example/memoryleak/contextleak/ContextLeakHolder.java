package com.example.memoryleak.contextleak;

import android.content.Context;

public class ContextLeakHolder {
    private static Context sContext = null;
    public ContextLeakHolder() {
    }
    
    public static void setContext(Context context) {
        sContext = context;
    }
}
