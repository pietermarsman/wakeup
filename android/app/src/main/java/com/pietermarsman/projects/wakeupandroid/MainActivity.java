package com.pietermarsman.projects.wakeupandroid;

import android.media.TimedText;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.URL;
import java.net.URLConnection;


public class MainActivity extends AppCompatActivity {

    private class StatusRetriever extends AsyncTask<String, Void, String> {

        protected String doInBackground(String... url_string) {
            try {
                URL url = new URL(url_string[0]);
                URLConnection urlConnection = url.openConnection();
                urlConnection.setConnectTimeout(1000);
                InputStream is = urlConnection.getInputStream();
                BufferedReader reader = new BufferedReader(new InputStreamReader(is));
                StringBuilder out = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    out.append(line);
                }
                reader.close();
                return(out.toString());
            } catch (Exception ex) {
                return ex.toString();
            }
        }

        @Override
        protected void onPostExecute(String result) {
            AlarmStatus alarm;
            try {
                JSONObject json = new JSONObject(result);
                alarm = new AlarmStatus(json);
                textViewAlarmType.setText(alarm.getAlarmType().toString());
                textViewAlarms.setText(alarm.getAlarms());
            } catch (JSONException e) {
                e.printStackTrace();
            }
            super.onPostExecute(result);
        }
    }

    private TextView textViewAlarmType, textViewAlarms;
    private Button button1, button2;
    private EditText textMinute, textHour;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

       FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        textViewAlarmType = (TextView) findViewById(R.id.textView2);
        textViewAlarms = (TextView) findViewById(R.id.textView4);
        textHour = (EditText) findViewById(R.id.editText);
        textMinute = (EditText) findViewById(R.id.editText2);
        button1 = (Button) findViewById(R.id.button);

        button1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                new StatusRetriever().execute("http://192.168.2.15:5000/remove/0");
            }
        });
        button2 = (Button) findViewById(R.id.button2);
        button2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                int hour = Integer.valueOf(textHour.getText().toString());
                int minute = Integer.valueOf(textMinute.getText().toString());
                String url = String.format("http://192.168.2.15:5000/alarm/%d/%d", hour, minute);
                new StatusRetriever().execute(url);
            }
        });
    }

    @Override
    public void onResume() {
        super.onResume();

        new StatusRetriever().execute("http://192.168.2.15:5000/");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button1, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

}
