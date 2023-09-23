document.querySelector("input").addEventListener("click",function(){
    var hobbies=document.getElementById("id1").value;
    var harass=document.getElementById("id2").value;
    if(checkfam(hobbies)==true&&checkharas(harass)==true){
    alert("Your messgae has been recieved ");
    }
    else{
        alert("Please fill both the boxes");
    }
})

function checkfam(context)
{
    if(context.length!=0)
    {
        return true;
    }
    else{
        return false;

    }
}
function checkharas(context)
{
    if(context.length!=0)
    {
        return true;
    }
    else{
        return false;

    }
}