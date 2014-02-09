package com.example.gesturesapp;

import java.util.ArrayList;

import android.app.Activity;
import android.os.Bundle;
import android.view.Menu;
import android.view.MotionEvent;
import android.widget.TextView;

public class MainActivity extends Activity {

    private TextView tv;
    private PufDrawView pufDrawView;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
        tv = (TextView) findViewById( R.id.textview );
        pufDrawView = (PufDrawView) findViewById( R.id.pufDrawView );
        pufDrawView.setTV(tv);
        ArrayList<Point> challenge = new ArrayList<Point>();
        challenge.add(new Point(100, 300, 0));
        challenge.add(new Point(500, 300, 0));
        challenge.add(new Point(500, 700, 0));
        challenge.add(new Point(100, 700, 0));
        pufDrawView.giveChallenge(challenge.toArray(new Point[challenge.size()]));
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

//    @Override
//    public boolean onTouchEvent( MotionEvent me )
//    {
//        switch( me.getAction() )
//        {
//            case MotionEvent.ACTION_DOWN:
//                tv.setText( "Touch (x,y) = (" + me.getX() + ", " + me.getY() + ")" );
//                break;
//            case MotionEvent.ACTION_UP:
//                tv.setText( "No touch detected." );
//                break;
//            case MotionEvent.ACTION_MOVE:
//                tv.setText( "Touch (x,y) = (" + me.getX() + ", " + me.getY() + ")" );
//                break;
//            default:
//                break;
//        }
//
//        return true;
//    }

}
