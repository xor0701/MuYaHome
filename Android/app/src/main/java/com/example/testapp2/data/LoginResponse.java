package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class LoginResponse {

    @SerializedName("code")
    private int code;

    @SerializedName("message")
    private String message;

    @SerializedName("userid")
    private String userid;

    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }

    public String getUserid() {
        return userid;
    }

}