package com.example.testapp2.activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.testapp2.R;
import com.example.testapp2.Network.RetrofitClient;
import com.example.testapp2.Network.ServiceApi;
import com.example.testapp2.data.LoginData;
import com.example.testapp2.data.LoginResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class LoginActivity extends AppCompatActivity {

    private ServiceApi service;
    private ImageButton login_button, join_button;
    private EditText login_id,login_pw;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        service = RetrofitClient.getClient().create(ServiceApi.class);

        login_id=findViewById(R.id.login_id);
        login_pw=findViewById(R.id.login_password);

        join_button = findViewById(R.id.join_button);
        join_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(com.example.testapp2.activity.LoginActivity.this, com.example.testapp2.activity.JoinActivity.class);
                startActivity(intent);
            }
        });

        login_button = findViewById( R.id.login_button );
        login_button.setOnClickListener( new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                //Intent intent = new Intent(com.example.testapp2.activity.LoginActivity.this, com.example.testapp2.activity.MainActivity.class);
                //startActivity(intent);
                Login();

            }
        });
    }

    private void Login(){
        login_id.setError(null);
        String Id=login_id.getText().toString();
        String Pw=login_pw.getText().toString();

        boolean cancel=false;
        View focusView =null;

        //아이디의 유효성 검사
        if(Id.isEmpty()){
            login_id.setError("아이디를 입력해주세요.");
            focusView = login_id;
            cancel=true;
        }else if(!isIDValid(Id)){
            login_id.setError("6자리 이상으로 입력해주세요.");
            focusView = login_id;
            cancel=true;
        }if(Pw.isEmpty()){
            login_pw.setError("비밀번호를 입력해주세요.");
            focusView = login_pw;
            cancel=true;
        }else if(!isPWValid(Pw)){
            login_pw.setError("4자리 이상으로 입력해주세요.");
            focusView = login_pw;
            cancel=true;
        }

        if(cancel){
            focusView.requestFocus();
        }else{
            startLogin(new LoginData(Id,Pw));
        }

    }

    private void startLogin(LoginData data){

        service.userLogin(data).enqueue(new Callback<LoginResponse>() {
            @Override
            public void onResponse(Call<LoginResponse> call, Response<LoginResponse> response) {
                LoginResponse result=response.body();
                Toast.makeText(com.example.testapp2.activity.LoginActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                if(result.getCode()==200){
                    Intent intent = new Intent(com.example.testapp2.activity.LoginActivity.this, com.example.testapp2.activity.MainActivity.class);
                    String id = result.getUserid();
                    intent.putExtra("id", id);
                    startActivity(intent);
                }

            }

            @Override
            public void onFailure(Call<LoginResponse> call, Throwable t) {
                Toast.makeText(com.example.testapp2.activity.LoginActivity.this,"존재하지않는 아이디입니다.",Toast.LENGTH_SHORT).show();
            }
        });
    }
    private boolean isIDValid(String id) {
        return id.length() >= 6;
    }
    private boolean isPWValid(String pw) {
        return pw.length() >= 4;
    }
}