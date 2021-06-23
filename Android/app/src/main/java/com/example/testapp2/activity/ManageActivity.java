package com.example.testapp2.activity;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.example.testapp2.Network.RetrofitClient;
import com.example.testapp2.Network.ServiceApi;
import com.example.testapp2.R;
import com.example.testapp2.data.MypageData;
import com.example.testapp2.data.MypageResponse;
import com.example.testapp2.data.UpdateData;
import com.example.testapp2.data.UpdateResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ManageActivity extends AppCompatActivity {

    private EditText userPW, userName, userPhone;
    private TextView tvID;
    private ServiceApi service;
    private ImageButton btnupdate;
    String id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_manage);

        service = RetrofitClient.getClient().create(ServiceApi.class);

        Intent idintent = getIntent();
        id = idintent.getStringExtra("id");

        tvID = findViewById(R.id.tv_id);
        userPW = findViewById(R.id.edt_pw);
        userName = findViewById(R.id.edt_name);
        userPhone = findViewById(R.id.edt_phone);

        btnupdate = findViewById(R.id.btn_update);
        btnupdate.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Update();
            }
        });

        mypage();
    }
    private void mypage(){

        Mypage(new MypageData(id));

    }
    private void Mypage(MypageData data) {
        service.mypage(data).enqueue(new Callback<MypageResponse>() {
            @Override
            public void onResponse(Call<MypageResponse> call, Response<MypageResponse> response) {
                MypageResponse result=response.body();
                if(result.getCode()==200){
                    tvID.setText(result.getUserid());
                    userPW.setText(result.getUserpw());
                    userName.setText(result.getUsername());
                    userPhone.setText(result.getUserphone());
                }
            }

            @Override
            public void onFailure(Call<MypageResponse> call, Throwable t) {
                Toast.makeText(ManageActivity.this, "ERROR",Toast.LENGTH_SHORT).show();
                Log.e("ERROR", t.getMessage());
            }
        });
    }

    private void Update() {
        userPW.setError(null);
        userName.setError(null);
        userPhone.setError(null);

        String pw = userPW.getText().toString();
        String name = userName.getText().toString();
        String phone = userPhone.getText().toString();

        boolean cancel = false;
        View focusView = null;

        if(pw.isEmpty()) {
            userPW.setError("비밀번호를 입력하세요");
            focusView = userPW;
            cancel = true;
        }

        if(cancel) {
            focusView.requestFocus();
        } else {
            startUpdate(new UpdateData(id, pw, name, phone));
        }
    }
    private void startUpdate(UpdateData data) {
        service.update(data).enqueue(new Callback<UpdateResponse>() {
            @Override
            public void onResponse(Call<UpdateResponse> call, Response<UpdateResponse> response) {
                UpdateResponse result = response.body();
                Toast.makeText(ManageActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                if(result.getCode() == 200) {
                    finish();
                }
            }

            @Override
            public void onFailure(Call<UpdateResponse> call, Throwable t) {
                Toast.makeText(ManageActivity.this, "ERROR",Toast.LENGTH_SHORT).show();
                Log.e("ERROR", t.getMessage());
            }
        });
    }
}