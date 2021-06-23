package com.example.testapp2.Network;


import com.example.testapp2.data.CodeCheckData;
import com.example.testapp2.data.CodeCheckResponse;
import com.example.testapp2.data.EleData;
import com.example.testapp2.data.EleResponse;
import com.example.testapp2.data.ElecallData;
import com.example.testapp2.data.ElecallResponse;
import com.example.testapp2.data.IdCheckData;
import com.example.testapp2.data.IdCheckResponse;
import com.example.testapp2.data.JoinData;
import com.example.testapp2.data.JoinResponse;
import com.example.testapp2.data.LoginData;
import com.example.testapp2.data.LoginResponse;
import com.example.testapp2.data.MypageData;
import com.example.testapp2.data.MypageResponse;
import com.example.testapp2.data.UpdateData;
import com.example.testapp2.data.UpdateResponse;

import okhttp3.MultipartBody;
import okhttp3.RequestBody;
import okhttp3.ResponseBody;
import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.Header;
import retrofit2.http.Multipart;
import retrofit2.http.POST;
import retrofit2.http.Part;

public interface ServiceApi {
    //로그인
    @POST("/user/login")
    Call<LoginResponse> userLogin(@Body LoginData data);

    //회원가입
    @POST("/user/join")
    Call<JoinResponse> userJoin(@Body JoinData data);

    //아이디 중복조회
    @POST("/user/idcheck")
    Call<IdCheckResponse> checkId(@Body IdCheckData data);

    //세대번호 조회
    @POST("/user/codecheck")
    Call<CodeCheckResponse> checkcode(@Body CodeCheckData data);

    //MYPAGE
    @POST("/user/mypage")
    Call<MypageResponse> mypage(@Body MypageData data);

    //UPDATE
    @POST("/user/update")
    Call<UpdateResponse> update(@Body UpdateData data);

    //UPLOAD
    @Multipart
    @POST("/upload")
    Call<ResponseBody> postImage(@Part MultipartBody.Part image, @Part("upload")
                                 RequestBody name);
    //elecall
    @POST("/user/elecall")
    Call<ElecallResponse> Elefloor(@Body ElecallData data);

    //eleopen
    @POST("/user/eleopen")
    Call<EleResponse> Eleopen(@Body EleData data);
}