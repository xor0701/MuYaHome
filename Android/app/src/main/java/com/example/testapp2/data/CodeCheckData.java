package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class CodeCheckData {
    @SerializedName("hostcode")
    String hostcode;


    public CodeCheckData(String hostcode) {
        this.hostcode = hostcode;

    }
}
