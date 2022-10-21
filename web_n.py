import collections
import textwrap
import requests
from bs4 import BeautifulSoup
import random
import dearpygui.dearpygui as dpg
import re



dpg.create_context()
dpg.create_viewport(title='Daily News', width=1000, height=850)


class webNews():


    def refresh():

        selected_mode = dpg.get_value('cbo')

#Website init


        wikipedia = "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite"

    #Getting current links from the site

        lg_page = requests.get("https://orf.at/")
        lg_soup = BeautifulSoup(lg_page.content, 'html.parser')
        lg_links = lg_soup.find_all('a',{'href': re.compile('^.*\d{2}.')})


        lg_li = []

        for a in lg_links:
            lg_li.append(a['href'])


        if(selected_mode == 'Wikipedia'):
            page = requests.get(wikipedia)
        if(selected_mode == 'ORF'):
            page = requests.get(lg_li[random.randrange(0,len(lg_li))])

    #Pseudo text init
        
        thetext = ""

#The scarping part

        soup = BeautifulSoup(page.content, 'html.parser')
        dpg.set_value('date_text', '')
        
    #Extracting div class 'print-only' (Date the article was published) from html and removing unnecesary whitespaces using regex substitution

        if(selected_mode == 'ORF'):
            t_date = soup.find('div', class_=('print-only')).getText()
            t_date = re.sub(' +', ' ', t_date)
            t_date = re.sub('^\s', '', t_date)
            dpg.set_value('date_text', t_date)
            print(t_date)

    #Extracting Heading

        h1 = soup.select('h1')[0].text.strip()
        print('\n', h1, '\n')
        dpg.set_value('title_text', h1)

    #Extracting Phrases

        for x in soup.find_all('p'):
            print(x.getText())
            thetext += ("" + x.getText())

#Text formatting and UI filling

    #Setting Article URL text

        thePage = ""
        if(selected_mode == 'ORF'):
            thePage = orf
        if(selected_mode == 'Wikipedia'):
            thePage = page.url

        dpg.set_value('article_url', thePage)

    #Text fromatting using textwrap and regex

        wrapper = textwrap.TextWrapper(width=50)
        t_formatted = textwrap.dedent(text=thetext)

        t_formatted = textwrap.fill(t_formatted, width=70, break_long_words=True)
        t_formatted = re.sub(' +', ' ', t_formatted)
        t_formatted = re.sub('^\s', '', t_formatted)        

        dpg.set_value('input_text', t_formatted)

        print(page.url)

#Word counting

    #Splitting String into a list with all words and counting the most used ones

        t_cleaned = re.sub('(?![Ä-ü])\W|\d', ' ', t_formatted)

        if(dpg.get_value('filter_words')):
            t_cleaned = re.sub(r'\b(d|D|)e(r|s)\b|\b(d|D)ie\b|\b(d|D)as\b|\b(i|I)n\b|\b(i|I)m\b|\b(i|I)ns\b|\b(a|A)uf\b|\b(v|V)on\b|\b(z|Z)u\b|\b(d|D)en\b|\b(d|D)em\b|\b(u|U)nd\b|\b(a|A)ls\b|\b(b|B)ei\b|\b(b|B)eim\b|\b(i|I)st\b|\b(e|E)in\b|\b(a|A)us\b|\b(m|M)it\b|\b(e|E)ine(|n)\b|\b(a|A)n\b|\b(b|B)is\b|\b(e|E)\b|\b(n|N)ach\b|\b(f|F)ür\b|\b(a|A)(n|m)\b|\b(s|S)i(e|ch)\b|\b(w|W)(ar|er|s)', '', t_cleaned)


        split_it = t_cleaned.split()
        Counter = collections.Counter(map(str.lower, split_it))
        most_occur = Counter.most_common(10)

    #Debug: Printing Word count and the full word array

        print(len(most_occur))
        print(split_it)

    #Setting arrays for the graph

        t_items = []
        t_times = []
        t_names = []
        ccc = 0

#Plotting the graph

    #Filling graph with the data about most common words

        for x in most_occur:
            ccc += 1
            t_items.append(ccc)
            t_times.append(x[1])

        for x in most_occur:
            t_names.append(x[0]) 

    #Setting piechar values and labels 

        dpg.configure_item('pie', labels=[t_names[0],t_names[1], t_names[2], t_names[3], t_names[4]])
        dpg.set_value('pie', [[t_times[0],t_times[1],t_times[2],t_times[3], t_times[4]], [], [], [], []])

        print(t_times)
 
 
    #Debug: Setting most common words result text

        temptext = ""
        count = 0

        for x in most_occur:
            count += 1
            temptext += (str( x[0]) + ": " + str( x[1]) + " | ")

        t_textt = textwrap.fill(temptext, width=50)
        dpg.set_value('search_result', t_textt)



    #Item list declaration for the combobox

    modes = ['ORF', 'Wikipedia']

#UI Initialisation

    with dpg.window(label='Random Articles', width=1000, height=820):
        dpg.add_input_text(tag='date_text', readonly=True, width=570)
        dpg.add_input_text(tag='title_text', readonly=True, width=570)
        dpg.add_input_text(tag='input_text', multiline=True, readonly=True, width=570, height= 600)
        dpg.add_button(callback=refresh, label='refresh', width=570)
        dpg.add_combo(tag='cbo', label='mode', items=modes, default_value='ORF',width=570)
        dpg.add_input_text(tag='search_result', label='Most Common Words', readonly=True, multiline=True, height=60,width=570)
        dpg.add_input_text(tag='article_url',label='Article URL', readonly=True,width=570)
        dpg.add_checkbox(tag='filter_words', label='Filter common words', pos=[580,430], default_value=True)
        dpg.show_style_editor()
        dpg.show_font_manager()
        
#Plot Initialisation

        with dpg.plot(label='Most common words', no_mouse_pos=True, width=400, height=400, pos=[580,27]):

            plttt = dpg.add_plot_legend(show=True)
            dpg.show_item(plttt)

            dpg.add_plot_axis(dpg.mvXAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True  )
            dpg.set_axis_limits(dpg.last_item(), 0, 1)

            with dpg.plot_axis(dpg.mvYAxis, label="", no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
                dpg.set_axis_limits(dpg.last_item(), 0, 1)
                dpg.add_pie_series(0.5,0.5,0.5, [1,2,3], ["Most", 'common', 'words'] , normalize=True, tag='pie')
                print(dpg.get_value('pie'))
                print(dpg.get_item_configuration("pie"))

#Show UI
            
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()