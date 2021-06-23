var fs = require('fs');
var ejs = require('ejs');
var mysql = require('mysql');
var axios = require('axios');
var kill = require('tree-kill');
var fs = require('fs');
multer = require('multer');
path = require('path');
crypto = require('crypto');

var floor = 0;
var success="false";

//파이어베이스
var FCM = require('fcm-node'); 
var serverKey = 'AAAATKht2Mg:APA91bEVYVJ3SugQZINCOk8hFVOQuW3Cofm37z8Unwjb1Sa7bH7diZA9q-58KTV5cWL-rCIz6aOsSGzbhQ4xC28v82RMnUokVS-C6jH9ddTU5PLpN_rF21meazk_Azy4aNTVvOgLCn-4'; //서버키 
var fcm = new FCM(serverKey);

var message = { //this may vary according to the message type (single recipient, multicast, topic, et cetera) 
    to: 'euGXDgeWQr692pptG_J8FY:APA91bGZ8WV2T7rjbQzuAwSwZBDtBn9rSjA4vL5JM1Rvm2p1przM6aYqnxCVQITlyT4di96QC23TbqNIrpkcvHxAiBsxSnhl1fZtZy-0QwlItrVIZIgY53KMt9aYAlukOA8eyhId0FEm', //앱에서 복사한 토큰 
    notification: { 
        title: '제목', 
        body: '내용' 
    }, 
    data: { //you can send only notification or only data(or include both) 
        my_key: 'my value', 
        my_another_key: 'my another value' 
    } 
};

fcm.send(message, function(err, response){ 
    if (err) { 
        console.log("Something has gone wrong!"); 
    } 
    else { 
        console.log("Successfully sent with response: ", response); 
    } 
});


/////////////////////////////pushAlarm///////////////// 
const admin = require("firebase-admin"); 
let serviceAccount = require("./firebase-admin.json"); 
admin.initializeApp({ 
    credential: admin.credential.cert(serviceAccount), 
}); 
//////////////////////////////pushAlarm//////////////////


     



// 데이터베이스와 연결합니다.
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '123456789',
    database: 'db_muyahome',
    port: 3306
});


exports.join = (req, res) => { //회원가입 요청시
    
    let res1 = res;
    var resultCode = 404;
    var message = '에러가 발생했습니다';

    //req.body는 APP에서 POST로 넘어온 값을 가지고 있고 sql명령문으로 디비에 insert문을 보냄
    connection.query("INSERT INTO `db_muyahome`.`home` (`PK_Home_id`,`Home_pw`,`Home_phonenum`,`Home_name`,`FK_Ho_code`) VALUES ('"
    +req.body.userId+"','"+req.body.userPw+"','"+req.body.userPhone+"','"+req.body.userName+"','"+req.body.hostcode+"');", function(err, results,flied) {

        if(results!=null){
            console.log("회원가입성공.")
            resultCode = 200;
            message = "회원가입 되었습니다."
        }
        else{
            console.log("회원가입실패")
            resultCode = 204;
            message = "회원가입을 실패했습니다."
        }
        
        res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
            'code': resultCode,
            'message': message
        });
    });

};




exports.login = (req, res) => { //로그인 요청 시
    console.log('로그인');
    let res1 = res;

    USERID = req.body.userId; //로그인을 할때 보냄 id값이 저장
    //디비에 SELECT문을 보냄
    console.log(req.body.userId, req.body.userPw);
    connection.query("SELECT PK_Home_id, Home_pw F" +
        "ROM  db_muyahome.home where PK_Home_id='" + req.body.userId + "' AND Home_pw= '" + req.body.userPw + "';",
        function(err, results, filed) {
            var resultCode = 404;
            var message = '에러가 발생했습니다';


            if (results[0] != null) { //로그인을 할려고 한 데이터가 존재하면 검색한 결과가  NULL이 아니기 때문에 로그인 가능
                console.log("로그인 성공")
                resultCode = 200;
                message = "로그인성공"

            } else {
                { //로그인을 할려고 한 데이터가 존재하면 존재하지않으면  NULL이기 때문에 로그인 불가능가능
                    console.log("로그인 실패")
                    resultCode = 204;
                    message = "아이디와 비밀번호가 일치하지 않습니다."
                }


            }
            res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'code': resultCode,
                'message': message,
                'userid' : USERID
            });
        });


};



