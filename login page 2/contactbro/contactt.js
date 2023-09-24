document.getElementById("btn_send").addEventListener("click",function(){
    var name=document.getElementById("txt_name").value;
    var email=document.getElementById("txt_email").value;
    var phone=document.getElementById("txt_phone").value;
    var subject=document.getElementById("txt_subject").value;
    var message=document.getElementById("txt_message").value;
    if(checkphone(phone)&&checkmessage(subject,message))
    {
        alert("Your message has been sent!");
        window.open("../homepage.html");
    }
    else if(checkphone(phone)==false)
    {
        alert("Plz enter a valid number");
    }
    else if(checkmessage(subject,message)==false)
    {
        alert("Plz fill up the text boxes");
    }
    

})
function checkmessage(subject,message)
{
    if(subject.length>0&&message.length>0)
    {
        return true;
    }
    else{
        false;
    }
}
function checkphone(number)
{
    var count=0;
    if(number.length==10)
    {
        for(var i=0;i<number.length;i++)
        {
            if(number[i]>='0'&&number[i]<='9')
            {
                count++;
            }
        }
        if(count==10)
        {
            return true;
        }
        else{
            return false;
        }
    }
    else{
        return false;
    }
    
}