package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class IdCheckData {
    @SerializedName("userId")
    String userId;


    public IdCheckData(String userId) {
        this.userId = userId;

    }
}
