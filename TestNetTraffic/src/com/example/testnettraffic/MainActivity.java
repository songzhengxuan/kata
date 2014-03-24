package com.example.testnettraffic;

import java.util.List;

import android.app.Activity;
import android.app.ActivityManager;
import android.app.ActivityManager.RunningAppProcessInfo;
import android.content.pm.PackageManager;
import android.net.TrafficStats;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class MainActivity extends Activity {
    private ListView mList;
    private BaseAdapter mAdapter;
    private ActivityManager mActivityManager;
    private PackageManager mPackageManager;
    private LayoutInflater mInflater;
    private int[] mUids = new int[] {};
    private boolean mIsResumed;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        mList = (ListView) findViewById(R.id.list);
        mActivityManager = (ActivityManager) getSystemService(ACTIVITY_SERVICE);
        mPackageManager = getPackageManager();
        mInflater = LayoutInflater.from(this);
        mAdapter = new TrafficAdapter();
        mList.setAdapter(mAdapter);
    }

    @Override
    protected void onResume() {
        super.onResume();
        updateData();
        mIsResumed = true;
    }

    @Override
    protected void onPause() {
        super.onPause();
        mIsResumed = false;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    private void updateData() {
        List<RunningAppProcessInfo> newUids = mActivityManager.getRunningAppProcesses();
        if (newUids != null) {
            int newUidsSize = newUids.size();
            mUids = new int[newUidsSize];
            for (int i = 0; i < newUidsSize; ++i) {
                mUids[i] = newUids.get(i).uid;
            }
        }
        mAdapter.notifyDataSetChanged();
        mList.postDelayed(new Runnable() {

            @Override
            public void run() {
                if (MainActivity.this.isFinishing()) {
                    return;
                }
                if (!mIsResumed) {
                    return;
                }
                updateData();
            }
        }, 1000);
    }

    class ViewHolder {
        TextView text1;
        TextView text2;
    }

    class TrafficAdapter extends BaseAdapter {

        @Override
        public int getCount() {
            return mUids.length;
        }

        @Override
        public Object getItem(int position) {
            return null;
        }

        @Override
        public long getItemId(int position) {
            return position;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            ViewHolder holder = null;
            if (convertView == null) {
                convertView = mInflater.inflate(android.R.layout.simple_expandable_list_item_2, null);
                holder = new ViewHolder();
                convertView.setTag(holder);
                holder.text1 = (TextView) convertView.findViewById(android.R.id.text1);
                holder.text2 = (TextView) convertView.findViewById(android.R.id.text2);
            }
            if (holder == null) {
                holder = (ViewHolder) convertView.getTag();
            }
            int uid = mUids[position];
            String name = mPackageManager.getNameForUid(uid);
            long bytes = TrafficStats.getUidRxBytes(uid) + TrafficStats.getUidTxBytes(uid);
            holder.text1.setText(name);
            holder.text2.setText("" + bytes);
            return convertView;
        }

    }

}
