const multer = require('multer');

var storage = multer.diskStorage({
    destination: './uploads/',
    filename: function(req, file, cb) {
		return crypto.pseudoRandomBytes(16, function(err, raw) {
			if(err) {
				return cb(err);
			}
			return cb(null, file.originalname);
		});
	}
});

module.exports = (app) => {
    const contacts = require('./controller.js'); //contact.controller.js를 로딩

    app.post('/user/join', contacts.join); //회원가입
    app.post('/user/login', contacts.login); //로그인
    app.post('/user/idcheck', contacts.idcheck); //아이디 중복 체크
    app.post('/user/codecheck',contacts.codecheck);//세대코드 체크

    app.post('/cctv/cctvon',contacts.cctvon);//cctv 1값 체크

    app.post('/user/mypage', contacts.mypage);
    app.post('/user/update', contacts.update);

    app.post('/upload', multer({
        storage: storage
    }).single('upload'), contacts.upload);
    app.get('/uploads/:upload', contacts.uploadfile);

    app.get('/callelevator12',contacts.callelevator12);

    app.post('/rpi/pir', contacts.pir);

    app.post('/face', contacts.face);
    
    app.get('/test', contacts.test);

    app.post('/user/elecall', contacts.elecall);
    app.post('/user/eleopen',contacts.eleopen);

    app.get('/push', contacts.push);
}