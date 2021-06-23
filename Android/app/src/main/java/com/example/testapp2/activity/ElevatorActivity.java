package com.example.testapp2.activity;

import android.content.Intent;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.example.testapp2.Network.RetrofitClient;
import com.example.testapp2.Network.ServiceApi;
import com.example.testapp2.R;
import com.example.testapp2.data.EleData;
import com.example.testapp2.data.EleResponse;
import com.example.testapp2.data.ElecallData;
import com.example.testapp2.data.ElecallResponse;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class ElevatorActivity extends AppCompatActivity {
    private ServiceApi service;
    TextView elefloor;
    Button btnok, cancelbtn;
    String id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ele);
        Intent idintent = getIntent();
        id = idintent.getStringExtra("id");
        service = RetrofitClient.getClient().create(ServiceApi.class);

        elefloor=findViewById(R.id.elefloor);

        btnok = (Button) findViewById(R.id.btnok);
        cancelbtn = (Button) findViewById(R.id.cancelbtn);

        btnok.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                elecall();
            }
        });
        eleopen();

    }
    //동작클릭
    public void mok(View view) {
        finish();
    }
    //취소클릭
    public void mcancel(View view) {
        finish();
    }
    @Override
    public boolean onTouchEvent(MotionEvent event) {
        //바깥레이어 클릭시 안닫히게
        if (event.getAction() == MotionEvent.ACTION_OUTSIDE) {
            return false;
        }
        return true;
    }
    @Override
    public void onBackPressed(){
        //안드로이드 백버튼 막기
        return;
    }

    private void elecall(){

        elecallstart(new ElecallData(id));


    }

    private void elecallstart(ElecallData data){

        service.Elefloor(data).enqueue(new Callback<ElecallResponse>() {
            @Override
            public void onResponse(Call<ElecallResponse> call, Response<ElecallResponse> response) {
                ElecallResponse result=response.body();

                if(result.getCode()==200){
                    String message = result.getMessage();
                    Toast.makeText(ElevatorActivity.this, message, Toast.LENGTH_SHORT).show();
                    finish();
                }

            }

            @Override
            public void onFailure(Call<ElecallResponse> call, Throwable t) {
                Toast.makeText(ElevatorActivity.this,"호출실패",Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void eleopen(){

        eleopenstart(new EleData(id));


    }

    private void eleopenstart(EleData data){

        service.Eleopen(data).enqueue(new Callback<EleResponse>() {
            @Override
            public void onResponse(Call<EleResponse> call, Response<EleResponse> response) {
                EleResponse result=response.body();

                if(result.getCode()==200){
                    String message = result.getMessage();
                    Toast.makeText(ElevatorActivity.this, message, Toast.LENGTH_SHORT).show();
                    elefloor.setText(message);

                }

            }
            @Override
            public void onFailure(Call<EleResponse> call, Throwable t) {
                Toast.makeText(ElevatorActivity.this,"실패",Toast.LENGTH_SHORT).show();
            }
        });
    }
}

