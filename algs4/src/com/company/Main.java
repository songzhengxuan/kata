package com.company;

public class Main {

    public static void main(String[] args) {
	// write your code here
        Bag<String> test = new Bag<>();
        test.add("hello world");
        test.add("hello world 2");
        for (String item : test) {
            System.out.println(item);
        }
    }
}
