package edu.ai.oval

import android.content.Intent
import android.graphics.Bitmap
import android.os.Bundle
import android.provider.MediaStore
import android.util.Base64
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ImageButton
import android.widget.ImageView
import android.widget.LinearLayout
import android.widget.ProgressBar
import android.widget.ScrollView
import android.widget.TextView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.view.children
import androidx.core.view.contains
import androidx.core.view.get
import org.json.JSONArray
import org.json.JSONObject
import java.io.ByteArrayOutputStream


class MainActivity : AppCompatActivity() {
    private val tag: String="MainActivity"
    private var imageView: ImageView? = null
    private lateinit var utils: Utils
    private lateinit var socketController: SocketController
    private var scrollView :ScrollView? = null
    private lateinit var  collapseButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        supportActionBar?.hide()
        super.onCreate(savedInstanceState)
        utils = Utils(this)
        socketController = SocketController(this, utils)
        collapseButton = layoutInflater.inflate(R.layout.compact_button, null) as  Button
        tryToConnectToTheServer()
    }

    override fun onDestroy() {
        super.onDestroy()
        socketController.disconnect(1000, "App Closed")
    }

    fun notifyCon(isConnected:Boolean, attemptingToConnect:Boolean = false){
        try{
        runOnUiThread {
            if(isConnected){
                setContentView(R.layout.activity_main)
                imageView = findViewById(R.id.image_view)
                val button = findViewById<Button>(R.id.photo_button)
                button.setOnClickListener {
                    val cameraIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                    resultLauncher.launch(cameraIntent)
                }
                scrollView = findViewById(R.id.scrollView)
                val scrollToTopBtn: ImageButton = findViewById(R.id.scroll_to_top_button)
                scrollToTopBtn.setOnClickListener{   run {
                        scrollView?.smoothScrollTo(0,0)
                    }
                }
                scrollView?.setOnScrollChangeListener { _, _, scrollY, _, _ -> run {
                        if (scrollY >= scrollView!!.height * 0.2 && scrollToTopBtn.visibility != View.VISIBLE) {
                            scrollToTopBtn.visibility = View.VISIBLE
                        } else if (scrollY <= scrollView!!.height * 0.2 && scrollToTopBtn.visibility != View.GONE) {
                            scrollToTopBtn.visibility = View.GONE
                        }
                    }
                }
            }else{
                setContentView(R.layout.main_connection)
                if(attemptingToConnect){
                    findViewById<ConstraintLayout>(R.id.connecting_constrain_layout).visibility = View.VISIBLE
                    findViewById<ConstraintLayout>(R.id.reconnect_constrain_layout).visibility = View.GONE
                }else{
                    findViewById<ConstraintLayout>(R.id.connecting_constrain_layout).visibility = View.GONE
                    findViewById<ConstraintLayout>(R.id.reconnect_constrain_layout).visibility = View.VISIBLE
                    Toast.makeText(this,"No Connection",Toast.LENGTH_SHORT).show()
                    findViewById<Button>(R.id.reconnect_button).setOnClickListener { tryToConnectToTheServer() }
                }
            }
        }
        }catch (e:Exception){
            Log.e(tag,"ERROR: ${e.message} ---> ${e.cause}")
        }
    }



    private fun tryToConnectToTheServer(){
        try {
            socketController.connect()
        }catch (e:Exception){
            Log.e(tag,"ERROR: ${e.message} ---> ${e.cause}")
            notifyCon(false)
        }
    }

    fun displayServerResponse(jsonData: JSONArray) {
        runOnUiThread{
            val container = findViewById<LinearLayout>(R.id.predictions_linear_layout)
            collapseButton.setOnClickListener {

                // if list is collapsed expand it
                if (collapseButton.text.equals(getString(R.string.expand))){
                    for (c in container.children){
                        c.visibility = View.VISIBLE
                    }
                    collapseButton.text = getString(R.string.collapse)
                }else{ // if list is expanded collapse it
                    for (i in 6 until container.childCount -1){
//                        Log.d(tag, "collapsing $i")
                        container[i].visibility = View.GONE
                    }
                    collapseButton.text = getString(R.string.expand)
                }
            }
            if(container.childCount!= jsonData.length()){//Different sizes -> remove all and add new views
                container.removeAllViews()
                for (i in  0 until jsonData.length()){
                    val entry = jsonData.get(i) as JSONObject
                    val clas = entry.getString("Class")
                    val prob = entry.getString("Probability")
                    val view = layoutInflater.inflate(R.layout.probability,null) as LinearLayout
                    (((view[0])as LinearLayout) [0] as TextView).text = clas
                    (((view[0])as LinearLayout) [1] as TextView).text = prob
                    ((view[1])as ProgressBar ).progress = (prob.toFloat() * 100).toInt()
                    container.addView(view)
                    if(i>=5)
                        view.visibility = View.GONE
                }
            }else{// If sizes are same -> no need to recreated and read views
                for (i in  0 until jsonData.length()){
                    val view = container[i] as LinearLayout
                    val entry = jsonData.get(i) as JSONObject
                    val clas = entry.getString("Class")
                    val prob = entry.getString("Probability")
                    (((view[0])as LinearLayout) [0] as TextView).text = clas
                    (((view[0])as LinearLayout) [1] as TextView).text = prob
                    ((view[1])as ProgressBar ).progress = (prob.toFloat() * 100).toInt()
                    if(i>=5)
                        view.visibility = View.GONE
                }
            }

            if(container.childCount > 5 && !container.contains(collapseButton)) {
                container.addView(collapseButton)
            }else {
                container.removeView(collapseButton)
            }
        }
    }

    private var resultLauncher = registerForActivityResult(ActivityResultContracts.StartActivityForResult()){ result ->
        if( result.resultCode == RESULT_OK){
//            Display captured image
            val data = result.data?.extras?.get("data") as Bitmap
            imageView?.setImageBitmap(data)
//          Convert image to String data and send to the server
            val byteArrayOutputStream = ByteArrayOutputStream()
            data.compress(Bitmap.CompressFormat.JPEG,100, byteArrayOutputStream)
            val message = Base64.encodeToString(byteArrayOutputStream.toByteArray(), Base64.DEFAULT)
//            Log.i(TAG,"Sending: $message")
            socketController.send(message)

        }
    }
}


