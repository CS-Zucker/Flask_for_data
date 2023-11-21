//#整个网页加载完才执行此代码
//点击发送验证码的响应
$(function()
{ $("#captcha-btn").click(function(event){
//   按钮被点击时执行,
//   function(event)被称为事件处理器或事件处理程序。
//   在这里，它被绑定到#captcha-btn元素上的click事件
//   阻止默认事件
//   event对象是一个包含了关于事件的各种信息的对象。例如，它可以包含关于事件的类型、发生事件的时间、
//   触发事件的元素等的信息。这个event对象是由浏览器在事件发生时自动创建的，并传递给事件处理程序。
   event.preventDefault();
   var email=$("#email").val();//获得input的值,email是id
   $.ajax({ //$.ajax 是 jQuery 库中的一个函数，用于发起 HTTP 请求
   url:"/auth/captcha/email?email="+email,//符合get获取数据的方式,对url发起请求
   method:"GET",
   success:function(result){
   //result 是一个从服务器返回的响应数据。
   //它是通过 AJAX请求从服务器获取的。
    var code=result['code'];
    if (code==200){
        alert("邮箱验证码发送成功")
    }else{
        alert(result['message'])
    }
   },
   fail:function(error){
    console.log(error);
   }
   })

  });//由id寻找按钮

});