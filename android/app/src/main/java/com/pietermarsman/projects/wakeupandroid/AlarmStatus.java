package com.pietermarsman.projects.wakeupandroid;

import org.json.JSONException;
import org.json.JSONObject;

/**
 * Created by pieter on 11/29/16.
 */
public class AlarmStatus {
    
    private JSONObject json;
    private JSONObject instructions;
    private JSONObject state;
    private AlarmType alarmType;
    private String alarms;
    
    public AlarmStatus(JSONObject json) {
        this.json = json;
        this.parse_json();
    }

    private void parse_json() {
        try {
            this.instructions = this.json.getJSONObject("instructions");
            this.state = this.json.getJSONObject("state");
            this.alarmType = AlarmType.valueOf(this.state.get("alarm_type").toString());
            this.alarms = this.state.get("alarms").toString();
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public AlarmType getAlarmType() {
        return this.alarmType;
    }

    public String getAlarms() {
        return this.alarms;
    }

    public String toString() {
        return this.alarmType + "\n\n" + this.alarms;
    }
}