exports.idcheck = (req, res) => { //아이디 중복요청시
    
    console.log(req.body.userId);
   
    let res1 = res;

    //디비에 SELECT문을 보냄
    connection.query("SELECT PK_Home_id FROM  home where PK_Home_id='" + req.body.userId + "';",
        function(err, results, filed) {
            console.log(results[0]);
            var resultCode = 404;
            var message = '에러가 발생했습니다';
            
            if (results[0] != null) { //보낸 데이터(아이디)가 디비에 있으면 결과값이 NULL아니다. 그러므로 가입한 아이디는 있는것이다.
                console.log("아이디있다.")
                resultCode = 204;
                message = "이미 유효한 아이디입니다."

            } else { //보낸 데이터(아이디)가 디비에 없으면 결과값이 NULL이다. 그러므로 가입한 아이디는 없는것이다.

                console.log("아이디없다.")
                resultCode = 200;
                message = "사용가능한 아이디입니다."
            }
            res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'code': resultCode,
                'message': message
            });

        });
    


};



exports.codecheck = (req, res) => { //코드 중복요청시
    
    console.log(req.body.hostcode);
   
    let res1 = res;

    //디비에 SELECT문을 보냄
    connection.query("SELECT * FROM  Ho where PK_Ho_Code='" + req.body.hostcode + "';",
        function(err, results, filed) {
            console.log("SELECT * FROM  Ho where PK_Ho_Code='" + req.body.hostcode + "';");
            var resultCode = 404;
            var message = '에러가 발생했습니다';
            
            if (results[0] != null) { 
                console.log("유효한코드")
                resultCode = 200;
                message = "유효한 코드입니다."

            } else { 

                console.log("무효한 코드")
                resultCode = 204;
                message = "무효한 코드입니다"
            }
            res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'code': resultCode,
                'message': message
            });
        });
    


};

exports.callelevator12 = (req,res) => { //아이디 중복요청시

    if(success=="false")
    {
        res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
            'message': "연결안됨",
        });
    }
    else if(success=="true"){
        console.log("엘리베이터 호출")
        if(floor==101 || floor==102)
        {
            connection.query("SELECT * FROM  elevator where FK_Line_num=12;",
            function(err, results, filed) {
            console.log(results[0].Elevator_floor)
            res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'message': "연결됨",
                'el_before':results[0].Elevator_floor,
                'el_after':1
                });
            });
            connection.query("UPDATE elevator SET Elevator_floor=1 where FK_Line_num=12;");
            
        }
        else if(floor==201 || floor==202)
        {
            connection.query("SELECT * FROM  elevator where FK_Line_num=12;",
            function(err, results, filed) {
            console.log(results[0].Elevator_floor)
            res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'message': "연결됨",
                'el_before':results[0].Elevator_floor,
                'el_after':2
                });
            });
            connection.query("UPDATE elevator SET Elevator_floor=2 where FK_Line_num=12;");
            
        }
        else if(floor==301 || floor==302)
        {
            connection.query("SELECT * FROM  elevator where FK_Line_num=12;",
            function(err, results, filed) {
            console.log(results[0].Elevator_floor)
            res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'message': "연결됨",
                'el_before':results[0].Elevator_floor,
                'el_after':3
                });
            });
            connection.query("UPDATE elevator SET Elevator_floor=3 where FK_Line_num=12;");
            
            
        }
        floor=0;
        success="false";
    }
};

exports.mypage = (req, res) => {
    console.log("mypage");
    let res1 = res;

    USERID = req.body.userId;

    //디비에 SELECT문을 보냄
    connection.query("SELECT * FROM  Home where PK_Home_id='" + req.body.userId + "';",
        function(err, results, filed) {
            var resultCode = 200;
            var message = '에러가 발생했습니다';
            
            console.log(results[0].Home_pw);
            console.log(results[0].Home_phonenum);
            console.log(results[0].Home_name);

            res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'code': resultCode,
                'message': message,
                'userid': results[0].PK_Home_id,
                'userpw': results[0].Home_pw,
                'userphone':results[0].Home_phonenum,
                'username': results[0].Home_name
            });
        });
};

