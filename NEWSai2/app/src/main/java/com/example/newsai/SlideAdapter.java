package com.example.newsai;

import android.graphics.Color;
import android.support.annotation.NonNull;
import android.support.v4.view.PagerAdapter;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class SlideAdapter extends PagerAdapter{
    Context context;
    LayoutInflater inflater;



    public int[] list_images = {
            R.drawable.image_2,
            R.drawable.image_1,
            R.drawable.image_3
    };

    public String[] list_title = {

            "TRENDING",
            "NEWS.ai",
            "HISTORY",
    };

    public String[] lst_description = {
            "Description 1",
            "Description 2",
            "Description 3",

    };

    public int[] lst_backgroundcolors= {
            Color.rgb(244,244,239),
            Color.rgb(244,244,239),
            Color.rgb(244,244,239),
    };

    public SlideAdapter(Context context){
        this.context = context;

    }

    @Override
    public int getCount(){
        return list_title.length;

    }


    @Override
    public boolean isViewFromObject( View view,  Object object) {
        return (view ==(LinearLayout)object);
    }

    @Override
    public Object instantiateItem(@NonNull ViewGroup container, int position) {
        inflater = (LayoutInflater) context.getSystemService(context.LAYOUT_INFLATER_SERVICE);
        View view = inflater.inflate(R.layout.slide1,container, false);
        LinearLayout layoutslide = view.findViewById(R.id.slidelinearlayout);
        ImageView imageslide = (ImageView) view.findViewById(R.id.slideimg);
        TextView txttitle = (TextView) view.findViewById(R.id.txttitle);
        TextView description = (TextView) view.findViewById(R.id.txtdescription);
        layoutslide.setBackgroundColor(lst_backgroundcolors[position]);
        imageslide.setImageResource(list_images[position]);
        txttitle.setText(list_title[position]);
        description.setText(lst_description[position]);
        container.addView(view);
        return view;
    }

    @Override
    public void destroyItem(@NonNull ViewGroup container, int position, @NonNull Object object) {
        container.removeView((LinearLayout)object);
    }
}
