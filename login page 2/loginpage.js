

document.querySelector("button").addEventListener("click",function(){
    var username=document.getElementById("name").value;
    var password=document.getElementById("pass").value;
    if(check(password)==true&&checkgmail(username)){
        alert("Welcome back "+username.slice(0,username.indexOf("@")));
        window.open("./homepage.html");
    }
    else{
        alert("wrong password or userid");
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
function checkforsame(password,username)
{
    if(password!="terimaki")
    {
        alert("wrong password");
        return false;
    }
    else if(username!="tahapasha121@gmail.com")
    {
        alert("wrong username");
        return false;
    }
   return true;
}
