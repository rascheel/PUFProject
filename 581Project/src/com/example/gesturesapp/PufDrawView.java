package com.example.gesturesapp;

import java.io.File;
import java.io.FileWriter;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.os.Environment;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import au.com.bytecode.opencsv.CSVWriter;

public class PufDrawView extends View
{
    private Paint redPaint;
    private TextView tv;
    private Point[] challenge;
    private ArrayList<Point> response;

    public PufDrawView(Context context, AttributeSet attr)
    {
        super(context, attr);
        init();
    }

    public void setTV(TextView tv)
    {
        this.tv = tv;
    }

    private void init()
    {
        redPaint = new Paint();
        redPaint.setAntiAlias(true);
        redPaint.setStyle(Paint.Style.STROKE);
        redPaint.setColor(Color.RED);
        redPaint.setStrokeWidth(15);

        response = new ArrayList<Point>();
    }

    @Override
    protected void onDraw(Canvas canvas)
    {
        Path challengePath = new Path();
        for(int i = 0; i < challenge.length; i++)
        {
            if(i == 0)
            {
                challengePath.moveTo(challenge[i].x, challenge[i].y);
            }
            else
            {
                challengePath.lineTo(challenge[i].x, challenge[i].y);
            }
        }
        canvas.drawPath(challengePath, redPaint);
    }

    public void giveChallenge(Point[] challenge)
    {
        this.challenge = challenge;
        this.invalidate();
    }

    @Override
    public boolean onTouchEvent( MotionEvent me )
    {
        switch( me.getAction() )
        {
            case MotionEvent.ACTION_DOWN:
                tv.setText( "Touch (x,y) = (" + me.getX() + ", " + me.getY() + ")" );
                response.clear();
                response.add(new Point(me.getX(), me.getY(), me.getPressure()));
                break;
            case MotionEvent.ACTION_UP:
                tv.setText( "No touch detected." );
                //RECORD ACTION FINISH 
                writeResponseCsv();
                break;
            case MotionEvent.ACTION_MOVE:
                tv.setText( "Touch (x,y) = (" + me.getX() + ", " + me.getY() + ")" );
                response.add(new Point(me.getX(), me.getY(), me.getPressure()));
                break;
            default:
                break;
        }

        return true;
    }

    public void writeResponseCsv()
    {
        File baseDir = new File(Environment.getExternalStorageDirectory(), "581Proj");
        if (!baseDir.exists())
        {
            baseDir.mkdirs();
        }
        String fileName = getCurrentLocalTime();
        File f = new File(baseDir, fileName);
        try
        {
            f.createNewFile();
            CSVWriter csvWrite = new CSVWriter(new FileWriter(f));
            String[] headers = { "X", "Y", "PRESSURE" };
            csvWrite.writeNext(headers);
            for( int i = 0; i < response.size(); i++)
            {
                Point point = response.get(i);
                String[] row = { Float.toString(point.x),
                    Float.toString(point.y),
                    Float.toString(point.pressure) };
                csvWrite.writeNext(row);
            }
            csvWrite.close();
        }
        catch( Exception e)
        {
            Toast.makeText(getContext(), e.toString(), 
                                    Toast.LENGTH_SHORT).show();
        } 
    }

    public String getCurrentLocalTime()
    {
        Calendar c = Calendar.getInstance(); 
        String format = "yyyy-MM-dd hh:mm:ss aa";
        SimpleDateFormat localSdf = new SimpleDateFormat(format);
        return localSdf.format(c.getTime());
    }
}
