import collections
from subprocess import call
import textwrap
import requests
from bs4 import BeautifulSoup
import random
import dearpygui.dearpygui as dpg
import re
from collections import Counter
from math import sin


dpg.create_context()
dpg.create_viewport(title='Daily News', width=600, height=840)


class webNews():

#is this git working?

    def refresh():

        selected_mode = dpg.get_value('cbo')

        rrr = random.randrange(700,770)


        ssss = f"https://orf.at/stories/3289{rrr}/"
        wwww = "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite"

        if(selected_mode == 'Wikipedia'):
            page = requests.get(wwww)
        if(selected_mode == 'ORF'):
            page = requests.get(ssss)

        
        thetext = ""


        soup = BeautifulSoup(page.content, 'html.parser')

        dpg.set_value('date_text', '')

        if(selected_mode == 'ORF'):
            t_date = soup.find('div', class_=('print-only')).getText()
            t_regs = re.sub(' +', ' ', t_date)
            t_sss = re.sub('^\s', '', t_regs)
            dpg.set_value('date_text', t_sss)
            print(t_date)


        h1 = soup.select('h1')[0].text.strip()
        print('\n', h1, '\n')
        dpg.set_value('title_text', h1)

        for x in soup.find_all('p'):
            print(x.getText())
            thetext += ("" + x.getText())


        thePage = ""

        if(selected_mode == 'ORF'):
            thePage = ssss
        if(selected_mode == 'Wikipedia'):
            thePage = page.url


        dpg.set_value('article_url', thePage)

        wrapper = textwrap.TextWrapper(width=50)

        det_text = textwrap.dedent(text=thetext)

        t_formatted = textwrap.fill(det_text, width=70, break_long_words=True)
        t_reg = re.sub(' +', ' ', t_formatted)
        t_ss = re.sub('^\s', '', t_reg)        

        dpg.set_value('input_text', t_ss)
        print(t_reg)
        print(page.url)

        t_cleaned = re.sub('(?![Ä-ü])\W|\d', ' ', t_ss)

        split_it = t_cleaned.split()
        Counter = collections.Counter(map(str.lower, split_it))
        most_occur = Counter.most_common(10)

        print(len(most_occur))

        print(split_it)

 
        t_items = []
     #   it_ = 0
     #   for x in split_it:

       #     it_ += 1
      #      t_items.append(it_)

        t_times = []
        ccc = 0
        for x in most_occur:
            ccc += 1
            t_items.append(ccc)
            t_times.append(x[1])


        t_names = []
        for x in most_occur:
            t_names.append(x[0]) 

        dpg.set_value('series', [t_items, t_times] )
        dpg.fit_axis_data('x_axis')
        dpg.fit_axis_data('y_axis')
        dpg.set_axis_ticks('x_axis', ((t_names[0],t_times[0]),(t_names[1],t_times[1]),(t_names[2],t_times[3]),(t_names[4],t_times[4]),(t_names[5],t_times[5])  ))

      #  print(t_items)
        print(t_times)
        temptext = ""
        countt = 0

        for x in most_occur:
            countt += 1
            temptext += (str( x[0]) + ": " + str( x[1]) + " | ")




        t_textt = textwrap.fill(temptext, width=50)
        dpg.set_value('search_result', t_textt)




    modes = ['ORF', 'Wikipedia']

    print (dpg.get_global_font_scale())
    dpg.set_global_font_scale(1)
    with dpg.window(label='Random Articles', width=585, height=800):
        dpg.add_input_text(tag='date_text', readonly=True, width=570)
        dpg.add_input_text(tag='title_text', readonly=True, width=570)
        dpg.add_input_text(tag='input_text', multiline=True, readonly=True, width=570, height= 600)
        dpg.add_button(callback=refresh, label='refresh')
        dpg.add_combo(tag='cbo', label='mode', items=modes, default_value='ORF')
        #dpg.add_button(callback=openPlot, label='Open Demographic')
        dpg.add_input_text(tag='search_result', label='Most Common Words', readonly=True, multiline=True, height=60)
        dpg.add_input_text(tag='article_url',label='Article URL', readonly=True)
        dpg.show_style_editor()
        dpg.show_font_manager()
        with dpg.plot(label="Most common words", height=400, width=400):
            # optionally create legend
            dpg.add_plot_legend()
            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="Words", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Occurences", tag="y_axis")
            # series belong to a y axis
            dpg.add_line_series([2010,2011,2012,2013,2014], [0,300,400,700,200,500], parent="y_axis", tag='series')    
              







dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()