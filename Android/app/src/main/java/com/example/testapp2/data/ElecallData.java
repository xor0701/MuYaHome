package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class ElecallData {
    @SerializedName("userId")
    String userId;


    public ElecallData(String userId) {
        this.userId = userId;

    }
}
