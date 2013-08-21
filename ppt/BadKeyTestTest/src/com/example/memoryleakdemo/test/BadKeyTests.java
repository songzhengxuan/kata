package com.example.memoryleakdemo.test;

import java.util.HashMap;

import android.test.AndroidTestCase;

public class BadKeyTests extends AndroidTestCase {
    static class BadKeyClass {
        public final String memberA;

        public BadKeyClass(String memberA) {
            this.memberA = memberA;
        }
    }

    private static final HashMap<BadKeyClass, Object> sMaps = new HashMap<BadKeyClass, Object>();

    public void testKey() {
        BadKeyClass key1 = new BadKeyClass("test");
        sMaps.put(key1, "value");
        assertTrue(sMaps.containsKey(key1));
        BadKeyClass key2 = new BadKeyClass("test");
        assertTrue(sMaps.containsKey(key2));
    }

}
