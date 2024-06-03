package edu.ai.oval

import android.util.Log
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import org.json.JSONArray


class SocketController(private val activity: MainActivity, private val utils: Utils) : WebSocketListener() {
    private val tag: String = "SocketController"
    private var socket: WebSocket?=null
    private var connected:Boolean = false

    fun send(data: String){
        socket?.send(data)
    }

    fun connect(){
        val ip = utils.getConfigValue("IP","")
        val port = utils.getConfigValue("PORT","")
        if(ip.equals("") or port.equals(""))
            throw Exception("Bad Path")
        val path = "ws://$ip:$port"
        Log.i(tag, "Connecting to: $path")
        socket = OkHttpClient().newWebSocket(Request.Builder().url(path).build(),this)
        activity.notifyCon(isConnected= false, attemptingToConnect = true)
    }

    fun disconnect(code :Int, reason:String){
        socket?.close(code, reason)
    }

    fun getConnected(): Boolean{
        return connected
    }

    private fun setConnected(boolean: Boolean){
        connected = boolean
    }

    override fun onOpen(webSocket: WebSocket, response: Response) {
        super.onOpen(webSocket, response)
        socket = webSocket
        setConnected(true)
        activity.notifyCon( true)
        Log.i(tag, "<----------WEB SOCKET CONNECTED---------->")
    }

    override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
        super.onClosed(webSocket, code, reason)
        socket = null
        Log.i(tag, "<----------WEB SOCKET DISCONNECTED---------->")
        setConnected(false)
        activity.notifyCon(false)
    }

    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
        super.onFailure(webSocket, t, response)
        Log.e(tag,"ERROR: ${t.message} ---> ${t.cause}")
        disconnect(1000, "Reset Accept")
        activity.notifyCon(false)
    }

    override fun onMessage(webSocket: WebSocket, text: String) {
        super.onMessage(webSocket, text)

        try {
            val jsonData = JSONArray(text)
            activity.displayServerResponse(jsonData)
        } catch (e:Exception){
            Log.e(tag,"ERROR: ${e.message} ---> ${e.cause}")
        }

    }
}