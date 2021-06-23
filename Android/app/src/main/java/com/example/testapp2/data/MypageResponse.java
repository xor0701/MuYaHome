package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class MypageResponse {
    @SerializedName("code")
    private int code;

    @SerializedName("message")
    private String message;

    @SerializedName("username")
    private String userName;

    @SerializedName("userid")
    private String userId;

    @SerializedName("userpw")
    private String userPw;

    @SerializedName("userphone")
    private String userPhone;

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public String getUsername() {
        return userName;
    }

    public String getUserid() {
        return userId;
    }

    public String getUserpw() {
        return userPw;
    }

    public String getUserphone() {
        return userPhone;
    }
}
