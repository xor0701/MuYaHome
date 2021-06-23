package com.example.testapp2.activity;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;

import com.example.testapp2.R;
import com.example.testapp2.Network.ServiceApi;

public class LoadingActivity extends Activity {

    private ServiceApi service;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_loading);

        startLoading();
    }

    private void startLoading() {
        Handler handler = new Handler();
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent intent = new Intent(getBaseContext(), com.example.testapp2.activity.LoginActivity.class);
                startActivity(intent);
                finish();
            }
        }, 3000);
    }

}