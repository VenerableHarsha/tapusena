package com.example.helloworld

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.MaterialTheme
import androidx.compose.material.Surface
import androidx.compose.material.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.example.helloworld.ui.theme.HelloWorldTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            HelloWorldTheme {
                // A surface container using the 'background' color from the theme
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colors.background) {
                   
                }
            }
        }
    }
}

@Composable
fun BirthdayCard(){

}

Box{
    Image(
        painter = bg,
        contentDescription = null,
        modifier= Modifier
            .fillMaxWidth()
            .fillMaxHeight(),
        contentScale = ContentScale.Crop
    )
    BirthdayCardText()
}
@Preview(showBackground = true, showSystemUi = true)//it tells that whatever we right should be previewed
@Composable
fun BirthdayCardPreview(){
//    BirthdayCardText()
    BirtdayCardImage()
}
@Composable //it tells the compiler that its ui part of the app
fun BirthdayCardText(){

    Column {            //used to place elements one above the other
        Text(
            text="Happy birthday Compose",
            fontSize = 36.sp  //scale dependent pixels - unit given to text -100%,200%
        )
        Text(
            text="- from Girish",
            fontSize= 24.sp,
        )
    }
}