exports.update = (req, res) => {
    console.log("update");
    let res1 = res;

    userId = req.body.userId;
    userPw = req.body.userPw;
    userName = req.body.userName;
    userPhone = req.body.userPhone;
    sql = 'UPDATE Home SET Home_pw=?, Home_name=?, Home_phonenum=? where PK_Home_id = ?';
    params = [userPw, userName, userPhone, userId];
    connection.query(sql, params, 
        function(err, results, filed) {
            var resultCode = 404;
            var message = 'ERROR';

            if(err) {
                console.log(err);
            } else {
                resultCode = 200;
                message = '변경되었습니다.';
            }
            res.json({
                'code' : resultCode,
                'message' : message
            });
        });
};

exports.upload = (req, res) => {
    try {
        let file = req.file;
        let originalName = '';
        let fileName = '';
        let mimeType = '';
        let size = 0;

        if(file) {
            originalName = file.originalname;
            fileName = file.filename;
            mimeType = file.mimetype;
            size = file.size;
            console.log("excute" +"\n"+ fileName);
        }else {
            console.log("request is null");
        }
    } catch (err) {
        console.dir(err.stack);
    }
    console.log(req.file);
    console.log(req.body);
    res.redirect("/uploads/"+req.file.filename);
    console.log(req.file.filename);

    return res.status(200).end();
};

exports.uploadfile = (req, res) => {
    var file = req.params.upload;
    console.log(file);
    console.log(req.params.upload); //
    var img = fs.readFileSync(__dirname + "/uploads/" + file);
    res.writeHead(200, {'Content-Type': 'image/png'});
    res.end(img, 'binary');
    console.log(__dirname + "/uploads/" + file);
};

exports.cctvon = (req, res) => {

    console.log('들어옴');
    console.log(req.body.cctvon);

    let res1 = res;

    var resultCode = 404;
    var message = '에러가 발생했습니다';
    
};

exports.pir = (req, res) => {
    console.log("pir 센서 값을 받기 위함");
    console.log(req.body.pir);

    var pir_signal = req.body.pir;
    var date = new Date();
    var date_now = date.getTime()/1000;

    var aa
    
    if(pir_signal==true){
        console.log("pir 센서 값 받기 성공");

        var {PythonShell} = require('python-shell');
        var face_signal = 'False'
        
        var options = {
            mode: 'text',
            pythonPath: 'C:/Python39/python.exe',
            pythonOptions: ['-u'],
            scriptPath: 'C:/Users/Administrator/Desktop/MuYaHome/back_end/face_recognition/',
            encoding: 'utf8',
            args: [date_now]
        }

        PythonShell.run('recognition.py', options, function(err, results) {
            console.log('얼굴 인식 실행 완료');
        
            console.log(results.length)
            console.log(results);
            console.log(results[results.length-1]);

            face_signal = results[results.length-1]

            kill(1, PythonShell.pid);            

            res.json({'face_signal' : face_signal});
            res.end();
        });
        
        PythonShell.run('record.py', options, function(err, results) {
            console.log('녹화 완료');

            if (face_signal == "True") {
                var Record_Folder = './Record';
                var recent_record;
                var delete_record;

                fs.readdir(Record_Folder, function(err, file_list) {
                    recent_record = file_list[file_list.length-1];
                    // console.log(recent_record);

                    delete_record = Record_Folder + '/' + recent_record;
                    // console.log(delete_record);

                    fs.unlink(delete_record, function (err) {
                        if (err) throw err;

                        console.log('얼굴인식 성공한 녹화 삭제됨');
                    }); 
                });              
            } else {
                console.log('얼굴인식 실패한 녹화 저장됨');
            }
        
            res.end();
        }); 
    }
};

