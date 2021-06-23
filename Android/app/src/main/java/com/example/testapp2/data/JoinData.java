package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class JoinData {

    @SerializedName("userId")
    private String userId;

    @SerializedName("userPw")
    private String userPw;

    @SerializedName("userName")
    private String userName;

    @SerializedName("userPhone")
    private String userPhone;

    @SerializedName("hostcode")
    private String hostcode;

    public JoinData(String userId,String userName, String userPw,String userPhone,String hostcode) {
        this.userName = userName;
        this.userPw = userPw;
        this.userId = userId;
        this.userPhone=userPhone;
        this.hostcode=hostcode;
    }
}