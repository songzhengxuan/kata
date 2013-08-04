package com.example.memoryleak.gcroot;

import java.util.ArrayList;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public class PathToGCRoots extends Activity {
    private static class Foo {
        private Foo mRef = null;
        private String mName;

        public Foo(String name) {
            mName = name;
        }

        public void setChild(Foo bar) {
            mRef = bar;
        }

        public void doSomething() {
            System.out.println(mRef.mName);
        }

        @Override
        public String toString() {
            return getClass().getName() + "[name=" + mName + "]";
        }
    }

    private static ArrayList<Foo> sInstances = new ArrayList<Foo>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView textView = new TextView(this);
        textView.setText("Path to gc roots");

        Foo foo00 = new Foo("00");
        Foo foo01 = new Foo("01");

        Foo foo10 = new Foo("10");
        Foo foo11 = new Foo("11");

        Foo foo20 = new Foo("20");

        sInstances.add(foo01);
        sInstances.add(foo00);
        foo00.setChild(foo10);
        foo01.setChild(foo11);
        foo10.setChild(foo20);
        foo11.setChild(foo20);
    }

    @Override
    public String toString() {
        return getClass().getName() + "[name=" + "haha" + "]";
    }
}
