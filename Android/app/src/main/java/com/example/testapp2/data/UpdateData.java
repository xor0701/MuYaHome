package com.example.testapp2.data;

import com.google.gson.annotations.SerializedName;

public class UpdateData {
    @SerializedName("userId")
    private String userId;

    @SerializedName("userPw")
    private String userPw;

    @SerializedName("userName")
    private String userName;

    @SerializedName("userPhone")
    private String userPhone;

    public UpdateData(String userId, String userPw, String userName, String userPhone){
        this.userId = userId;
        this.userPw = userPw;
        this.userName = userName;
        this.userPhone = userPhone;
    }
}
