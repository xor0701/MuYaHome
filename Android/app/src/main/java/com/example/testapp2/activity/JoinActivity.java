package com.example.testapp2.activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.testapp2.R;
import com.example.testapp2.data.CodeCheckData;
import com.example.testapp2.data.CodeCheckResponse;
import com.example.testapp2.data.IdCheckData;
import com.example.testapp2.data.IdCheckResponse;
import com.example.testapp2.Network.RetrofitClient;
import com.example.testapp2.Network.ServiceApi;
import com.example.testapp2.data.JoinData;
import com.example.testapp2.data.JoinResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class JoinActivity extends AppCompatActivity {
    private EditText join_id, join_password, join_phonenumber, join_pwck,join_name,join_hostcode;
    private ImageButton join_button, check_button, cancel_button,codecheck_button,backbutton;
    private ServiceApi service;
    String hostcode;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_join);

        service=RetrofitClient.getClient().create(ServiceApi.class);

        join_id=findViewById(R.id.join_id);
        join_password=findViewById(R.id.join_password);
        join_pwck=findViewById(R.id.join_pwcheck);
        join_phonenumber=findViewById(R.id.join_phonenumber);
        join_name=findViewById(R.id.join_name);
        join_hostcode=findViewById(R.id.join_hostcode);

        join_button = findViewById(R.id.join_button);
        join_button.setEnabled(false);
        join_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Join();
            }
        });

        cancel_button = findViewById(R.id.cancel_button);
        cancel_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                finish();

            }
        });
        check_button=findViewById(R.id.idcheck);
        check_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                IDCheck();
            }
        });

        codecheck_button=findViewById(R.id.codecheck);
        codecheck_button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                codeCheck();

            }
        });

        backbutton=findViewById(R.id.join_backbtn);
        backbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
    private void codeCheck(){
        join_hostcode.setError(null);
        hostcode=join_hostcode.getText().toString();

        boolean cancel=false;
        View focusView =null;

        //세대번호의 유효성 검사
        if(hostcode.isEmpty()){
            join_hostcode.setError("세대코드를 입력해주세요.");
            focusView = join_hostcode;
            cancel=true;
        }

        if(cancel){
            focusView.requestFocus();
        }else{

            codeCheck(new CodeCheckData(hostcode));
        }

    }

    private void codeCheck(CodeCheckData data){

        service.checkcode(data).enqueue(new Callback<CodeCheckResponse>() {
            @Override
            public void onResponse(Call<CodeCheckResponse> call, Response<CodeCheckResponse> response) {
                CodeCheckResponse result=response.body();
                Toast.makeText(com.example.testapp2.activity.JoinActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                if(result.getCode()==200){
                    join_id.setVisibility(View.VISIBLE);
                    join_password.setVisibility(View.VISIBLE);
                    join_pwck.setVisibility(View.VISIBLE);
                    join_name.setVisibility(View.VISIBLE);
                    join_phonenumber.setVisibility(View.VISIBLE);
                    join_button.setVisibility(View.VISIBLE);
                    check_button.setVisibility(View.VISIBLE);
                }
            }

            @Override
            public void onFailure(Call<CodeCheckResponse> call, Throwable t) {
                Toast.makeText(com.example.testapp2.activity.JoinActivity.this,"맞지 않는 코드 입니다.",Toast.LENGTH_SHORT).show();
            }
        });
    }
    private void IDCheck(){
        join_id.setError(null);
        String Id=join_id.getText().toString();

        boolean cancel=false;
        View focusView =null;

        //아이디의 유효성 검사
        if(Id.isEmpty()){
            join_id.setError("아이디를 입력해주세요.");
            focusView = join_id;
            cancel=true;
        }else if(!isIDValid(Id)){
            join_id.setError("6자리 이상으로 입력해주세요.");
            focusView = join_id;
            cancel=true;
        }

        if(cancel){
            focusView.requestFocus();
        }else{

            startIDCheck(new IdCheckData(Id));
        }

    }

    private void startIDCheck(IdCheckData data){

        service.checkId(data).enqueue(new Callback<IdCheckResponse>() {
            @Override
            public void onResponse(Call<IdCheckResponse> call, Response<IdCheckResponse> response) {
                IdCheckResponse result=response.body();
                Toast.makeText(com.example.testapp2.activity.JoinActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                if(result.getCode()==200){
                    join_button.setEnabled(true);
                    join_button.setBackgroundResource(R.drawable.joinbtn);
                }
                else{
                    join_button.setEnabled(false);
                    join_button.setBackgroundResource(R.drawable.joinbtn_disenable);
                }
            }

            @Override
            public void onFailure(Call<IdCheckResponse> call, Throwable t) {
                Toast.makeText(com.example.testapp2.activity.JoinActivity.this,"이미 가입한 아이디입니다.",Toast.LENGTH_SHORT).show();
            }
        });
    }
    private void Join(){
        join_id.setError(null);
        join_password.setError(null);
        join_pwck.setError(null);
        join_phonenumber.setError(null);
        join_name.setError(null);

        String Id=join_id.getText().toString();
        String Pw=join_password.getText().toString();
        String Pwck=join_pwck.getText().toString();
        String Name=join_name.getText().toString();
        String Phone=join_phonenumber.getText().toString();

        boolean cancel=false;
        View focusView =null;


        if(Pw.isEmpty()){
            join_password.setError("비밀번호를 입력해주세요.");
            focusView = join_password;
            cancel=true;
        }else if(!isPWValid(Pw)){
            join_password.setError("4자리 이상으로 입력해주세요.");
            focusView = join_password;
            cancel=true;
        }
        if(Pwck.isEmpty()){
            join_pwck.setError("비밀번호가 일치하지않습니다.");
            focusView = join_password;
            cancel=true;
        }else if(!Pwck.equals(Pw)){
            join_pwck.setError("비밀번호가 일치하지않습니다.");
            focusView = join_password;
            cancel=true;
        }
        if(Name.isEmpty()){
            join_name.setError("이름을 입력해주세요.");
            focusView = join_name;
            cancel=true;
        }


        if(Phone.isEmpty()){
            join_phonenumber.setError("전화번호를 입력해주세요.");
            focusView = join_phonenumber;
            cancel=true;
        }else if(!isNumber(Phone)){
            join_phonenumber.setError("숫자를 입력해주세요.");
            focusView = join_phonenumber;
            cancel=true;
        }else if(!isPhoneValid(Phone)){
            join_phonenumber.setError("11자리를 입력해주세요");
            focusView = join_phonenumber;
            cancel=true;
        }

        if(cancel){
            focusView.requestFocus();
        }else{
            startJoin(new JoinData(Id,Name,Pw,Phone,hostcode));

        }

    }
    private void startJoin(JoinData data){
        service.userJoin(data).enqueue(new Callback<JoinResponse>() {
            @Override
            public void onResponse(Call<JoinResponse> call, Response<JoinResponse> response) {
                JoinResponse result=response.body();
                Toast.makeText(com.example.testapp2.activity.JoinActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                if(result.getCode()==200){
                    Toast.makeText(JoinActivity.this, result.getMessage(), Toast.LENGTH_SHORT).show();
                    Intent intent = new Intent(JoinActivity.this, CameraActivity.class);
                    startActivity(intent);
                }

            }

            @Override
            public void onFailure(Call<JoinResponse> call, Throwable t) {

                Toast.makeText(getApplicationContext(),"회원가입 실패",Toast.LENGTH_SHORT).show();

            }
        });
    }
    private boolean isIDValid(String id) {
        return id.length() >= 6;
    }
    private boolean isPWValid(String pw) {
        return pw.length() >= 4;
    }
    private boolean isPhoneValid(String phone) {
        return phone.length()==11;
    }
    private boolean isNumber(String phone){
        try{
            Integer.parseInt(phone);
            return true;
        }catch(NumberFormatException e){
            return false;
        }
    }
}
