//製作拼裝網頁的<header>內容
function makeHeader(token) {
    var header_body = ''

    header_body += '<header>';
    header_body += '<nav id="nav1">';
    header_body += '<a href="/index" id="logo"><h1>個人電商</h1></a>';
    header_body += '<div class="header_btn">';
    if (token){
        header_body += '<b>Hi~' + username + '</b>';
    }
    header_body += '<a href="/cart">購物車</a>';
    if (token) {
        header_body += '<a href="#" onclick="logOut()">登出</a>';
    } else {
        header_body += '<a href="/register">註冊</a>';
        header_body += '<a href="/login">登入</a>';
    }
    header_body += '</div>';
    header_body += '</nav>';
    header_body += ' <nav id="nav2">';
    header_body += ' <!--搜尋框-->';
    header_body += '<form action="/search" id="index_form">';
    header_body += '<input type="text" name="kw" placeholder="輸入您想找的商品" style="width: 300px;height:30px">';
    header_body += '<input type="submit" value="搜尋">';
    header_body += '</form>';
    header_body += '<div class="header_btn">';
    header_body += '<a href="/vendor">廠商合作</a>';
    header_body += '<a href="/usercenter">顧客中心</a>';
    header_body += '</div>';
    header_body += '</nav>';
    header_body += '</header>';

    return header_body
}

//登出
function logOut() {
    if (confirm("確認登出嗎？")) {
        window.localStorage.removeItem('mfit_token');
        window.localStorage.removeItem('mfit_user');
        window.location.href = '/index';
    }
}

// //收藏功能
// function AddFavor() {
//     $(".favor_btn").on("click", function(){

//     });
// }
