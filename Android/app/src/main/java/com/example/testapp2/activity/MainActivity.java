package com.example.testapp2.activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

import androidx.appcompat.app.AppCompatActivity;

import com.example.testapp2.R;
import com.example.testapp2.Network.RetrofitClient;
import com.example.testapp2.Network.ServiceApi;

public class MainActivity extends AppCompatActivity {
    private ServiceApi service;
    private ImageButton btndoor, btnphone, btncctv, btnele, btnmypage, btnnotice;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Intent idintent = getIntent();
        final String id = idintent.getStringExtra("id");

        service = RetrofitClient.getClient().create(ServiceApi.class);


        btnmypage = findViewById(R.id.btn_mypage);
        btnmypage.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, ManageActivity.class);
                intent.putExtra("id", id);
                startActivity(intent);
            }
        });

        btncctv = findViewById(R.id.btn_cctv);
        btncctv.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, CCTVActivity.class);
                startActivity(intent);
            }
        });

        btnele = findViewById(R.id.btn_ele);
        btnele.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(MainActivity.this, ElevatorActivity.class);
                intent.putExtra("id", id);
                startActivity(intent);
            }
        });
    }
}
