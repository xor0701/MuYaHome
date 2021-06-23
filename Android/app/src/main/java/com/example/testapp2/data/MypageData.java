package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class MypageData {
    @SerializedName("userId")
    private String userId;

    public MypageData(String userId){
        this.userId = userId;
    }
}
