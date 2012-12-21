package com.example.rotateeclipse;

import java.util.ArrayList;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Point;
import android.view.View;

public class Draw2d extends View {
    int tickCount = 0;
    Paint paint;

    float mCenterX, mCenterY;
    double mAngle;

    ArrayList<Point> mStartPoints = new ArrayList<Point>();
    ArrayList<Point> mStopPoints = new ArrayList<Point>();

    public Draw2d(Context context) {
        super(context);
        paint = new Paint();
        mCenterX = 75f;
        mCenterY = 100f;
        mAngle = 0;
    }

    private void drawBigCircle(Canvas c) {
        paint.setStyle(Paint.Style.STROKE);
        paint.setColor(Color.BLACK);
        c.drawCircle(100.0f, 100.0f, 50, paint);
    }

    private void drawMoveCircle(Canvas c) {
        paint.setStyle(Paint.Style.STROKE);
        paint.setColor(Color.BLACK);
        c.drawCircle(mCenterX, mCenterY, 25, paint);
        final double cosValue = Math.cos(mAngle);
        final double sinValue = Math.sin(mAngle);
        final float startX = (float) (mCenterX + 25 * cosValue);
        final float stopX = (float) (mCenterX - 25 * cosValue);
        final float startY = (float) (mCenterY - 25 * sinValue);
        final float stopY = (float) (mCenterY + 25 * sinValue);
        c.drawLine(startX, startY, stopX, stopY, paint);

        Point newStart = new Point((int) startX, (int) startY);
        Point newStop = new Point((int) stopX, (int) stopY);
        if (!mStartPoints.contains(newStart)) {
            mStartPoints.add(newStart);
        }
        if (!mStopPoints.contains(newStop)) {
            mStopPoints.add(newStop);
        }

    }

    private void drawPoints(Canvas c) {
        paint.setColor(Color.RED);
        for (Point p : mStartPoints) {
            c.drawCircle(p.x, p.y, 1, paint);
        }

        paint.setColor(Color.BLUE);
        for (Point p : mStopPoints) {
            c.drawCircle(p.x, p.y, 1, paint);
        }
    }

    @Override
    public void onDraw(Canvas c) {
        super.onDraw(c);
        paint.setStyle(Paint.Style.FILL);

        paint.setColor(Color.WHITE);
        c.drawPaint(paint);

        drawBigCircle(c);
        drawMoveCircle(c);
        drawPoints(c);
    }

    public void increaseTick(int offset) {
        tickCount += offset;
        updateMoveCircle();
        invalidate();
    }

    private void updateMoveCircle() {
        double moveAngle = (2 * Math.PI * tickCount) / 360;

        double ang = moveAngle + Math.PI;
        double sinValue = Math.sin(ang);
        double cosValue = Math.cos(ang);

        mCenterX = (float) (100 + 25 * cosValue);
        mCenterY = (float) (100 - 25 * sinValue);

        mAngle = -moveAngle;
    }
}
