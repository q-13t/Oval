package edu.ai.oval

import android.content.Context
import android.content.res.Resources
import android.util.Log
import java.util.Properties

class Utils(con: Context) {
    private val tag: String = "Utils"
    private val properties: Properties = Properties()

    init {
        try {
            properties.load(con.resources.openRawResource(R.raw.config))
        }catch (e: Resources.NotFoundException){
            Log.e(tag, e.message.toString())
        }catch (e: java.io.IOException){
            Log.e(tag, e.message.toString())
        }
    }

    fun getConfigValue( name:String, default: Any): String? {
        return properties.getProperty(name, default as String?)
    }
}