exports.face = (req, res) => {
    console.log("얼굴인식 성공");
    console.log(req.body.face_id);

    success="true";
    floor = parseInt(req.body.face_id);
    
    res.end();
};

exports.ho_interface = (req, res) => {
    console.log("얼굴인식을 위해 호 정보 불러오기")

    // 디비에 SELECT문을 보냄
    connection.query("SELECT * FROM  Ho where PK_Ho_num;",
    function(err, results, filed) {
        var resultCode = 200;
        var message = '에러가 발생했습니다';
        
        console.log(results[0].Home_pw);
        console.log(results[0].Home_phonenum);
        console.log(results[0].Home_name);

        res1.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
            'code': resultCode,
            'message': message,
            'userid': results[0].PK_Home_id,
            'userpw': results[0].Home_pw,
            'userphone':results[0].Home_phonenum,
            'username': results[0].Home_name
        });
    });
}

exports.test = (req, res) => {
    
};

exports.elecall = (req, res) => {
    var elecallfloor;
    var ho_code;
    var ho_num;
    var line_num;
    userId=req.body.userId;

    connection.query("SELECT * FROM HOME WHERE PK_Home_id='" + userId + "';",
    function(err, results, filed) {
        ho_code=results[0].FK_Ho_code;
        sql = "SELECT * FROM HO WHERE PK_Ho_code= '"+ho_code+"';";
        connection.query(sql, 
        function(err, result, filed) {
            
            ho_num=result[0].PK_Ho_num;
            line_num=result[0].FK_Line_num;
            console.log(ho_num)
            if(ho_num==101||ho_num==102||ho_num==103||ho_num==104){
                floor=ho_num;
                elecallfloor=1;
            }else if(ho_num==201||ho_num==202||ho_num==203||ho_num==204){
                floor=ho_num;
                elecallfloor=2;
            }else if(ho_num==301||ho_num==302||ho_num==303||ho_num==304){
                floor=ho_num;
                elecallfloor=3;
            }
            console.log(elecallfloor)
            console.log(floor)
            success="true";
            res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                'code': 200,
                'message': elecallfloor,
             });
     });
    });
    

};

exports.eleopen = (req, res) => {
    
    var elecallfloor;
    var ho_code;
    var line_num;
    userId=req.body.userId;
    console.log(userId)
    connection.query("SELECT * FROM HOME WHERE PK_Home_id='" + userId + "';",
    function(err, results, filed) {
        ho_code=results[0].FK_Ho_code;
        sql = "SELECT * FROM HO WHERE PK_Ho_code= '"+ho_code+"';";
        connection.query(sql, 
        function(err, result, filed) {
            
            line_num=result[0].FK_Line_num;

            console.log(elecallfloor)
            sql = 'SELECT * FROM Elevator WHERE FK_Line_num=?;';
            params = [line_num];
            connection.query(sql, params, 
                function(err, Results, filed) {
                    console.log(Results[0].Elevator_floor);
                    res.json({ //APP에다가 JSON 형식으로 리스폰을 보냄
                    'code': 200,
                    'message': Results[0].Elevator_floor,

                 });
         });

     });
    });
};



exports.push = async function (req, res){ 
    //디바이스의 토큰 값 
    let deviceToken =`euGXDgeWQr692pptG_J8FY:APA91bGZ8WV2T7rjbQzuAwSwZBDtBn9rSjA4vL5JM1Rvm2p1przM6aYqnxCVQITlyT4di96QC23TbqNIrpkcvHxAiBsxSnhl1fZtZy-0QwlItrVIZIgY53KMt9aYAlukOA8eyhId0FEm` 
    let message = { 
        notification: { 
            title: '123', 
            body: '123', 
        }, 
        token: deviceToken, 
    } 
    admin 
    .messaging() 
    .send(message) 
    .then(function (response) { 
        console.log('Successfully sent message: : ', response) 
        return res.status(200).json({success : true}) 
    }) 
    .catch(function (err) { 
        console.log('Error Sending message!!! : ', err)
        return res.status(400).json({success : false})
    }); 
}

   