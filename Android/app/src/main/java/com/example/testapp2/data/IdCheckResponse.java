package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class IdCheckResponse {
    @SerializedName("code")
    private int code;

    @SerializedName("message")
    private String message;
    public int getCode() {
        return code;
    }

    public String getMessage() {
        return message;
    }
}