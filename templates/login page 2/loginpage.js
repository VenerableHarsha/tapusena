

document.querySelector("button").addEventListener("click",function(){
    var username=document.getElementById("name").value;
    var password=document.getElementById("pass").value;
    if(check(password)==true&&checkgmail(username)){
        window.open("./homepage.html");
    }
    else{
        alert("wrong id or password");
    }
})

function checkgmail(mail)
{
    if(mail.slice(mail.indexOf("."))==".com")
    {
        return true;
    }
    else{
       return false;
    }

}



function check(password)
{


    if(password.length<8)
    {
        return false;
    }
    else{
        return true;
    }
}
