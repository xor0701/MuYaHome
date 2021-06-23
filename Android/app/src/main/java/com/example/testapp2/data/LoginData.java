package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class LoginData {
    @SerializedName("userId")
    String userId;

    @SerializedName("userPw")
    String userPw;

    public LoginData(String userId, String userPw) {
        this.userId = userId;
        this.userPw = userPw;
    }
}
