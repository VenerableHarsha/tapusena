document.querySelector("button").addEventListener("click",function()
{
    var firstname=document.getElementById("fname").value;
    var lastname=document.getElementById("lname").value;
    var country=document.getElementById("country").value;
    var phone=document.getElementById("numb").value;
    var email=document.getElementById("E-mail").value;
    var address=document.getElementById("add").value;
    var newpassword=document.getElementById("pass").value;
    var confirmpassword=document.getElementById("newpass").value;
    if(checkphone(phone)==true&&checkpass(newpassword,confirmpassword)==true)
    {
        window.open("../registerrr/blah.html");

    }
    else if(checkpass(newpassword,confirmpassword)==false)
    {
        alert("check your password");
    }
    else if(checkphone(phone)==false)
    {
        alert("Enter a valid a valid number");
    }
    

})
function checkphone(number)
{
    if(number.length!=10)
    {
        return false;
    }
    else{
        return true;
    }

}
function checkpass(newpass,oldpass)
{
    if(newpass==oldpass)
    {
        return true;
    }
    else{
        return false;
    }
}