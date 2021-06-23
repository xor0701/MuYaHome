package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class EleData {
    @SerializedName("userId")
    String userId;


    public EleData(String userId) {
        this.userId = userId;

    }
}
